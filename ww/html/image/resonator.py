from pathlib import Path
from typing import Optional

from ww.crud.resonator import ELEMENT_ICON_HOME_PATH, RESONATOR_ICON_HOME_PATH
from ww.html.image.export import export_to_template
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateHtmlResonatorModel
from ww.tables.resonator import (
    CalculatedResonatorsTable,
    ResonatorsTable,
    get_resonator_information,
)
from ww.utils import get_jinja2_template, get_local_file_url
from ww.utils.number import to_number_string, to_percentage_str

TEMPLATE_RESONATOR_HTML_PATH = "./html/image/resonator.jinja2"


def get_element_icon_fpath(element: str) -> Optional[str]:
    element_path = Path(ELEMENT_ICON_HOME_PATH) / f"{element}.png"
    if element_path.exists():
        return get_local_file_url(element_path)
    return None


def get_element_icon_url(element: str) -> Optional[str]:
    return f"/assets/element/icon/{element}.png"


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
        return get_local_file_url(element_path)
    return None


def get_resonator_icon_url(resonator_name: str) -> str:
    return f"/assets/resonator/icon/{resonator_name}.png"


def merge_resonator_model(
    resonator_id: str,
    resonators_table: ResonatorsTable,
    calculated_resonators_table: CalculatedResonatorsTable,
    is_docs: bool = False,
) -> Optional[TemplateHtmlResonatorModel]:
    calculated_resonator = calculated_resonators_table.get_calculated_resonator_model(
        resonator_id
    )
    if calculated_resonator is None:
        return

    resonator = resonators_table.get_resonator_model(resonator_id)
    if resonator is None:
        return

    if is_docs:
        resonator_src = get_resonator_icon_url(resonator.name)
    else:
        resonator_src = get_resonator_icon_fpath(resonator.name)
    if resonator_src is None:
        return

    resonator_information = get_resonator_information(resonator.name)
    if not resonator_information:
        return
    resonator_element = resonator_information.element
    element_en = get_element_class_name(resonator_element)

    if is_docs:
        element_src = get_element_icon_url(resonator_element)
    else:
        element_src = get_element_icon_fpath(resonator_element)

    template_html_model = TemplateHtmlResonatorModel(
        resonator_src=str(resonator_src),
        element=str(resonator_element),
        element_src=str(element_src),
        element_en=str(element_en),
        name=str(resonator.name),
        chain=str(resonator.resonance_chain),
        weapon_name=str(resonator.weapon_name),
        weapon_rank=str(resonator.weapon_rank),
        weapon_level=str(resonator.weapon_level),
        level=str(resonator.level),
        hp=to_number_string(calculated_resonator.calculated_hp),
        attack=to_number_string(calculated_resonator.calculated_atk),
        defense=to_number_string(calculated_resonator.calculated_def),
        crit_rate=to_percentage_str(calculated_resonator.calculated_crit_rate),
        crit_dmg=to_percentage_str(calculated_resonator.calculated_crit_dmg),
        energy_regen=to_percentage_str(calculated_resonator.calculated_energy_regen),
        resonance_skill_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_resonance_skill_dmg_bonus
        ),
        basic_attack_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_basic_attack_dmg_bonus
        ),
        heavy_attack_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_heavy_attack_dmg_bonus
        ),
        resonance_liberation_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_resonance_liberation_dmg_bonus
        ),
        echo_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_echo_dmg_bonus
        ),
        healing_bonus=to_percentage_str(calculated_resonator.calculated_healing_bonus),
        physical_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_physical_dmg_bonus
        ),
        glacio_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_glacio_dmg_bonus
        ),
        fusion_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_fusion_dmg_bonus
        ),
        electro_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_electro_dmg_bonus
        ),
        aero_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_aero_dmg_bonus
        ),
        spectro_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_spectro_dmg_bonus
        ),
        havoc_dmg_bonus=to_percentage_str(
            calculated_resonator.calculated_havoc_dmg_bonus
        ),
        physical_dmg_res=to_percentage_str(
            calculated_resonator.calculated_physical_dmg_res
        ),
        glacio_dmg_res=to_percentage_str(
            calculated_resonator.calculated_glacio_dmg_res
        ),
        fusion_dmg_res=to_percentage_str(
            calculated_resonator.calculated_fusion_dmg_res
        ),
        electro_dmg_res=to_percentage_str(
            calculated_resonator.calculated_electro_dmg_res
        ),
        aero_dmg_res=to_percentage_str(calculated_resonator.calculated_aero_dmg_res),
        spectro_dmg_res=to_percentage_str(
            calculated_resonator.calculated_spectro_dmg_res
        ),
        havoc_dmg_res=to_percentage_str(calculated_resonator.calculated_havoc_dmg_res),
        normal_attack_lv=str(resonator.normal_attack_lv),
        resonance_skill_lv=str(resonator.resonance_skill_lv),
        resonance_liberation_lv=str(resonator.resonance_liberation_lv),
        forte_circuit_lv=str(resonator.forte_circuit_lv),
        intro_skill_lv=str(resonator.intro_skill_lv),
        inherent_skill_1=str(resonator.inherent_skill_1),
        inherent_skill_2=str(resonator.inherent_skill_2),
        echo_hp=to_number_string(calculated_resonator.echo_hp),
        echo_hp_p=to_percentage_str(calculated_resonator.echo_hp_p),
        echo_atk=to_number_string(calculated_resonator.echo_atk),
        echo_atk_p=to_percentage_str(calculated_resonator.echo_atk_p),
        echo_def=to_number_string(calculated_resonator.echo_def),
        echo_def_p=to_percentage_str(calculated_resonator.echo_def_p),
        echo_crit_rate=to_percentage_str(calculated_resonator.echo_crit_rate),
        echo_crit_dmg=to_percentage_str(calculated_resonator.echo_crit_dmg),
        echo_energy_regen=to_percentage_str(calculated_resonator.echo_energy_regen),
        echo_sonata_1=calculated_resonator.echo_sonata_1,
        echo_sonata_2=calculated_resonator.echo_sonata_2,
        echo_sonata_3=calculated_resonator.echo_sonata_3,
        echo_sonata_4=calculated_resonator.echo_sonata_4,
        echo_sonata_5=calculated_resonator.echo_sonata_5,
        echo_resonance_skill_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_resonance_skill_dmg_bonus
        ),
        echo_basic_attack_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_basic_attack_dmg_bonus
        ),
        echo_heavy_attack_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_heavy_attack_dmg_bonus
        ),
        echo_resonance_liberation_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_resonance_liberation_dmg_bonus
        ),
        echo_coordinated_attack_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_coordinated_attack_dmg_bonus
        ),
        echo_echo_dmg_bonus=to_percentage_str(calculated_resonator.echo_echo_dmg_bonus),
        echo_healing_bonus=to_percentage_str(calculated_resonator.echo_healing_bonus),
        echo_glacio_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_glacio_dmg_bonus
        ),
        echo_fusion_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_fusion_dmg_bonus
        ),
        echo_electro_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_electro_dmg_bonus
        ),
        echo_aero_dmg_bonus=to_percentage_str(calculated_resonator.echo_aero_dmg_bonus),
        echo_spectro_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_spectro_dmg_bonus
        ),
        echo_havoc_dmg_bonus=to_percentage_str(
            calculated_resonator.echo_havoc_dmg_bonus
        ),
    )
    return template_html_model


def get_html_template_resonator_model(
    resonator_id: str,
) -> Optional[TemplateHtmlResonatorModel]:
    if not resonator_id:
        return
    calculated_resonators_table = CalculatedResonatorsTable()
    resonators_table = ResonatorsTable()

    model = merge_resonator_model(
        resonator_id, resonators_table, calculated_resonators_table
    )
    return model


def export_html_template_resonator_model_as_png(template_id: str, resonator_id: str):
    if not template_id or not resonator_id:
        return

    resonator = get_html_template_resonator_model(resonator_id)
    if resonator is None:
        return

    template = get_jinja2_template(TEMPLATE_RESONATOR_HTML_PATH)

    html_str = template.render(
        resonator=resonator, to_percentage_str=to_percentage_str, ZhTwEnum=ZhTwEnum, _=_
    )
    png_fname = f"{resonator_id}.png"

    export_to_template(template_id, png_fname, html_str, 400)
