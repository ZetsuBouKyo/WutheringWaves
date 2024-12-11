import os
from pathlib import Path
from typing import List

from ww.html.template.export import TEMPLATE_PNG_HOME_PATH, export_to_template
from ww.html.template.resonator import get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model import SkillBaseAttrEnum
from ww.model.template import CalculatedTemplateRowModel
from ww.utils import get_jinja2_template
from ww.utils.number import to_number_string, to_trimmed_number_string

TEMPLATE_DETAILED_CALCULATION_HTML_PATH = "./html/template/detailed_calculation.jinja2"


def export_detailed_calculation_as_png(
    template_id: str, rows: List[CalculatedTemplateRowModel], i: int, j: int
):
    if not template_id:
        return

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    template = get_jinja2_template(TEMPLATE_DETAILED_CALCULATION_HTML_PATH)

    _i = i - 1
    _rows = rows[_i:j]
    height = 200
    for row in rows:
        if len(row.buffs) > 0:
            height += 80 + 24 * (len(row.buffs) + 2)
        if (
            not row.real_dmg_crit
            or not row.real_dmg_no_crit
            or not row.damage_crit
            or not row.damage_no_crit
        ):
            height += 48

    html_str = template.render(
        template_id=template_id,
        i_0_indexed=_i,
        rows=_rows,
        get_resonator_icon_fpath=get_resonator_icon_fpath,
        to_number_string=to_number_string,
        to_trimmed_number_string=to_trimmed_number_string,
        SkillBaseAttrEnum=SkillBaseAttrEnum,
        ZhTwEnum=ZhTwEnum,
        _=_,
    )

    suffix = f"{_(ZhTwEnum.NO)}{i}-{j}{_(ZhTwEnum.ROW)}"

    fname = f"{_(ZhTwEnum.DETAILED_CALCULATION)}-{suffix}.png"
    export_to_template(template_id, fname, html_str, height=height)
