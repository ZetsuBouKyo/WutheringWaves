import os
from pathlib import Path
from typing import Optional, Union

import numpy as np
from html2image import Html2Image
from PIL import Image

from ww.locale import ZhTwEnum, _

TEMPLATE_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/template"


def _get_margin_top(data) -> Optional[int]:
    """Return the count of empty rows."""

    i = 0
    for row in data:
        for pixel in row:
            if pixel[3] != np.int32(0):
                return i
        i += 1


def crop_image(data):
    margin_top = _get_margin_top(data)
    if margin_top is None:
        return data

    bottom = 0
    for i in range(margin_top, len(data)):
        for pixel in data[i]:
            if pixel[3] != np.int32(0):
                break
        else:
            bottom = i
            break
    img_bottom = bottom + margin_top
    if bottom == 0:
        return data
    return data[:img_bottom]


def export_html_as_png(home_path: Path, png_fname: str, html_str: str, height: int):
    os.makedirs(home_path, exist_ok=True)

    h2png = Html2Image(
        custom_flags=[
            "--no-sandbox",
            "--default-background-color=00000000",
            "--force-device-scale-factor=2",
        ],
        output_path=str(home_path),
        size=(1920, height),  # (pixel, pixel)
        disable_logging=True,
    )
    h2png.screenshot(
        html_str=html_str,
        save_as=png_fname,
    )

    fpath = home_path / png_fname
    if not fpath.exists():
        return

    html_str_fname = fpath.stem
    html_str_path = fpath.parent / f"{html_str_fname}.html"
    with html_str_path.open(mode="w", encoding="utf-8") as fp:
        fp.write(html_str)

    img = Image.open(fpath)
    img.load()
    data = np.asarray(img, dtype="int32")
    new_data = crop_image(data)
    if len(data) == len(new_data):
        return
    new_data = new_data.astype(np.uint8)
    img = Image.fromarray(new_data)
    img.save(fpath)


def export_to_template(template_id: str, fname: str, html_str: str, height: int):
    png_home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    export_html_as_png(png_home_path, fname, html_str, height)


def export_to(home: Union[str, Path], png_fname: str, html_str: str, height: int):
    png_home_path = Path(home)
    export_html_as_png(png_home_path, png_fname, html_str, height)
