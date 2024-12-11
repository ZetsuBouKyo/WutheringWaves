import os
from pathlib import Path

from ww.html.template.export import TEMPLATE_PNG_HOME_PATH, export_to_template
from ww.locale import ZhTwEnum, _
from ww.tables.resonator import CalculatedResonatorsTable
from ww.utils import get_jinja2_template
from ww.utils.number import to_percentage_str

TEMPLATE_ECHO_HTML_PATH = "./html/template/echo.jinja2"


def export_echo_as_png(template_id: str, resonator_id: str):
    if not template_id:
        return

    home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(home_path, exist_ok=True)

    template = get_jinja2_template(TEMPLATE_ECHO_HTML_PATH)

    calculated_resonator_table = CalculatedResonatorsTable()
    resonator = calculated_resonator_table.get_calculated_resonator_model(resonator_id)

    html_str = template.render(
        resonator=resonator, to_percentage_str=to_percentage_str, ZhTwEnum=ZhTwEnum, _=_
    )

    fname = f"{_(resonator_id)} {_(ZhTwEnum.ECHO)}.png"
    export_to_template(template_id, fname, html_str, height=400)
