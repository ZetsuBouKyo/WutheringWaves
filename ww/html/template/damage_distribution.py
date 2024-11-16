import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional

from jinja2 import Template

from ww.data.resonator import resonators
from ww.html.template.damage import get_max_damage
from ww.html.template.export import TEMPLATE_PNG_HOME_PATH, export_to_template
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils.number import get_percentage_str, to_number_string

TEMPLATE_TEAM_DAMAGE_DISTRIBUTION_HTML_PATH = (
    "./html/template/team_damage_distribution.jinja2"
)


def _get_resonator_damages(
    damage_distribution: TemplateDamageDistributionModel,
) -> List[Decimal]:
    damages = []
    for _, resonator in damage_distribution.resonators.items():
        damages.append(resonator.damage)
    return damages


def export_team_damage_distribution_as_png(
    resonator_names: List[str],
    damage_distribution: TemplateDamageDistributionModel,
    max_damage: Optional[int] = None,
    suffix: Optional[str] = None,
):
    template_id = damage_distribution.template_id
    if not template_id:
        return

    html_fpath = Path(TEMPLATE_TEAM_DAMAGE_DISTRIBUTION_HTML_PATH)
    if not html_fpath.exists():
        return

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

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

    name = f"{_(ZhTwEnum.DAMAGE_DISTRIBUTION)}"
    if suffix:
        name = f"{name}-{suffix}"

    png_fname = f"{name}.png"
    export_to_template(template_id, png_fname, html_str, height=320)
