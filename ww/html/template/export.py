import os
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from html2image import Html2Image

from ww.model.template import TemplateDamageDistributionModel

TEMPLATE_PNG_HOME_PATH = "./cache/v1/zh_tw/output/png/template"
TEMPLATE_DAMAGE_DISTRIBUTION_HOME_PATH = "./cache/v1/zh_tw/output/damage_distribution"
TEMPLATE_DAMAGE_DISTRIBUTION_RAW_FNAME = "damage_distribution_raw.png"


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


def export_damage_distribution_raw_png(
    name: str, damage_distributions: List[TemplateDamageDistributionModel]
):
    if not name or len(damage_distributions) == 0:
        return
    # png_home_path = Path(TEMPLATE_DAMAGE_DISTRIBUTION_HOME_PATH) / name
    # os.makedirs(png_home_path, exist_ok=True)
