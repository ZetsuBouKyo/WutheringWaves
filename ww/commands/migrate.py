import json
import os
from pathlib import Path

import yaml
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
    names = []
    name2no = {}
    for info_fpath in home.glob("*/基本資料.json"):
        with info_fpath.open(mode="r", encoding="utf-8") as fp:
            info = json.load(fp)
            print(info)
        no = info["no"]
        info["element_zh_tw"] = info["element"]
        info["element_en"] = elements[info["element"]]
        del info["element"]
        names.append(info["name"])
        name2no[info["name"]] = no

        new_info_fpath = Path(f"./build/migrate/resonators/{no}/info.json")
        os.makedirs(new_info_fpath.parent, exist_ok=True)

        with new_info_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(info, fp, indent=4, ensure_ascii=False)

    names.sort(key=lambda name: name2no[name])
    new_name2no = {}
    for name in names:
        new_name2no[name] = name2no[name]

    new_fpath = Path(f"./build/migrate/cache/resonator_name_to_no.json")
    os.makedirs(new_fpath.parent, exist_ok=True)

    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_name2no, fp, indent=4, ensure_ascii=False)


@app.command()
def docs():
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


@app.command()
def templates():
    home = Path("./cache/v1/zh_tw/custom/template")
    id2hashed_id = {}
    for fpath in home.glob("*.json"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            template = json.load(fp)
        hashed_id = get_md5(template["id"])
        id2hashed_id[template["id"]] = hashed_id

        new_template = {}
        new_template["hashed_id"] = hashed_id
        for key, value in template.items():
            new_template[key] = value

        new_fpath = Path(f"./build/migrate/templates/{hashed_id}.json")
        os.makedirs(new_fpath.parent, exist_ok=True)
        with new_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(new_template, fp, indent=4, ensure_ascii=False)


@app.command()
def locale():
    resonator_name_fpath = Path("./data/v1/zh_tw/manual/resonator_id.json")
    new_resonator_name_fpath = Path("./build/migrate/locale/zh_TW/resonator/name.json")
    with resonator_name_fpath.open(mode="r", encoding="utf-8") as fp:
        d = json.load(fp)
    new_d = {}
    for v in d.values():
        new_d[v] = v
    os.makedirs(new_resonator_name_fpath.parent, exist_ok=True)
    with new_resonator_name_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_d, fp, indent=4, ensure_ascii=False)

    template_ids = {}
    docs_fpath = Path("./data/v1/zh_tw/docs.yml")
    with docs_fpath.open(mode="r", encoding="utf-8") as stream:
        docs_ = yaml.safe_load(stream)
    for template in docs_["templates"]:
        template_ids[template["id"]] = template["id"]

    template_ids_fpath = Path("./build/migrate/locale/zh_TW/template_ids.json")
    os.makedirs(template_ids_fpath.parent, exist_ok=True)
    with template_ids_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(template_ids, fp, indent=4, ensure_ascii=False)

    comparison_titles = {}
    for comparisons in docs_["comparisons"].values():
        for comparison in comparisons:
            comparison_titles[comparison["title"]] = comparison["title"]
    comparison_titles_fpath = Path(
        "./build/migrate/locale/zh_TW/comparison_titles.json"
    )
    os.makedirs(comparison_titles_fpath.parent, exist_ok=True)
    with comparison_titles_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(comparison_titles, fp, indent=4, ensure_ascii=False)
