import os
from pathlib import Path
from typing import List

from jinja2 import Template

from ww.data.resonator import resonators
from ww.html.template.export import TEMPLATE_PNG_HOME_PATH, export_to_template
from ww.html.template.resonator import get_element_class_name, get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel
from ww.utils.number import get_percentage_str

TEMPLATE_DAMAGE_DISTRIBUTIONS_HTML_PATH = "./html/template/damage_distributions.jinja2"
MAX_DAMAGE = 1000000


def export_damage_distribution_as_png(
    resonator_names: List[str],
    damage_distribution: TemplateDamageDistributionModel,
    max_damage: int = MAX_DAMAGE,
):
    template_id = damage_distribution.template_id
    if not template_id:
        return

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    html_fpath = Path(TEMPLATE_DAMAGE_DISTRIBUTIONS_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    html_str = template.render(
        damage_distributions=[damage_distribution],
        resonators=resonators,
        resonator_names=resonator_names,
        ZhTwEnum=ZhTwEnum,
        get_element_class_name=get_element_class_name,
        get_percentage_str=get_percentage_str,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        max_damage=max_damage,
        _=_,
    )

    html_str_path = home_path / f"{_(ZhTwEnum.DAMAGE_DISTRIBUTION)}.html"
    with html_str_path.open(mode="w", encoding="utf-8") as fp:
        fp.write(html_str)

    fname = f"{_(ZhTwEnum.DAMAGE_DISTRIBUTION)}.png"
    export_to_template(template_id, fname, html_str, height=276)
