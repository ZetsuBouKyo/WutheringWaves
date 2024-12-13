import os
from pathlib import Path

from html2image import Html2Image
from jinja2 import Template
from typer import Typer

from ww.html.image.resonator import (
    get_element_class_name,
    get_element_icon_fpath,
    get_resonator_icon_fpath,
)
from ww.locale import ZhTwEnum, _
from ww.model.template import TemplateHtmlResonatorModel


def get_resonator_example() -> TemplateHtmlResonatorModel:
    resonator_name = "凌陽"
    resonator_src = get_resonator_icon_fpath(resonator_name)

    element = _(ZhTwEnum.GLACIO)
    element_class_name = get_element_class_name(element)
    element_src = get_element_icon_fpath(element)

    return TemplateHtmlResonatorModel(
        name=resonator_name,
        chain="1",
        element=element,
        weapon_name="擎淵怒濤",
        weapon_rank="1",
        weapon_level="90",
        level="90",
        hp="15000",
        attack="2000",
        defense="1000",
        crit_rate="50.00%",
        crit_dmg="220.00%",
        energy_regen="120.00%",
        resonance_skill_dmg_bonus="100.00%",
        basic_attack_dmg_bonus="8.00%",
        heavy_attack_dmg_bonus="8.00%",
        resonance_liberation_dmg_bonus="8.00%",
        healing_bonus="0.00%",
        physical_dmg_bonus="0.00%",
        glacio_dmg_bonus="70.00%",
        fusion_dmg_bonus="0.00%",
        electro_dmg_bonus="0.00%",
        aero_dmg_bonus="0.00%",
        spectro_dmg_bonus="0.00%",
        havoc_dmg_bonus="0.00%",
        physical_dmg_res="0.00%",
        glacio_dmg_res="0.00%",
        fusion_dmg_res="0.00%",
        electro_dmg_res="0.00%",
        aero_dmg_res="0.00%",
        spectro_dmg_res="0.00%",
        havoc_dmg_res="0.00%",
        normal_attack_lv="1",
        resonance_skill_lv="1",
        forte_circuit_lv="1",
        resonance_liberation_lv="1",
        intro_skill_lv="1",
        inherent_skill_1="✓",
        inherent_skill_2="✓",
        element_src=element_src,
        element_class_name=element_class_name,
        resonator_src=resonator_src,
    )


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
    html_str = template.render(resonator=resonator, ZhTwEnum=ZhTwEnum, _=_)

    h2png = Html2Image(
        custom_flags=[
            "--no-sandbox",
            "--default-background-color=00000000",
            "--force-device-scale-factor=2",
        ],
        output_path=out,
        size=(1920, 276),  # (pixel, pixel)
    )
    h2png.screenshot(
        html_str=html_str,
        save_as=name,
    )
