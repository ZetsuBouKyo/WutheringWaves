import os
from pathlib import Path

from html2image import Html2Image
from jinja2 import Template
from typer import Typer

from ww.html.template import get_resonator_example
from ww.locale import ZhTwEnum, _

app = Typer(name="tests")


@app.command()
def get_html(html_fpath: str, out: str):
    html_fpath = Path(html_fpath)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    resonator = get_resonator_example()
    html_str = template.render(resonator=resonator, ZhTwEnum=ZhTwEnum, _=_)

    out_fpath = Path(out)
    os.makedirs(out_fpath.parent, exist_ok=True)
    with out_fpath.open(mode="w", encoding="utf-8") as fp:
        fp.write(html_str)


@app.command()
def get_png(html_fpath: str, out: str, name: str):
    html_fpath = Path(html_fpath)
    if not html_fpath.exists():
        return
    with html_fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    resonator = get_resonator_example()
    html_str = template.render(resonator=resonator)

    h2png = Html2Image(
        custom_flags=["--no-sandbox"],
        output_path=out,
        size=(1920, 1000),  # (pixel, pixel)
    )
    h2png.screenshot(
        html_str=html_str,
        save_as=name,
    )
