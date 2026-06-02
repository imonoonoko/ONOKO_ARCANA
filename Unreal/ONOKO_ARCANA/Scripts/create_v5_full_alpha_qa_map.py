import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STAGING_DIR = os.path.join(PROJECT_DIR, "ImportStaging", "MajorArcana_V5_Full")
IMPORT_RESULT_PATH = os.path.join(STAGING_DIR, "v5-full-import-result.json")
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "V5FullAlphaQAMapResult.json")

MAP_PATH = "/Game/ONOKOArcana/Maps/L_QA_CardAlpha_V5_Full"
MATERIAL_DIR = "/Game/ONOKOArcana/QA/Materials/V5Full"
TEXTURE_ROOT = "/Game/ONOKOArcana/Cards/Textures/V5Full"

CARD_PLANE_SCALE = {"x": 0.68, "y": 1.02, "z": 1.0}
GRID_COLUMNS = 6
GRID_SPACING_X = 96.0
GRID_SPACING_Y = 142.0
SURFACE_OFFSET_X = 340.0
BASE_Y = 120.0

CARDS = [
    ("back", "T_Card_Back_ONOKO_V5_Alpha", "BACK"),
    ("major-00-fool", "T_Major_00_Fool_ONOKO_V5_Alpha", "00 Fool"),
    ("major-01-magician", "T_Major_01_Magician_ONOKO_V5_Alpha", "01 Magician"),
    ("major-02-high-priestess", "T_Major_02_High_Priestess_ONOKO_V5_Alpha", "02 High Priestess"),
    ("major-03-empress", "T_Major_03_Empress_ONOKO_V5_Alpha", "03 Empress"),
    ("major-04-emperor", "T_Major_04_Emperor_ONOKO_V5_Alpha", "04 Emperor"),
    ("major-05-hierophant", "T_Major_05_Hierophant_ONOKO_V5_Alpha", "05 Hierophant"),
    ("major-06-lovers", "T_Major_06_Lovers_ONOKO_V5_Alpha", "06 Lovers"),
    ("major-07-chariot", "T_Major_07_Chariot_ONOKO_V5_Alpha", "07 Chariot"),
    ("major-08-strength", "T_Major_08_Strength_ONOKO_V5_Alpha", "08 Strength"),
    ("major-09-hermit", "T_Major_09_Hermit_ONOKO_V5_Alpha", "09 Hermit"),
    ("major-10-wheel-of-fortune", "T_Major_10_Wheel_Of_Fortune_ONOKO_V5_Alpha", "10 Wheel"),
    ("major-11-justice", "T_Major_11_Justice_ONOKO_V5_Alpha", "11 Justice"),
    ("major-12-hanged-man", "T_Major_12_Hanged_Man_ONOKO_V5_Alpha", "12 Hanged Man"),
    ("major-13-death", "T_Major_13_Death_ONOKO_V5_Alpha", "13 Death"),
    ("major-14-temperance", "T_Major_14_Temperance_ONOKO_V5_Alpha", "14 Temperance"),
    ("major-15-devil", "T_Major_15_Devil_ONOKO_V5_Alpha", "15 Devil"),
    ("major-16-tower", "T_Major_16_Tower_ONOKO_V5_Alpha", "16 Tower"),
    ("major-17-star", "T_Major_17_Star_ONOKO_V5_Alpha", "17 Star"),
    ("major-18-moon", "T_Major_18_Moon_ONOKO_V5_Alpha", "18 Moon"),
    ("major-19-sun", "T_Major_19_Sun_ONOKO_V5_Alpha", "19 Sun"),
    ("major-20-judgement", "T_Major_20_Judgement_ONOKO_V5_Alpha", "20 Judgement"),
    ("major-21-world", "T_Major_21_World_ONOKO_V5_Alpha", "21 World"),
]


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_FULL_ALPHA_QA] " + message)
    print("[ONOKO_ARCANA_V5_FULL_ALPHA_QA] " + message)


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def save_asset(asset):
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


def asset_path(texture_name):
    return f"{TEXTURE_ROOT}/{texture_name}.{texture_name}"


def create_texture_material(name, texture_path, masked=True):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_path = f"{MATERIAL_DIR}/{name}"
    if unreal.load_asset(material_path):
        unreal.EditorAssetLibrary.delete_asset(material_path)

    material = asset_tools.create_asset(
        asset_name=name,
        package_path=MATERIAL_DIR,
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    if material is None:
        raise RuntimeError(f"Could not create material: {material_path}")

    texture = unreal.load_asset(texture_path)
    if texture is None:
        raise RuntimeError(f"Could not load texture: {texture_path}")

    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionTextureSample,
        -360,
        0,
    )
    sample.texture = texture

    try:
        material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        unreal.MaterialEditingLibrary.connect_material_property(
            sample,
            "RGB",
            unreal.MaterialProperty.MP_EMISSIVE_COLOR,
        )
    except Exception:
        unreal.MaterialEditingLibrary.connect_material_property(
            sample,
            "RGB",
            unreal.MaterialProperty.MP_BASE_COLOR,
        )

    if masked:
        unreal.MaterialEditingLibrary.connect_material_property(
            sample,
            "A",
            unreal.MaterialProperty.MP_OPACITY_MASK,
        )
        material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
        material.set_editor_property("opacity_mask_clip_value", 0.333)
    else:
        material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)

    material.set_editor_property("two_sided", True)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    save_asset(material)
    return material


