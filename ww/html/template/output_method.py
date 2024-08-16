from pathlib import Path
from typing import List

from jinja2 import Template

from ww.html.template.export import export_html_as_png
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateHtmlOutputMethodModel, TemplateRowModel

TEMPLATE_OUTPUT_METHOD_HTML_PATH = "./html/template/output_method.html"


def get_html_template_output_method_model(
    rows: List[TemplateRowModel],
) -> List[TemplateHtmlOutputMethodModel]:
    output_methods = []
    current_output_method = TemplateHtmlOutputMethodModel()
    for row in rows:
        if row.resonator_name != current_output_method.resonator_name:
            if not current_output_method.is_none():
                output_methods.append(current_output_method)

            current_output_method = TemplateHtmlOutputMethodModel()
            current_output_method.resonator_name = row.resonator_name
        else:
            current_output_method.actions.append(row.action)

    return output_methods


def export_html_template_output_method_model_as_png(
    template_id: str, rows: List[TemplateRowModel]
):
    if not template_id or len(rows) == 0:
        return

    html_fpath = Path(TEMPLATE_OUTPUT_METHOD_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    output_methods = get_html_template_output_method_model(rows)

    # html_str = template.render(output_methods=output_methods, ZhTwEnum=ZhTwEnum, _=_)
    # png_fname = f"{_(ZhTwEnum.OUTPUT_METHOD)}.png"

    # export_html_as_png(template_id, png_fname, html_str)
