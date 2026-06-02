import json
import math
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, "..", ".."))
DECK_MANIFEST_PATH = os.path.join(REPO_ROOT, "data", "major-arcana-v5-deck.json")
DECK_VALIDATION_PATH = os.path.join(PROJECT_DIR, "Saved", "V5DeckManifestValidationResult.json")
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1OneCardTableMapResult.json")
CHECKPOINT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1OneCardTableMapCheckpoint.json")

MAP_PATH = "/Game/ONOKOArcana/Maps/L_Phase1_OneCard_Table"
TEMPLATE_MAP_PATH = "/Game/ONOKOArcana/Maps/L_QA_CardAlpha_V5_Full"
MATERIAL_DIR = "/Game/ONOKOArcana/Phase1/Materials"

CARD_SCALE = {"x": 0.72, "y": 1.08, "z": 1.0}
CARD_Z = 6.0


def log(message):
    unreal.log("[ONOKO_ARCANA_PHASE1_TABLE] " + message)
    print("[ONOKO_ARCANA_PHASE1_TABLE] " + message)


def checkpoint(stage, **extra):
    payload = {"stage": stage}
    payload.update(extra)
    os.makedirs(os.path.dirname(CHECKPOINT_PATH), exist_ok=True)
    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def save_asset(asset):
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


def ensure_dirs():
    unreal.EditorAssetLibrary.make_directory(MATERIAL_DIR)


def delete_asset_if_exists(asset_path):
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.EditorAssetLibrary.delete_asset(asset_path)


def level_subsystem():
    return unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)


def actor_subsystem():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def create_flat_material(name, color, unlit=False):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_path = f"{MATERIAL_DIR}/{name}"
    existing = unreal.load_asset(material_path)
    if existing is not None:
        return existing
    material = asset_tools.create_asset(
        asset_name=name,
        package_path=MATERIAL_DIR,
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    if material is None:
        raise RuntimeError(f"Could not create material: {material_path}")

    vector = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionConstant3Vector,
        -240,
        0,
    )
    vector.constant = unreal.LinearColor(*color)

    if unlit:
        material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        unreal.MaterialEditingLibrary.connect_material_property(
            vector,
            "",
            unreal.MaterialProperty.MP_EMISSIVE_COLOR,
        )
    else:
        unreal.MaterialEditingLibrary.connect_material_property(
            vector,
            "",
            unreal.MaterialProperty.MP_BASE_COLOR,
        )

    material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    save_asset(material)
    return material


def create_card_material(name, texture_path):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_path = f"{MATERIAL_DIR}/{name}"
    existing = unreal.load_asset(material_path)
    if existing is not None:
        return existing
    material = asset_tools.create_asset(
        asset_name=name,
        package_path=MATERIAL_DIR,
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    if material is None:
        raise RuntimeError(f"Could not create material: {material_path}")

    texture = unreal.load_asset(texture_path)
    if texture is None and "." in texture_path:
        texture = unreal.load_asset(texture_path.split(".", 1)[0])
    if texture is None:
        raise RuntimeError(f"Could not load texture: {texture_path}")

    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionTextureSample,
        -360,
        0,
    )
    sample.texture = texture
    unreal.MaterialEditingLibrary.connect_material_property(
        sample,
        "RGB",
        unreal.MaterialProperty.MP_BASE_COLOR,
    )
    unreal.MaterialEditingLibrary.connect_material_property(
        sample,
        "A",
        unreal.MaterialProperty.MP_OPACITY_MASK,
    )
    material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
    material.set_editor_property("opacity_mask_clip_value", 0.333)
    material.set_editor_property("two_sided", True)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    save_asset(material)
    return material


def disable_shadows(actor):
    component = getattr(actor, "static_mesh_component", None)
    if not component:
        return
    try:
        component.set_editor_property("cast_shadow", False)
        component.set_cast_shadow(False)
    except Exception:
        pass


def spawn_mesh(mesh_path, label, material, location, scale, yaw=0.0, disable_shadow=False):
    mesh = unreal.load_asset(mesh_path)
    if mesh is None:
        raise RuntimeError(f"Could not load mesh: {mesh_path}")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        mesh,
        unreal.Vector(*location),
        unreal.Rotator(0.0, yaw, 0.0),
    )
    set_label(actor, label)
    actor.set_actor_scale3d(unreal.Vector(scale["x"], scale["y"], scale.get("z", 1.0)))
    actor.static_mesh_component.set_material(0, material)
    if disable_shadow:
        disable_shadows(actor)
    return actor


def spawn_plane(label, material, location, scale, yaw=0.0, disable_shadow=False):
    return spawn_mesh("/Engine/BasicShapes/Plane.Plane", label, material, location, scale, yaw, disable_shadow)


