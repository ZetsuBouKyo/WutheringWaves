import os
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from html2image import Html2Image

from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateDamageDistributionModel

TEMPLATE_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/template"
TEMPLATE_DAMAGE_DISTRIBUTION_HOME_PATH = "./cache/v1/zh_tw/output/damage_distribution"
TEMPLATE_DAMAGE_DISTRIBUTION_FNAME = "damage_distribution_raw.png"


def export_html_as_png(home_path: Path, fname: str, html_str: str, height: int):
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
        save_as=fname,
    )


def export_to_template(template_id: str, fname: str, html_str: str, height: int):
    png_home_path = Path(TEMPLATE_PNG_HOME_PATH) / template_id
    export_html_as_png(png_home_path, fname, html_str, height)
