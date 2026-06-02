import json
import os

import unreal


PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULT_PATH = os.path.join(PROJECT_DIR, "Saved", "Phase1RuntimeMaterialsResult.json")
MATERIAL_DIR = "/Game/ONOKOArcana/Phase1/Materials"
CARD_MATERIAL_NAME = "M_Phase1_CardMasked_TextureParam"
CARD_MATERIAL_PATH = f"{MATERIAL_DIR}/{CARD_MATERIAL_NAME}"
DEFAULT_TEXTURE_PATH = "/Game/ONOKOArcana/Cards/Textures/V5Full/T_Card_Back_ONOKO_V5_Alpha.T_Card_Back_ONOKO_V5_Alpha"


def save_asset(asset):
    unreal.EditorAssetLibrary.save_loaded_asset(asset, only_if_is_dirty=False)


def set_property_if_available(obj, prop, value):
    try:
        obj.set_editor_property(prop, value)
        return True
    except Exception:
        return False


def normalize_card_material(material):
    texture = unreal.load_asset(DEFAULT_TEXTURE_PATH)
    if texture is None:
        raise RuntimeError(f"Could not load default texture: {DEFAULT_TEXTURE_PATH}")

    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material,
        unreal.MaterialExpressionTextureSampleParameter2D,
        -520,
        0,
    )
    sample.set_editor_property("parameter_name", "CardTexture")
    sample.texture = texture

    unreal.MaterialEditingLibrary.connect_material_property(
        sample,
        "RGB",
        unreal.MaterialProperty.MP_EMISSIVE_COLOR,
    )
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
    set_property_if_available(material, "shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    material.set_editor_property("opacity_mask_clip_value", 0.333)
    material.set_editor_property("two_sided", True)
    unreal.MaterialEditingLibrary.layout_material_expressions(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    save_asset(material)


def create_or_get_card_material():
    existing = unreal.load_asset(CARD_MATERIAL_PATH)
    if existing is not None:
        normalize_card_material(existing)
        return existing, False

    unreal.EditorAssetLibrary.make_directory(MATERIAL_DIR)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material = asset_tools.create_asset(
        asset_name=CARD_MATERIAL_NAME,
        package_path=MATERIAL_DIR,
        asset_class=unreal.Material,
        factory=unreal.MaterialFactoryNew(),
    )
    if material is None:
        raise RuntimeError(f"Could not create material: {CARD_MATERIAL_PATH}")

    normalize_card_material(material)
    return material, True


def main():
    material, created = create_or_get_card_material()
    shading_model = ""
    try:
        shading_model = str(material.get_editor_property("shading_model"))
    except Exception:
        pass
    result = {
        "ok": material is not None,
        "material": CARD_MATERIAL_PATH,
        "created": created,
        "blendMode": str(material.get_editor_property("blend_mode")) if material else "",
        "shadingModel": shading_model,
        "lightingPolicy": "Unlit Masked; texture RGB drives Emissive Color and alpha drives Opacity Mask.",
        "textureParameter": "CardTexture",
        "defaultTexture": DEFAULT_TEXTURE_PATH,
    }
    os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
    with open(RESULT_PATH, "w", encoding="utf-8") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


main()
