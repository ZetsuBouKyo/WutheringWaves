from pathlib import Path

from html2image import Html2Image
from jinja2 import Template
from PIL import Image
from typer import Typer

from ww.commands.custom.resonators import app as resonators
from ww.commands.custom.template import app as template
from ww.commands.custom.tests import app as tests
from ww.html.image.export import export_html_as_png
from ww.utils.pd import get_df
from ww.utils.table import print_table, print_transpose_table

CACHE_HOME_PATH = "./cache/v1/zh_tw/output/png"

TABLE_HTML_PATH = "./html/image/table.jinja2"

app = Typer(name="custom")
app.add_typer(resonators)
app.add_typer(template)
app.add_typer(tests)


@app.command()
def tsv_to_png(src: str, dest: str, fname: str, height: int):
    df = get_df(src)

    column_names = list(df.columns)
    columns = {}
    for column_name in column_names:
        if column_name.startswith("Unnamed: "):
            columns[column_name] = ""
    df.rename(columns=columns, inplace=True)

    table_html = df.to_html(index=False)

    html_fpath = Path(TABLE_HTML_PATH)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        html_template = Template(fp.read())

    html_str = html_template.render(table_html=table_html)
    html_str = html_str.replace('<table border="1" class="dataframe">', "<table>")
    html_str = html_str.replace('<tr style="text-align: right;">', "<tr>")

    export_html_as_png(Path(dest), fname, html_str, height)


@app.command()
def tsv_to_gamer(src: str, dest: str, fname: str):
    df = get_df(src)

    column_names = list(df.columns)
    columns = {}
    for column_name in column_names:
        if column_name.startswith("Unnamed: "):
            columns[column_name] = ""
    df.rename(columns=columns, inplace=True)

    table_html = df.to_html(index=False)

    patterns = [
        ('<table border="1" class="dataframe">', "<table>"),
        ('<tr style="text-align: right;">', "<tr>"),
        ("<table>", "[table width=98% cellspacing=1 cellpadding=1 border=1]"),
        ("</table>", "[/table]"),
        ("<tbody>", ""),
        ("</tbody>", ""),
        ("<thead>", ""),
        ("</thead>", ""),
        ("<th>", "[td]"),
        ("</th>", "[/td]"),
        ("<tr>", "[tr]"),
        ("</tr>", "[/tr]"),
        ("<td>", "[td]"),
        ("</td>", "[/td]"),
    ]
    for pattern in patterns:
        table_html = table_html.replace(pattern[0], pattern[1])

    dest = Path(dest)
    if not dest.is_dir():
        return

    fpath = dest / fname

    with fpath.open(mode="w", encoding="utf-8") as fp:
        fp.write(table_html)


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
