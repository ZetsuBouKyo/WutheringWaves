from pathlib import Path
from typing import List

from jinja2 import Template

from ww.html.template.export import export_html_as_png
from ww.html.template.resonator import get_resonator_icon_fpath
from ww.locale import ZhTwEnum, _
from ww.model.template import (
    TemplateHtmlOutputMethodActionModel,
    TemplateHtmlOutputMethodModel,
    TemplateRowActionEnum,
    TemplateRowModel,
)
from ww.utils import get_local_file_url

TEMPLATE_OUTPUT_METHOD_HTML_PATH = "./html/template/output_method.jinja2"

E_ICON_FPATH = "./assets/actions/e.svg"
HOLD_LEFT_CLICK_ICON_FPATH = "./assets/actions/hold_left_click.svg"
LEFT_CLICK_ICON_FPATH = "./assets/actions/left_click.svg"
NUM_ICON_FPATH = "./assets/actions/num.svg"
Q_ICON_FPATH = "./assets/actions/q.svg"
R_ICON_FPATH = "./assets/actions/r.svg"
SHIFT_ICON_FPATH = "./assets/actions/shift.svg"
SPACE_ICON_FPATH = "./assets/actions/space.svg"
T_ICON_FPATH = "./assets/actions/t.svg"

RIGHT_ARROW_ICON_FPATH = "./assets/actions/right_arrow.svg"

action_icons = {
    TemplateRowActionEnum.ATTACK.value: get_local_file_url(LEFT_CLICK_ICON_FPATH),
    TemplateRowActionEnum.ATTACK_N.value: get_local_file_url(LEFT_CLICK_ICON_FPATH),
    TemplateRowActionEnum.AIR_ATTACK.value: get_local_file_url(LEFT_CLICK_ICON_FPATH),
    TemplateRowActionEnum.HEAVY_ATTACK.value: get_local_file_url(
        HOLD_LEFT_CLICK_ICON_FPATH
    ),
    TemplateRowActionEnum.AIR_HEAVY_ATTACK.value: get_local_file_url(
        HOLD_LEFT_CLICK_ICON_FPATH
    ),
    TemplateRowActionEnum.RESONANCE_SKILL.value: get_local_file_url(E_ICON_FPATH),
    TemplateRowActionEnum.RESONANCE_LIBERATION.value: get_local_file_url(R_ICON_FPATH),
    TemplateRowActionEnum.ECHO.value: get_local_file_url(Q_ICON_FPATH),
    TemplateRowActionEnum.OUTRO.value: get_local_file_url(NUM_ICON_FPATH),
    TemplateRowActionEnum.SWITCH.value: get_local_file_url(NUM_ICON_FPATH),
    TemplateRowActionEnum.SWITCH_AIR.value: get_local_file_url(NUM_ICON_FPATH),
    TemplateRowActionEnum.GRAPPLE.value: get_local_file_url(T_ICON_FPATH),
    TemplateRowActionEnum.DODGE.value: get_local_file_url(SHIFT_ICON_FPATH),
    TemplateRowActionEnum.JUMP.value: get_local_file_url(SPACE_ICON_FPATH),
}


def get_html_template_output_method_model(
    rows: List[TemplateRowModel],
) -> List[TemplateHtmlOutputMethodModel]:
    output_methods = []
    current_output_method = TemplateHtmlOutputMethodModel()
    for row in rows:
        action_name = row.action

        if (
            not action_name
            or action_name == TemplateRowActionEnum.COORDINATED_ATTACK.value
        ):
            continue

        if row.resonator_name != current_output_method.resonator_name:
            if not current_output_method.is_none():
                output_methods.append(current_output_method)

            resonator_name = row.resonator_name
            resonator_src = get_resonator_icon_fpath(resonator_name)

            current_output_method = TemplateHtmlOutputMethodModel()
            current_output_method.resonator_name = resonator_name
            current_output_method.resonator_src = resonator_src

        action_src = action_icons.get(action_name, "")
        action = TemplateHtmlOutputMethodActionModel(name=action_name, src=action_src)
        current_output_method.actions.append(action)

        comment = row.comment
        if comment:
            current_output_method.comments.append(comment)

    return output_methods


def export_html_template_output_method_model_as_png(
    template_id: str, rows: List[TemplateRowModel], height: int = 1000
):
    if not template_id or len(rows) == 0:
        return

    html_fpath = Path(TEMPLATE_OUTPUT_METHOD_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    output_methods = get_html_template_output_method_model(rows)

    right_arrow_src = get_local_file_url(RIGHT_ARROW_ICON_FPATH)
    html_str = template.render(
        output_methods=output_methods,
        ZhTwEnum=ZhTwEnum,
        _=_,
        right_arrow_src=right_arrow_src,
    )

    png_fname = f"{_(ZhTwEnum.OUTPUT_METHOD)}.png"

    export_html_as_png(template_id, png_fname, html_str, height)
