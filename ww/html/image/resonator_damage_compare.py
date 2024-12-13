import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple

from ww.data.resonator import resonators
from ww.html.image.damage import get_max_damage
from ww.html.image.export import export_to
from ww.html.image.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils import get_jinja2_template
from ww.utils.number import get_percentage_str, to_number_string

RESONATOR_DAMAGE_COMPARE_HTML_PATH = "./html/image/resonator_damage_compare.jinja2"
RESONATOR_DAMAGE_COMPARE_PNG_HOME_PATH = (
    "./cache/v1/zh_tw/output/png/compare_resonator_damage"
)
MAX_DAMAGE = 1500000


def _get_damages(
    damage_distributions: List[Tuple[str, TemplateDamageDistributionModel]],
) -> List[Decimal]:
    damages = []
    for _, damage_distribution in damage_distributions:
        for _, resonator in damage_distribution.resonators.items():
            damages.append(resonator.damage)
    return damages


def get_export_resonator_damage_compare_home_path(
    id: str, home_path: str = RESONATOR_DAMAGE_COMPARE_PNG_HOME_PATH
) -> Optional[Path]:
    if not id:
        return None
    return Path(home_path) / id


def export_resonator_damage_compare_as_png(
    id: str,
    damage_distributions: List[Tuple[str, TemplateDamageDistributionModel]],
    max_damage: Optional[int] = None,
):
    if len(damage_distributions) == 0:
        return

    template = get_jinja2_template(RESONATOR_DAMAGE_COMPARE_HTML_PATH)

    home_path = get_export_resonator_damage_compare_home_path(id)
    os.makedirs(home_path, exist_ok=True)

    dmgs = _get_damages(damage_distributions)
    if max_damage is None:
        max_damage = get_max_damage(dmgs)
    base_damage = max(dmgs)

    height = 80 + 100 * len(dmgs) + 100

    html_str = template.render(
        damage_distributions=damage_distributions,
        resonators=resonators,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        base_damage=base_damage,
        max_damage=max_damage,
        _=_,
    )

    name = f"{_(ZhTwEnum.DAMAGE_COMPARE)}"

    fname = f"{name}.png"
    export_to(home_path, fname, html_str, height=height)