def create_flat_material(name, color):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_path = f"{MATERIAL_DIR}/{name}"
    if unreal.load_asset(material_path):
        unreal.EditorAssetLibrary.delete_asset(material_path)

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
    try:
        material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
        unreal.MaterialEditingLibrary.connect_material_property(
            vector,
            "",
            unreal.MaterialProperty.MP_EMISSIVE_COLOR,
        )
    except Exception:
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


def disable_shadows(actor):
    component = getattr(actor, "static_mesh_component", None)
    if not component:
        return
    for prop, value in (
        ("cast_shadow", False),
        ("affect_dynamic_indirect_lighting", False),
        ("affect_distance_field_lighting", False),
    ):
        try:
            component.set_editor_property(prop, value)
        except Exception:
            pass
    try:
        component.set_cast_shadow(False)
    except Exception:
        pass


def spawn_plane(label, material, location, scale):
    plane = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
    if plane is None:
        raise RuntimeError("Could not load /Engine/BasicShapes/Plane")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        plane,
        unreal.Vector(*location),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(actor, label)
    actor.set_actor_scale3d(unreal.Vector(scale["x"], scale["y"], scale.get("z", 1.0)))
    actor.static_mesh_component.set_material(0, material)
    disable_shadows(actor)
    return actor


def spawn_camera_and_light():
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(0.0, -500.0, 600.0),
        unreal.Rotator(-70.0, 0.0, 0.0),
    )
    set_label(light, "V5_Full_QA_NoShadow_Key_Light")
    try:
        light.light_component.set_intensity(0.8)
    except Exception:
        pass

    camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(0.0, -980.0, 860.0),
        unreal.Rotator(-61.0, 0.0, 0.0),
    )
    set_label(camera, "V5_Full_QA_Alpha_Camera")
    camera.camera_component.set_field_of_view(35.0)
    try:
        camera.camera_component.set_editor_property("projection_mode", unreal.CameraProjectionMode.ORTHOGRAPHIC)
        camera.camera_component.set_editor_property("ortho_width", 1120.0)
    except Exception:
        pass
    return camera


def prepare_level():
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            unreal.EditorLevelLibrary.destroy_actor(actor)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)


def validate_import_result():
    if not os.path.exists(IMPORT_RESULT_PATH):
        raise RuntimeError(f"Missing import result: {IMPORT_RESULT_PATH}")
    with open(IMPORT_RESULT_PATH, "r", encoding="utf-8") as fp:
        payload = json.load(fp)
    if not payload.get("ok"):
        raise RuntimeError(f"Import result is not ok: {IMPORT_RESULT_PATH}")
    if payload.get("count") != len(CARDS):
        raise RuntimeError(f"Expected {len(CARDS)} imported cards, got {payload.get('count')}")
    return payload


def card_location(surface_x, index):
    row = index // GRID_COLUMNS
    col = index % GRID_COLUMNS
    x = surface_x + (col - (GRID_COLUMNS - 1) / 2.0) * GRID_SPACING_X
    y = BASE_Y + row * GRID_SPACING_Y
    return x, y, 8.0


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    import_payload = validate_import_result()
    prepare_level()

    checker = create_texture_material(
        "M_QA_V5Full_Checkerboard",
        "/Game/ONOKOArcana/QA/Textures/T_QA_Checkerboard_V1.T_QA_Checkerboard_V1",
        masked=False,
    )
    dark_table = create_flat_material("M_QA_V5Full_Dark_Table", (0.012, 0.017, 0.026, 1.0))

    card_materials = {}
    for card_id, texture_name, _label in CARDS:
        safe_name = texture_name.replace("T_", "M_QA_")
        card_materials[card_id] = create_texture_material(safe_name, asset_path(texture_name), masked=True)

    spawn_plane(
        "V5_Full_QA_Checkerboard_Surface",
        checker,
        (-SURFACE_OFFSET_X, BASE_Y + 180.0, 0.0),
        {"x": 6.7, "y": 6.1, "z": 1.0},
    )
    spawn_plane(
        "V5_Full_QA_Dark_Table_Surface",
        dark_table,
        (SURFACE_OFFSET_X, BASE_Y + 180.0, 0.0),
        {"x": 6.7, "y": 6.1, "z": 1.0},
    )

    for index, (card_id, _texture_name, label) in enumerate(CARDS):
        material = card_materials[card_id]
        left_location = card_location(-SURFACE_OFFSET_X, index)
        right_location = card_location(SURFACE_OFFSET_X, index)
        spawn_plane(f"V5_Full_Checker_{card_id}", material, left_location, CARD_PLANE_SCALE)
        spawn_plane(f"V5_Full_DarkTable_{card_id}", material, right_location, CARD_PLANE_SCALE)
    spawn_camera_and_light()
    unreal.EditorLevelLibrary.save_current_level()

    result = {
        "ok": True,
        "mapPath": MAP_PATH,
        "importResult": IMPORT_RESULT_PATH,
        "importCount": import_payload.get("count"),
        "cards": [{"id": card_id, "texture": asset_path(texture_name), "label": label} for card_id, texture_name, label in CARDS],
        "cardPlaneScale": CARD_PLANE_SCALE,
        "gridColumns": GRID_COLUMNS,
        "surfaces": ["checkerboard", "dark_table"],
        "shadowPolicy": "Static mesh card actors have cast shadows disabled for alpha/fringe QA.",
        "silhouettePolicy": "Use the user-approved taller V5 visible silhouette inside a 2:3 texture plane.",
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    log(f"Created map {MAP_PATH}")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_V5_FULL_ALPHA_QA] " + str(exc))
    print("[ONOKO_ARCANA_V5_FULL_ALPHA_QA_ERROR] " + str(exc), file=sys.stderr)
    raise
