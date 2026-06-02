import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase0CardPlaneSceneResult.json")

TEXTURES = {
    "Fool": "/Game/ONOKOArcana/Cards/Textures/T_Major_00_Fool_V1_Alpha.T_Major_00_Fool_V1_Alpha",
    "Magician": "/Game/ONOKOArcana/Cards/Textures/T_Major_01_Magician_V1_Alpha.T_Major_01_Magician_V1_Alpha",
    "ChariotV2": "/Game/ONOKOArcana/Cards/Textures/T_Major_07_Chariot_V2_Alpha.T_Major_07_Chariot_V2_Alpha",
    "Back": "/Game/ONOKOArcana/Cards/Textures/T_CardBack_ONOKO_Production_V2_Alpha.T_CardBack_ONOKO_Production_V2_Alpha",
}

MATERIAL_DIR = "/Game/ONOKOArcana/Cards/Materials"
MAP_PATH = "/Game/ONOKOArcana/Maps/L_Phase0_CardPlane_Check"


def log(message):
    unreal.log("[ONOKO_ARCANA_PHASE0_SCENE] " + message)
    print("[ONOKO_ARCANA_PHASE0_SCENE] " + message)


def create_texture_material(name, texture_path):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_path = f"{MATERIAL_DIR}/{name}"

    existing = unreal.load_asset(material_path)
    if existing:
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
    material.set_editor_property("two_sided", True)
    material.set_editor_property("opacity_mask_clip_value", 0.333)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material, only_if_is_dirty=False)
    return material


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def spawn_card(label, material, x, y):
    plane = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
    if plane is None:
        raise RuntimeError("Could not load /Engine/BasicShapes/Plane")

    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        plane,
        unreal.Vector(x, y, 2.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(actor, f"Card_2x3_{label}")
    actor.set_actor_scale3d(unreal.Vector(0.70, 1.05, 1.0))
    actor.static_mesh_component.set_material(0, material)
    return actor


def spawn_text(label, text, x, y):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TextRenderActor,
        unreal.Vector(x, y, 4.0),
        unreal.Rotator(90.0, 0.0, 0.0),
    )
    set_label(actor, label)
    comp = actor.text_render
    comp.set_text(text)
    comp.set_world_size(18.0)
    comp.set_text_render_color(unreal.Color(125, 205, 255, 255))
    return actor


def spawn_table():
    plane = unreal.load_asset("/Engine/BasicShapes/Plane.Plane")
    material = unreal.load_asset("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial")
    table = unreal.EditorLevelLibrary.spawn_actor_from_object(
        plane,
        unreal.Vector(0.0, 0.0, 0.0),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    set_label(table, "Phase0_Dark_Table_Reference")
    table.set_actor_scale3d(unreal.Vector(4.8, 3.4, 1.0))
    if material:
        table.static_mesh_component.set_material(0, material)
    return table


def spawn_camera_and_light():
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(-180.0, -120.0, 340.0),
        unreal.Rotator(-58.0, -20.0, 22.0),
    )
    set_label(light, "Phase0_Key_Light")

    camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(0.0, -360.0, 340.0),
        unreal.Rotator(-58.0, 0.0, 0.0),
    )
    set_label(camera, "Phase0_Table_Camera")
    camera.camera_component.set_field_of_view(42.0)
    return camera


def prepare_level():
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            unreal.EditorLevelLibrary.destroy_actor(actor)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)

    prepare_level()

    materials = {
        "Fool": create_texture_material("M_Phase0_Major_00_Fool", TEXTURES["Fool"]),
        "Magician": create_texture_material("M_Phase0_Major_01_Magician", TEXTURES["Magician"]),
        "ChariotV2": create_texture_material("M_Phase0_Major_07_Chariot_V2", TEXTURES["ChariotV2"]),
        "Back": create_texture_material("M_Phase0_CardBack_ONOKO_Production_V2", TEXTURES["Back"]),
    }

    spawn_table()
    spawn_card("Fool", materials["Fool"], -95.0, 0.0)
    spawn_card("Magician", materials["Magician"], 0.0, 0.0)
    spawn_card("ChariotV2", materials["ChariotV2"], 95.0, 0.0)
    spawn_card("Back", materials["Back"], 0.0, 125.0)
    spawn_text("Phase0_Label_Fronts", "2:3 card planes / 1024x1536 textures", 0.0, -95.0)
    spawn_text("Phase0_Label_Back", "card back reference", 0.0, 215.0)
    spawn_camera_and_light()
    unreal.EditorLevelLibrary.save_current_level()

    result = {
        "ok": True,
        "mapPath": MAP_PATH,
        "materials": [f"{MATERIAL_DIR}/{name}" for name in [
            "M_Phase0_Major_00_Fool",
            "M_Phase0_Major_01_Magician",
            "M_Phase0_Major_07_Chariot_V2",
            "M_Phase0_CardBack_ONOKO_Production_V2",
        ]],
        "cardPlaneScale": {"x": 0.70, "y": 1.05, "aspect": "2:3"},
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    log(f"Created map {MAP_PATH}")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_PHASE0_SCENE] " + str(exc))
    print("[ONOKO_ARCANA_PHASE0_SCENE_ERROR] " + str(exc), file=sys.stderr)
    raise
