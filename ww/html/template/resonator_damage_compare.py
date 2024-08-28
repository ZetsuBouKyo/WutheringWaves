import os
from pathlib import Path
from typing import List, Tuple

from jinja2 import Template

from ww.data.resonator import resonators
from ww.html.template.export import export_to
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils.number import get_percentage_str, to_number_string

RESONATOR_DAMAGE_COMPARE_HTML_PATH = "./html/template/resonator_damage_compare.jinja2"
RESONATOR_DAMAGE_COMPARE_PNG_HOME_PATH = (
    "./cache/v1/zh_tw/output/png/compare_resonator_damage"
)
MAX_DAMAGE = 1000000


def export_compare_resonator_damage_as_png(
    id: str,
    damage_distributions: List[Tuple[str, TemplateDamageDistributionModel]],
    max_damage: int = MAX_DAMAGE,
    height: int = 2000,
):
    if len(damage_distributions) == 0:
        return

    html_fpath = Path(RESONATOR_DAMAGE_COMPARE_HTML_PATH)
    if not html_fpath.exists():
        return

    home_path = Path(RESONATOR_DAMAGE_COMPARE_PNG_HOME_PATH) / id
    os.makedirs(home_path, exist_ok=True)

    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    html_str = template.render(
        damage_distributions=damage_distributions,
        resonators=resonators,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        max_damage=max_damage,
        _=_,
    )

    name = f"{_(ZhTwEnum.DAMAGE_COMPARE)}"

    fname = f"{name}.png"
    export_to(home_path, fname, html_str, height=height)
