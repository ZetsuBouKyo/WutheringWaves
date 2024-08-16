import os
from pathlib import Path

from html2image import Html2Image

TEMPLATE_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/template"


def export_html_as_png(template_id: str, fname: str, html_str: str, height: int):
    png_home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    os.makedirs(png_home_path, exist_ok=True)

    h2png = Html2Image(
        custom_flags=[
            "--no-sandbox",
            "--default-background-color=00000000",
            "--force-device-scale-factor=2",
        ],
        output_path=str(png_home_path),
        size=(1920, height),  # (pixel, pixel)
        disable_logging=True,
    )
    h2png.screenshot(
        html_str=html_str,
        save_as=fname,
    )
