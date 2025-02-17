import json
import os
from pathlib import Path

from typer import Typer

from ww.locale import ZhTwEnum, _
from ww.utils import get_md5

app = Typer(name="migrate")

elements = {
    _(ZhTwEnum.GLACIO): "glacio",
    _(ZhTwEnum.FUSION): "fusion",
    _(ZhTwEnum.ELECTRO): "electro",
    _(ZhTwEnum.AERO): "aero",
    _(ZhTwEnum.SPECTRO): "spectro",
    _(ZhTwEnum.HAVOC): "havoc",
}


@app.command()
def resonator_info():
    home = "./data/v1/zh_tw/角色"
    home = Path(home)
    for info_fpath in home.glob("*/基本資料.json"):
        with info_fpath.open(mode="r", encoding="utf-8") as fp:
            info = json.load(fp)
            print(info)
        no = info["no"]
        info["element_zh_tw"] = info["element"]
        info["element_en"] = elements[info["element"]]
        del info["element"]

        new_info_fpath = Path(f"./build/migrate/resonators/{no}/info.json")
        os.makedirs(new_info_fpath.parent, exist_ok=True)

        with new_info_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(info, fp, indent=4, ensure_ascii=False)


@app.command()
def docs():
    import yaml

    fpath = Path("./data/v1/zh_tw/docs.yml")

    with fpath.open(mode="r", encoding="utf-8") as stream:
        docs_ = yaml.safe_load(stream)

    new_docs = {}
    new_templates = []
    for template in docs_["templates"]:
        new_template = {}
        new_template["hashed_id"] = get_md5(template["id"])
        for key, value in template.items():
            new_template[key] = value
        new_templates.append(new_template)
    new_docs["templates"] = new_templates

    for name, comparisons in docs_["comparisons"].items():
        new_comparisons = []
        for comparison in comparisons:
            new_comparison = {
                "id": get_md5(name + comparison["title"]),
                "title": comparison["title"],
                "template_ids": comparison["template_ids"],
            }
            new_comparisons.append(new_comparison)
        docs_["comparisons"][name] = new_comparisons

    new_docs["comparisons"] = docs_["comparisons"]

    new_fpath = Path(f"./build/migrate/templates.json")
    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_docs, fp, indent=4, ensure_ascii=False)
