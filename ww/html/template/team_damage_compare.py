import os
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple

from ww.data.resonator import resonators
from ww.html.template.damage import get_max_damage
from ww.html.template.export import export_to
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils import get_jinja2_template
from ww.utils.number import get_percentage_str, to_number_string

TEAM_DAMAGE_COMPARE_HTML_PATH = "./html/template/team_damage_compare.jinja2"
TEAM_DAMAGE_COMPARE_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/compare_team_damage"
MAX_DAMAGE = 1500000


def _get_all_dps(
    damage_distributions: List[Tuple[str, TemplateDamageDistributionModel]],
) -> List[Decimal]:
    all_dps = []
    for _, damage_distribution in damage_distributions:
        all_dps.append(damage_distribution.get_max_dps())
    return all_dps


def get_export_team_damage_compare_home_path(
    id: str, home_path: str = TEAM_DAMAGE_COMPARE_PNG_HOME_PATH
) -> Optional[Path]:
    if not id:
        return None
    return Path(home_path) / id


def export_team_damage_compare_as_png(
    id: str,
    damage_distributions: List[Tuple[str, TemplateDamageDistributionModel]],
    max_dps: Optional[int] = None,
):
    if len(damage_distributions) == 0:
        return

    template = get_jinja2_template(TEAM_DAMAGE_COMPARE_HTML_PATH)

    damage_distributions = sorted(
        damage_distributions, key=lambda d: d[1].get_max_dps(), reverse=True
    )

    home_path = get_export_team_damage_compare_home_path(id)
    os.makedirs(home_path, exist_ok=True)

    all_dps = _get_all_dps(damage_distributions)
    if max_dps is None:
        max_dps = get_max_damage(
            all_dps, default_max_damage=Decimal(35000), tick=Decimal(5000)
        )
    base_dps = max(all_dps)

    height = 80 + 100 * len(all_dps) + 120

    html_str = template.render(
        damage_distributions=damage_distributions,
        resonators=resonators,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        base_dps=base_dps,
        max_dps=max_dps,
        _=_,
    )

    name = f"{_(ZhTwEnum.DAMAGE_COMPARE)}"

    fname = f"{name}.png"
    export_to(home_path, fname, html_str, height=height)
