from pathlib import Path

import pandas as pd
from html2image import Html2Image
from typer import Argument, Option, Typer

from ww.commands.custom.resonator.calc import calc
from ww.model.resonator import ResonatorEnum
from ww.tables.resonators import ResonatorsTable
from ww.utils.pd import get_df
from ww.utils.table import print_table, print_transpose_table

app = Typer(name="resonator")


# @app.command()
# def gen_html():
#     df = _get_custom_resonators()
#     html = Path(RESONATOR_HTML_PATH)
#     df.to_html(html)


# @app.command()
# def gen_png():
#     h2png = Html2Image(
#         custom_flags=["--no-sandbox"],
#         output_path=CACHE_PATH,
#     )
#     h2png.screenshot(
#         html_file=RESONATOR_HTML_PATH,
#         save_as=RESONATOR_PNG_FNAME,
#     )


@app.command()
def gem_calc():
    calc()


@app.command()
def list():
    table = ResonatorsTable()
    df = table.df

    table_title = "角色"
    column_name = df.columns[0]
    _df = df[[column_name]]
    print_table(table_title, _df)


@app.command()
def search(id: str, col: ResonatorEnum = Argument(...)):
    table = ResonatorsTable()
    cell = table.search(id, col)

    print(cell)
