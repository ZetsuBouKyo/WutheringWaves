from pathlib import Path

import pandas as pd
from html2image import Html2Image
from PIL import Image
from typer import Argument, Option, Typer

from ww.commands.custom.resonators import app as resonators
from ww.commands.custom.template import app as template
from ww.model.resonators import ResonatorsEnum
from ww.tables.calculated_resonators import calc as _calc
from ww.tables.resonators import (
    CALCULATED_RESONATOR_PATH,
    CalculatedResonatorsTable,
    ResonatorsTable,
)
from ww.utils.pd import get_df
from ww.utils.table import print_table, print_transpose_table

CACHE_HOME_PATH = "./cache/v1/zh_tw/output/png"

app = Typer(name="custom")
app.add_typer(resonators)
app.add_typer(template)


@app.command()
def df_to_html(src: str, dest: str):
    df = get_df(src)
    html = df.to_html()
    dest = Path(dest)
    with dest.open(mode="w", encoding="utf-8") as fp:
        fp.write(html)


@app.command()
def gen_png(src: str, dest: str):
    h2png = Html2Image(
        custom_flags=["--no-sandbox"],
        output_path=CACHE_HOME_PATH,
        size=(3000, 3000),  # (pixel, pixel)
    )
    h2png.screenshot(
        html_file=src,
        save_as=dest,
    )

    png_path = Path(CACHE_HOME_PATH) / dest

    # open the PNG again, and crop it to the content.

    img = Image.open(png_path)

    # Get the content bounds.
    content = img.getbbox()

    # Crop the image.
    img = img.crop(content)

    # Save the image.
    img.save(png_path)
