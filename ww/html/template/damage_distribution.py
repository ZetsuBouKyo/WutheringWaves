import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

from ww.data.resonator import resonators
from ww.html.template.damage import get_max_damage
from ww.html.template.export import TEMPLATE_PNG_HOME_PATH, export_to_template
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.buff import SkillBonusTypeEnum
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.template import TemplateDamageDistributionModel
from ww.utils import get_jinja2_template
from ww.utils.number import get_percentage_str, to_number_string

TEMPLATE_TEAM_DAMAGE_DISTRIBUTION_HTML_PATH = (
    "./html/template/team_damage_distribution.jinja2"
)

TEMPLATE_RESONATOR_SKILL_DAMAGE_DISTRIBUTION_HTML_PATH = (
    "./html/template/resonator_skill_damage_distribution.jinja2"
)


def _get_resonator_damages(
    damage_distribution: TemplateDamageDistributionModel,
) -> List[Decimal]:
    damages = []
    for _, resonator in damage_distribution.resonators.items():
        damages.append(resonator.damage)
    return damages


def export_resonator_skill_damage_distribution_as_png(
    resonator_name: str,
    damage_distribution: TemplateDamageDistributionModel,
    skill_enum: Union[SkillBonusTypeEnum, ResonatorSkillTypeEnum],
    max_damage: Optional[int] = None,
    suffix: Optional[str] = None,
):
    template_id = damage_distribution.template_id
    if not template_id:
        return

    template = get_jinja2_template(
        TEMPLATE_RESONATOR_SKILL_DAMAGE_DISTRIBUTION_HTML_PATH
    )

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    resonator_damage_distribution = damage_distribution.resonators.get(
        resonator_name, None
    )
    if resonator_damage_distribution is None:
        return

    base_damage = Decimal("0.0")
    for e in skill_enum:
        base_damage += resonator_damage_distribution.get_damage(e.name.lower())

    dmgs = [base_damage]
    if max_damage is None:
        max_damage = get_max_damage(dmgs)

    if base_damage == Decimal("0.0"):
        return

    html_str = template.render(
        damage_distribution=damage_distribution,
        resonator_damage_distribution=resonator_damage_distribution,
        resonators=resonators,
        resonator_name=resonator_name,
        skill_enum=skill_enum,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        base_damage=base_damage,
        max_damage=max_damage,
        _=_,
    )

    name = f"{resonator_name}{_(ZhTwEnum.DAMAGE_DISTRIBUTION)}"
    if suffix:
        name = f"{name}-{suffix}"

    png_fname = f"{name}.png"
    export_to_template(template_id, png_fname, html_str, height=800)


def export_team_damage_distribution_as_png(
    resonator_names: List[str],
    damage_distribution: TemplateDamageDistributionModel,
    max_damage: Optional[int] = None,
    suffix: Optional[str] = None,
):
    template_id = damage_distribution.template_id
    if not template_id:
        return

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    template = get_jinja2_template(TEMPLATE_TEAM_DAMAGE_DISTRIBUTION_HTML_PATH)

    if max_damage is None:
        max_damage = get_max_damage(_get_resonator_damages(damage_distribution))

    html_str = template.render(
        damage_distributions=[damage_distribution],
        resonators=resonators,
        resonator_names=resonator_names,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        max_damage=max_damage,
        _=_,
    )

    name = f"{_(ZhTwEnum.TEAM)}{_(ZhTwEnum.DAMAGE_DISTRIBUTION)}"
    if suffix:
        name = f"{name}-{suffix}"

    png_fname = f"{name}.png"
    export_to_template(template_id, png_fname, html_str, height=500)
