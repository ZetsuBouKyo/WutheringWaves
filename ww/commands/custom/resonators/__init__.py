from pathlib import Path

import pandas as pd
from html2image import Html2Image
from typer import Argument, Option, Typer

from ww.commands.custom.resonators.calc import get_calculated_resonators_df
from ww.model.resonators import ResonatorsEnum
from ww.tables.resonators import ResonatorsTable
from ww.utils.pd import get_df
from ww.utils.table import print_table, print_transpose_table

CALCULATED_RESONATOR_PATH = "./cache/[計算用]角色"

app = Typer(name="resonators")


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

# html = Path(CALCULATED_RESONATOR_HTML_PATH)
# calculated_resonators_df.to_html(html)

# print(df.transpose())

# print(resonators.head(2).T)
# print_transpose_table("", resonators.head(2).T)
# print(resonators.head(2).T)
# print_transpose_table("", calculated_resonators_df.head(5).T)


@app.command()
def calc():
    df = get_calculated_resonators_df()
    fpath = Path(CALCULATED_RESONATOR_PATH)
    df.to_csv(fpath, sep="\t")


@app.command()
def list():
    table = ResonatorsTable()
    df = table.df

    table_title = "角色"
    column_name = df.columns[0]
    _df = df[[column_name]]
    print_table(table_title, _df)


@app.command()
def search(id: str, col: ResonatorsEnum = Argument(...)):
    table = ResonatorsTable()
    cell = table.search(id, col)

    print(cell)