def spawn_cube(label, material, location, scale, yaw=0.0, disable_shadow=False):
    return spawn_mesh("/Engine/BasicShapes/Cube.Cube", label, material, location, scale, yaw, disable_shadow)


def spawn_rectangle_outline(label, center, width, height, material, z=4.0, thickness=4.0):
    x, y = center
    spawn_cube(f"{label}_Top", material, (x, y + height / 2.0, z), {"x": width / 100.0, "y": thickness / 100.0, "z": 0.025}, 0.0, True)
    spawn_cube(f"{label}_Bottom", material, (x, y - height / 2.0, z), {"x": width / 100.0, "y": thickness / 100.0, "z": 0.025}, 0.0, True)
    spawn_cube(f"{label}_Left", material, (x - width / 2.0, y, z), {"x": height / 100.0, "y": thickness / 100.0, "z": 0.025}, 90.0, True)
    spawn_cube(f"{label}_Right", material, (x + width / 2.0, y, z), {"x": height / 100.0, "y": thickness / 100.0, "z": 0.025}, 90.0, True)


def spawn_ring(label, center, radius, material, segment_count=64, z=3.5, thickness=3.0):
    cx, cy = center
    segment_length = (2.0 * math.pi * radius) / segment_count
    for index in range(segment_count):
        angle = (2.0 * math.pi * index) / segment_count
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius
        yaw = math.degrees(angle) + 90.0
        spawn_cube(
            f"{label}_{index:02d}",
            material,
            (x, y, z),
            {"x": segment_length / 100.0, "y": thickness / 100.0, "z": 0.018},
            yaw,
            True,
        )


def prepare_level():
    checkpoint("prepare_level:start")
    checkpoint("prepare_level:load_level")
    level_subsystem().load_level(MAP_PATH)
    checkpoint("prepare_level:set_current_level")
    try:
        level_subsystem().set_current_level_by_name("PersistentLevel")
    except Exception as exc:
        checkpoint("prepare_level:set_current_level_failed", error=str(exc))
    checkpoint("prepare_level:get_all_actors")
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    checkpoint("prepare_level:destroy_actors", actorCount=len(actors))
    for actor in actors:
        try:
            class_name = actor.get_class().get_name()
        except Exception:
            class_name = ""
        if class_name == "WorldSettings":
            continue
        unreal.EditorLevelLibrary.destroy_actor(actor)
    checkpoint("prepare_level:done")
    return None


def load_manifest():
    if not os.path.exists(DECK_VALIDATION_PATH):
        raise RuntimeError(f"Run validate_v5_deck_manifest.py first: {DECK_VALIDATION_PATH}")
    with open(DECK_VALIDATION_PATH, "r", encoding="utf-8") as fp:
        validation = json.load(fp)
    if not validation.get("ok"):
        raise RuntimeError(f"Deck validation is not ok: {DECK_VALIDATION_PATH}")

    with open(DECK_MANIFEST_PATH, "r", encoding="utf-8") as fp:
        manifest = json.load(fp)
    cards_by_id = {card["id"]: card for card in manifest.get("cards", [])}
    return manifest, cards_by_id


def spawn_cards(back_material, sample_material):
    # Deck stack on the lower-left side.
    deck_positions = [(-250.0, -185.0, CARD_Z), (-246.0, -181.0, CARD_Z + 0.8), (-242.0, -177.0, CARD_Z + 1.6)]
    for index, location in enumerate(deck_positions):
        spawn_plane(
            f"Phase1_Deck_Back_{index + 1}",
            back_material,
            location,
            CARD_SCALE,
            0.0,
            True,
        )

    # One revealed sample card at the central reading slot.
    spawn_plane(
        "Phase1_Revealed_Sample_Major_01_Magician",
        sample_material,
        (0.0, -20.0, CARD_Z + 1.2),
        CARD_SCALE,
        0.0,
        True,
    )


