import os
from pathlib import Path
from typing import Optional

from html2image import Html2Image
from jinja2 import Template

from ww.data.resonator import resonators
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateHtmlResonatorModel
from ww.tables.resonator import CalculatedResonatorsTable, ResonatorsTable
from ww.utils import get_url

ELEMENT_ICON_HOME_PATH = "./cache/v1/zh_tw/assets/element/icon"
RESONATOR_ICON_HOME_PATH = "./cache/v1/zh_tw/assets/resonator/icon"

TEMPLATE_RESONATOR_HTML_PATH = "./html/template/resonator.html"
TEMPLATE_RESONATOR_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/template"


def get_element_icon_fpath(element: str) -> Optional[str]:
    element_path = Path(ELEMENT_ICON_HOME_PATH) / f"{element}.png"
    if element_path.exists():
        return get_url(element_path)
    return None


def get_element_class_name(element: str) -> Optional[str]:
    elements = {
        _(ZhTwEnum.GLACIO): "glacio",
        _(ZhTwEnum.FUSION): "fusion",
        _(ZhTwEnum.ELECTRO): "electro",
        _(ZhTwEnum.AERO): "aero",
        _(ZhTwEnum.SPECTRO): "spectro",
        _(ZhTwEnum.HAVOC): "havoc",
    }
    return elements.get(element, None)


def get_resonator_icon_fpath(resonator_name: str) -> Optional[str]:
    element_path = Path(RESONATOR_ICON_HOME_PATH) / f"{resonator_name}.png"
    if element_path.exists():
        return get_url(element_path)
    return None


def get_html_template_resonator_model(
    resonator_id: str,
) -> Optional[TemplateHtmlResonatorModel]:
    if not resonator_id:
        return
    calculated_resonators_table = CalculatedResonatorsTable()
    calculated_resonator = calculated_resonators_table.get_calculated_resonator_model(
        resonator_id
    )
    if calculated_resonator is None:
        return

    resonators_table = ResonatorsTable()
    resonator = resonators_table.get_resonator_model(resonator_id)
    if resonator is None:
        return

    resonator_src = get_resonator_icon_fpath(resonator.name)
    if resonator_src is None:
        return

    resonator_data = resonators.get(resonator.name, "")
    resonator_element = resonator_data.element
    element_class_name = get_element_class_name(resonator_element)
    element_src = get_element_icon_fpath(resonator_element)

    template_html_model = TemplateHtmlResonatorModel(
        name=resonator.name,
        chain=resonator.resonance_chain,
        element=resonator_element,
        weapon_name=resonator.weapon_name,
        weapon_rank=resonator.weapon_rank,
        weapon_level=resonator.weapon_level,
        level=resonator.level,
        hp=calculated_resonator.calculated_hp,
        attack=calculated_resonator.calculated_atk,
        defense=calculated_resonator.calculated_def,
        crit_rate=calculated_resonator.calculated_crit_rate,
        crit_dmg=calculated_resonator.calculated_crit_dmg,
        energy_regen=calculated_resonator.calculated_energy_regen,
        resonance_skill_dmg_bonus=calculated_resonator.calculated_resonance_skill_dmg_bonus,
        basic_attack_dmg_bonus=calculated_resonator.calculated_basic_attack_dmg_bonus,
        heavy_attack_dmg_bonus=calculated_resonator.calculated_heavy_attack_dmg_bonus,
        resonance_liberation_dmg_bonus=calculated_resonator.calculated_resonance_liberation_dmg_bonus,
        healing_bonus=calculated_resonator.calculated_healing_bonus,
        physical_dmg_bonus=calculated_resonator.calculated_physical_dmg_bonus,
        glacio_dmg_bonus=calculated_resonator.calculated_glacio_dmg_bonus,
        fusion_dmg_bonus=calculated_resonator.calculated_fusion_dmg_bonus,
        electro_dmg_bonus=calculated_resonator.calculated_electro_dmg_bonus,
        aero_dmg_bonus=calculated_resonator.calculated_aero_dmg_bonus,
        spectro_dmg_bonus=calculated_resonator.calculated_spectro_dmg_bonus,
        havoc_dmg_bonus=calculated_resonator.calculated_havoc_dmg_bonus,
        physical_dmg_res=calculated_resonator.calculated_physical_dmg_res,
        glacio_dmg_res=calculated_resonator.calculated_glacio_dmg_res,
        fusion_dmg_res=calculated_resonator.calculated_fusion_dmg_res,
        electro_dmg_res=calculated_resonator.calculated_electro_dmg_res,
        aero_dmg_res=calculated_resonator.calculated_aero_dmg_res,
        spectro_dmg_res=calculated_resonator.calculated_spectro_dmg_res,
        havoc_dmg_res=calculated_resonator.calculated_havoc_dmg_res,
        normal_attack_lv=resonator.normal_attack_lv,
        resonance_skill_lv=resonator.resonance_skill_lv,
        resonance_liberation_lv=resonator.resonance_liberation_lv,
        forte_circuit_lv=resonator.forte_circuit_lv,
        inherent_skill_1=resonator.inherent_skill_1,
        inherent_skill_2=resonator.inherent_skill_2,
        resonator_src=resonator_src,
        element_class_name=element_class_name,
        element_src=element_src,
    )
    return template_html_model


def export_html_template_resonator_model_as_png(template_id: str, resonator_id: str):
    if not template_id or not resonator_id:
        return

    resonator = get_html_template_resonator_model(resonator_id)
    if resonator is None:
        return

    html_fpath = Path(TEMPLATE_RESONATOR_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    html_str = template.render(resonator=resonator, ZhTwEnum=ZhTwEnum, _=_)

    png_home_path = Path(TEMPLATE_RESONATOR_PNG_HOME_PATH) / template_id
    os.makedirs(png_home_path, exist_ok=True)
    png_fname = f"{resonator_id}.png"

    h2png = Html2Image(
        custom_flags=[
            "--no-sandbox",
            "--default-background-color=00000000",
            "--force-device-scale-factor=2",
        ],
        output_path=str(png_home_path),
        size=(1920, 276),  # (pixel, pixel)
        disable_logging=True,
    )
    h2png.screenshot(
        html_str=html_str,
        save_as=png_fname,
    )
