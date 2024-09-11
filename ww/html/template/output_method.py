import os
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Optional, Union

from jinja2 import Template

from ww.crud.template import get_template
from ww.html.template.export import export_to, export_to_template
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


def get_html_template_output_methods(
    rows: List[TemplateRowModel],
    labels: Optional[List[str]] = None,
) -> Dict[str, List[TemplateHtmlOutputMethodModel]]:
    output_methods: Dict[str, List[TemplateHtmlOutputMethodModel]] = {}
    current_output_methods: Dict[str, TemplateHtmlOutputMethodModel] = {}
    for row in rows:
        action_name = row.action

        if (
            not action_name
            or action_name == TemplateRowActionEnum.COORDINATED_ATTACK.value
        ):
            continue

        _labels = deepcopy(row.labels)
        if "" not in _labels:
            _labels.append("")

        for label in _labels:
            if labels is not None and label not in labels:
                continue
            if output_methods.get(label, None) is None:
                output_methods[label] = []
            if current_output_methods.get(label, None) is None:
                resonator_name = row.resonator_name
                resonator_src = get_resonator_icon_fpath(resonator_name)

                current_output_methods[label] = TemplateHtmlOutputMethodModel()
                current_output_methods[label].resonator_name = resonator_name
                current_output_methods[label].resonator_src = resonator_src
            else:
                if row.resonator_name != current_output_methods[label].resonator_name:
                    output_methods[label].append(current_output_methods[label])

                    resonator_name = row.resonator_name
                    resonator_src = get_resonator_icon_fpath(resonator_name)

                    current_output_methods[label] = TemplateHtmlOutputMethodModel()
                    current_output_methods[label].resonator_name = resonator_name
                    current_output_methods[label].resonator_src = resonator_src

            action_src = action_icons.get(action_name, "")
            action = TemplateHtmlOutputMethodActionModel(
                name=action_name, src=action_src
            )
            current_output_methods[label].actions.append(action)

            comment = row.comment
            if comment:
                current_output_methods[label].comments.append(comment)

    for label_name, current_output_method in current_output_methods.items():
        output_methods[label_name].append(current_output_method)

    return output_methods


def export_html_template_output_methods_as_png(
    template_id: str,
    rows: List[TemplateRowModel],
    height: int = 2000,
    labels: Optional[List[str]] = None,
):
    if not template_id or len(rows) == 0:
        return

    html_fpath = Path(TEMPLATE_OUTPUT_METHOD_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    output_methods = get_html_template_output_methods(rows, labels=labels)

    right_arrow_src = get_local_file_url(RIGHT_ARROW_ICON_FPATH)
    for fname_suffix, rows in output_methods.items():
        html_str = template.render(
            output_methods=rows,
            ZhTwEnum=ZhTwEnum,
            _=_,
            right_arrow_src=right_arrow_src,
        )

        png_fname = f"{_(ZhTwEnum.OUTPUT_METHOD)}.png"
        if fname_suffix:
            png_fname = f"{_(ZhTwEnum.OUTPUT_METHOD)}-{fname_suffix}.png"

        export_to_template(template_id, png_fname, html_str, height)


def export_html_template_output_methods_as_png_by_template_id(
    template_id: str,
    home_path: Union[str, Path],
    height: int = 2000,
    labels: Optional[List[str]] = None,
):
    if not template_id:
        return

    template = get_template(template_id)
    if not template:
        return
    rows = template.rows

    html_fpath = Path(TEMPLATE_OUTPUT_METHOD_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        html_template = Template(fp.read())

    output_methods = get_html_template_output_methods(rows, labels=labels)

    right_arrow_src = get_local_file_url(RIGHT_ARROW_ICON_FPATH)
    for fname_suffix, rows in output_methods.items():
        html_str = html_template.render(
            output_methods=rows,
            ZhTwEnum=ZhTwEnum,
            _=_,
            right_arrow_src=right_arrow_src,
        )

        png_fname = f"{template_id}-{_(ZhTwEnum.OUTPUT_METHOD)}.png"
        if fname_suffix:
            png_fname = f"{template_id}-{_(ZhTwEnum.OUTPUT_METHOD)}-{fname_suffix}.png"

        home_path = Path(home_path)
        os.makedirs(home_path, exist_ok=True)
        export_to(home_path, png_fname, html_str, height)