def spawn_camera_and_lights():
    sun = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(-180.0, -360.0, 520.0),
        unreal.Rotator(-54.0, -18.0, 0.0),
    )
    set_label(sun, "Phase1_Table_Key_Light")
    try:
        sun.light_component.set_intensity(1.5)
    except Exception:
        pass

    fill = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PointLight,
        unreal.Vector(220.0, -180.0, 180.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(fill, "Phase1_Table_Blue_Fill_Light")
    try:
        fill.light_component.set_intensity(1800.0)
        fill.light_component.set_light_color(unreal.LinearColor(0.05, 0.24, 1.0, 1.0))
    except Exception:
        pass

    camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(0.0, -620.0, 430.0),
        unreal.Rotator(-55.0, 0.0, 0.0),
    )
    set_label(camera, "Phase1_OneCard_Table_Camera")
    camera.camera_component.set_field_of_view(39.0)
    return camera


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    ensure_dirs()
    manifest, cards_by_id = load_manifest()
    sample_card = cards_by_id["major-01-magician"]

    world = prepare_level()

    table = create_flat_material("M_Phase1_Dark_Walnut_Table", (0.025, 0.018, 0.013, 1.0))
    acrylic = create_flat_material("M_Phase1_Black_Acrylic_Mat", (0.003, 0.006, 0.012, 1.0))
    panel = create_flat_material("M_Phase1_Side_Panel_Dark_Glass", (0.009, 0.015, 0.026, 1.0))
    blue = create_flat_material("M_Phase1_Electric_Blue_Line", (0.0, 0.28, 1.0, 1.0), unlit=True)
    gold = create_flat_material("M_Phase1_Muted_Gold_Trim", (0.78, 0.56, 0.28, 1.0), unlit=True)
    back_material = create_card_material("M_Phase1_Card_Back_V5", manifest["back"]["unrealTexture"])
    sample_material = create_card_material("M_Phase1_Major_01_Magician_V5", sample_card["unrealTexture"])

    checkpoint("main:materials_ready")
    spawn_plane("Phase1_Dark_Walnut_Table_Surface", table, (0.0, 0.0, 0.0), {"x": 12.0, "y": 8.0, "z": 1.0})
    checkpoint("main:table_surface_spawned")
    spawn_plane("Phase1_Black_Acrylic_Reading_Mat", acrylic, (0.0, -20.0, 1.0), {"x": 7.2, "y": 5.2, "z": 1.0})
    checkpoint("main:reading_mat_spawned")

    spawn_ring("Phase1_Observation_Ring_Outer", (0.0, -20.0), 220.0, blue, 72, 3.5, 3.0)
    spawn_ring("Phase1_Observation_Ring_Inner", (0.0, -20.0), 150.0, blue, 56, 3.8, 2.2)

    spawn_rectangle_outline("Phase1_Central_Draw_Slot_Gold", (0.0, -20.0), 96.0, 142.0, gold, 4.4, 4.0)
    spawn_rectangle_outline("Phase1_Deck_Zone_Blue", (-250.0, -185.0), 96.0, 142.0, blue, 4.0, 3.0)

    spawn_plane("Phase1_Left_Note_Panel", panel, (-360.0, 70.0, 2.2), {"x": 2.0, "y": 2.65, "z": 1.0}, -7.0)
    spawn_rectangle_outline("Phase1_Left_Note_Panel_Trim", (-360.0, 70.0), 210.0, 280.0, gold, 4.5, 3.0)
    spawn_plane("Phase1_Right_Guide_Panel", panel, (360.0, 70.0, 2.2), {"x": 2.0, "y": 2.65, "z": 1.0}, 7.0)
    spawn_rectangle_outline("Phase1_Right_Guide_Panel_Trim", (360.0, 70.0), 210.0, 280.0, gold, 4.5, 3.0)

    # Small top plaque, matching the kanban board's blue/gold device language.
    spawn_plane("Phase1_ONOKO_Arcana_Back_Plaque", panel, (0.0, 270.0, 2.4), {"x": 3.2, "y": 0.78, "z": 1.0})
    spawn_rectangle_outline("Phase1_ONOKO_Arcana_Back_Plaque_Trim", (0.0, 270.0), 340.0, 86.0, blue, 4.8, 3.0)

    spawn_cards(back_material, sample_material)
    camera = spawn_camera_and_lights()

    result = {
        "ok": True,
        "mapPath": MAP_PATH,
        "deckValidation": DECK_VALIDATION_PATH,
        "deckId": manifest.get("deckId"),
        "sampleCard": {
            "id": sample_card["id"],
            "englishName": sample_card["englishName"],
            "japaneseName": sample_card["japaneseName"],
            "texture": sample_card["unrealTexture"],
        },
        "backTexture": manifest["back"]["unrealTexture"],
        "cardScale": CARD_SCALE,
        "materialsRoot": MATERIAL_DIR,
        "camera": {
            "actorLabel": "Phase1_OneCard_Table_Camera",
            "location": [0.0, -620.0, 430.0],
            "rotation": [-55.0, 0.0, 0.0],
            "fov": 39.0,
        },
        "mapSaveAttempted": False,
        "mapSaved": False,
        "acceptanceNotes": [
            "This is the first production-like table preview map, not the final runtime Blueprint flow.",
            "Cards use the validated V5 candidate deck textures.",
            "QA checkerboard maps remain separate and unchanged.",
        ],
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    result["mapSaveAttempted"] = True
    result["mapSaved"] = bool(unreal.EditorLoadingAndSavingUtils.save_current_level())
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    if not result["mapSaved"]:
        raise RuntimeError(f"Could not save map: {MAP_PATH}")
    log(f"Created map {MAP_PATH}")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_PHASE1_TABLE] " + str(exc))
    print("[ONOKO_ARCANA_PHASE1_TABLE_ERROR] " + str(exc), file=sys.stderr)
    raise
