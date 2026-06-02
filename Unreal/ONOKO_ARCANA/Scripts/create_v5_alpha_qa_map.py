import json
import os
import sys

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "V5AlphaQAMapResult.json")

MAP_PATH = "/Game/ONOKOArcana/Maps/L_QA_CardAlpha_V5_Check"
MATERIAL_DIR = "/Game/ONOKOArcana/QA/Materials"

TEXTURES = {
    "MagicianV5": "/Game/ONOKOArcana/Cards/Textures/V5/T_Major_01_Magician_ONOKO_V5_Clean_Alpha.T_Major_01_Magician_ONOKO_V5_Clean_Alpha",
    "Checker": "/Game/ONOKOArcana/QA/Textures/T_QA_Checkerboard_V1.T_QA_Checkerboard_V1",
}

# Plane keeps the full texture canvas at 2:3. The visible V5 card silhouette is
# intentionally taller/narrower inside the transparent canvas.
CARD_PLANE_SCALE = {"x": 1.40, "y": 2.10, "z": 1.0}


def log(message):
    unreal.log("[ONOKO_ARCANA_V5_ALPHA_QA] " + message)
    print("[ONOKO_ARCANA_V5_ALPHA_QA] " + message)


def set_label(actor, label):
    try:
        actor.set_actor_label(label)
    except Exception:
        pass


def save_asset(asset):
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


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


def spawn_text(label, text, location, size=11.0):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TextRenderActor,
        unreal.Vector(*location),
        unreal.Rotator(90.0, 0.0, 0.0),
    )
    set_label(actor, label)
    comp = actor.text_render
    comp.set_text(text)
    comp.set_world_size(size)
    comp.set_text_render_color(unreal.Color(190, 225, 255, 255))
    return actor


def spawn_camera_and_light():
    light = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight,
        unreal.Vector(0.0, -180.0, 320.0),
        unreal.Rotator(-70.0, 0.0, 0.0),
    )
    set_label(light, "V5_QA_NoShadow_Key_Light")
    try:
        light.light_component.set_intensity(1.0)
    except Exception:
        pass

    camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(0.0, -330.0, 275.0),
        unreal.Rotator(-58.0, 0.0, 0.0),
    )
    set_label(camera, "V5_QA_Alpha_Camera")
    camera.camera_component.set_field_of_view(35.0)
    try:
        camera.camera_component.set_editor_property("projection_mode", unreal.CameraProjectionMode.ORTHOGRAPHIC)
        camera.camera_component.set_editor_property("ortho_width", 320.0)
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


def main():
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    prepare_level()

    materials = {
        "Checker": create_texture_material("M_QA_Checkerboard_V1", TEXTURES["Checker"], masked=False),
        "MagicianV5": create_texture_material("M_QA_V5_Major_01_Magician_Clean", TEXTURES["MagicianV5"], masked=True),
    }

    spawn_plane("V5_QA_Checkerboard_Background", materials["Checker"], (0.0, 25.0, 0.0), {"x": 4.4, "y": 5.8, "z": 1.0})
    spawn_plane("V5_QA_Card_01_Magician_Clean", materials["MagicianV5"], (0.0, 0.0, 4.0), CARD_PLANE_SCALE)
    spawn_text("V5_QA_Label_Title", "V5 clean-start sample / original tall silhouette", (0.0, -200.0, 8.0), 12.0)
    spawn_text("V5_QA_Label_Note", "2:3 texture plane, shadows disabled, checkerboard alpha check", (0.0, 206.0, 8.0), 10.0)
    spawn_camera_and_light()
    unreal.EditorLevelLibrary.save_current_level()

    result = {
        "ok": True,
        "mapPath": MAP_PATH,
        "materials": {key: f"{MATERIAL_DIR}/{value.get_name()}" for key, value in materials.items()},
        "textures": TEXTURES,
        "cardPlaneScale": CARD_PLANE_SCALE,
        "sourceAlphaBbox": [103, 35, 921, 1504],
        "silhouettePolicy": "Use the original V5 taller visible silhouette; do not normalize to the older wider bbox.",
        "shadowPolicy": "Static mesh card actor has cast shadows disabled for alpha-only QA.",
    }
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    log(f"Created map {MAP_PATH}")
    log(f"Result: {RESULT_PATH}")


try:
    main()
except Exception as exc:
    unreal.log_error("[ONOKO_ARCANA_V5_ALPHA_QA] " + str(exc))
    print("[ONOKO_ARCANA_V5_ALPHA_QA_ERROR] " + str(exc), file=sys.stderr)
    raise
