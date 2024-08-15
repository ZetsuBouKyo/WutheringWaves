from pathlib import Path
from typing import Optional

from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateHtmlResonatorModel
from ww.tables.resonator import CalculatedResonatorsTable, ResonatorsTable
from ww.utils import get_url

ELEMENT_ICON_HOME_PATH = "./cache/v1/zh_tw/assets/element/icon"
RESONATOR_ICON_HOME_PATH = "./cache/v1/zh_tw/assets/resonator/icon"


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


def get_resonator_example() -> TemplateHtmlResonatorModel:
    resonator_name = "凌陽"
    resonator_src = get_resonator_icon_fpath(resonator_name)

    element = _(ZhTwEnum.GLACIO)
    element_class_name = get_element_class_name(element)
    element_src = get_element_icon_fpath(element)

    return TemplateHtmlResonatorModel(
        name=resonator_name,
        chain="1",
        element=element,
        weapon_name="擎淵怒濤",
        weapon_rank="1",
        weapon_level="90",
        level="90",
        hp="15000",
        attack="2000",
        defense="1000",
        crit_rate="50.00%",
        crit_dmg="220.00%",
        energy_regen="120.00%",
        resonance_skill_dmg_bonus="100.00%",
        basic_attack_dmg_bonus="8.00%",
        heavy_attack_dmg_bonus="8.00%",
        resonance_liberation_dmg_bonus="8.00%",
        healing_bonus="0.00%",
        physical_dmg_bonus="0.00%",
        glacio_dmg_bonus="70.00%",
        fusion_dmg_bonus="0.00%",
        electro_dmg_bonus="0.00%",
        aero_dmg_bonus="0.00%",
        spectro_dmg_bonus="0.00%",
        havoc_dmg_bonus="0.00%",
        physical_dmg_res="0.00%",
        glacio_dmg_res="0.00%",
        fusion_dmg_res="0.00%",
        electro_dmg_res="0.00%",
        aero_dmg_res="0.00%",
        spectro_dmg_res="0.00%",
        havoc_dmg_res="0.00%",
        normal_attack_lv="1",
        resonance_skill_lv="1",
        forte_circuit_lv="1",
        resonance_liberation_lv="1",
        intro_skill_lv="1",
        inherent_skill_1="✓",
        inherent_skill_2="✓",
        element_src=element_src,
        element_class_name=element_class_name,
        resonator_src=resonator_src,
    )


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

    template_html_model = TemplateHtmlResonatorModel(
        name=resonator.name,
        chain=resonator.resonance_chain,
        element="",
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
        element_class_name="",
        element_src="",
    )
    print(template_html_model)
