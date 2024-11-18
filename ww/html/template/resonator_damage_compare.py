import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple

from jinja2 import Template

from ww.data.resonator import resonators
from ww.html.template.damage import get_max_damage
from ww.html.template.export import export_to
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils.number import get_percentage_str, to_number_string

RESONATOR_DAMAGE_COMPARE_HTML_PATH = "./html/template/resonator_damage_compare.jinja2"
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
    height: int = 3000,
):
    if len(damage_distributions) == 0:
        return

    html_fpath = Path(RESONATOR_DAMAGE_COMPARE_HTML_PATH)
    if not html_fpath.exists():
        return

    home_path = get_export_resonator_damage_compare_home_path(id)
    os.makedirs(home_path, exist_ok=True)

    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    dmgs = _get_damages(damage_distributions)
    if max_damage is None:
        max_damage = get_max_damage(dmgs)
    base_damage = max(dmgs)

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
