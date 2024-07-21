from pathlib import Path

import pandas as pd
from html2image import Html2Image
from PIL import Image
from typer import Argument, Option, Typer

from ww.model.resonators import ResonatorsEnum
from ww.tables.calculated_resonators import calc as _calc
from ww.tables.resonators import (
    CALCULATED_RESONATOR_PATH,
    CalculatedResonatorsTable,
    ResonatorsTable,
)
from ww.utils.pd import get_df
from ww.utils.table import print_table, print_transpose_table

CACHE_PATH = "./cache"
CALCULATED_RESONATOR_HTML_PATH = "./cache/[計算用]角色.html"
RESONATORS_HTML_PATH = "./cache/角色.html"
RESONATORS_PNG_FNAME = "角色.png"

app = Typer(name="resonators")


# @app.command()
# def gen_html():
#     df = _get_custom_resonators()
#     html = Path(RESONATOR_HTML_PATH)
#     df.to_html(html)


@app.command()
def gen_png():
    h2png = Html2Image(
        custom_flags=["--no-sandbox"], output_path=CACHE_PATH, size=(3000, 3000)
    )
    h2png.screenshot(
        html_file=RESONATORS_HTML_PATH,
        save_as=RESONATORS_PNG_FNAME,
    )

    png_path = Path(CACHE_PATH) / RESONATORS_PNG_FNAME

    # open the PNG again, and crop it to the content.

    img = Image.open(png_path)

    # Get the content bounds.
    content = img.getbbox()

    # Crop the image.
    img = img.crop(content)

    # Save the image.
    img.save(png_path)


# html = Path(CALCULATED_RESONATOR_HTML_PATH)
# calculated_resonators_df.to_html(html)

# print(df.transpose())

# print(resonators.head(2).T)
# print_transpose_table("", resonators.head(2).T)
# print(resonators.head(2).T)
# print_transpose_table("", calculated_resonators_df.head(5).T)


@app.command()
def calc():
    _calc()


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


@app.command()
def list_calc():
    table = CalculatedResonatorsTable()
    df = table.df

    table_title = "角色"
    print_transpose_table(table_title, df.head(5).T)
