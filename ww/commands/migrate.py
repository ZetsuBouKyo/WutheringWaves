import json
import os
import re
import shutil
from pathlib import Path

import pandas as pd
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
def resonator_info(new_home: str = "./build/migrate/resonators/"):
    home = "./data/v1/zh_tw/角色"
    home = Path(home)
    names = []
    name2no = {}
    new_home: Path = Path(new_home)
    for resonator_folder_path in home.glob("*"):
        info_fpath = resonator_folder_path / "基本資料.json"
        with info_fpath.open(mode="r", encoding="utf-8") as fp:
            info = json.load(fp)
            print(info["name"])
            new_stat_bonus = {}
            for key, value in info["stat_bonus"].items():
                if key not in ["crit_rate", "crit_dmg", "hp_p", "atk_p", "def_p"]:
                    key = f"bonus_{key}"
                new_stat_bonus[key] = value
            info["stat_bonus"] = new_stat_bonus

        no = info["no"]
        info["element_zh_tw"] = info["element"]
        info["element_en"] = elements[info["element"]]
        del info["element"]
        names.append(info["name"])
        name2no[info["name"]] = no

        # attr
        attr_fpath = resonator_folder_path / "屬性.tsv"
        if attr_fpath.exists():
            attr_df = pd.read_csv(attr_fpath, sep="\t", keep_default_na=False)
            attr_list = []
            for _, row in attr_df.iterrows():
                data = row.to_dict()
                new_row = {
                    "lv": data["等級"],
                    "hp": data["生命"],
                    "atk": str(data["攻擊"]),
                    "def": data["防禦"],
                }
                attr_list.append(new_row)
            info["attrs"] = attr_list

        # skill
        skill_fpath = resonator_folder_path / "技能.tsv"
        if skill_fpath.exists():
            skill_df = pd.read_csv(skill_fpath, sep="\t", keep_default_na=False)
            skill_list = []
            for _, row in skill_df.iterrows():
                data = row.to_dict()
                new_row = {
                    "id": data["代稱"],
                    "type": data["Type"],
                    "skill_type": data["種類"],
                    "element": data["屬性"],
                    "base_attr": data["Base Attribute"],
                    "bonus_type": data["技能加成種類"],
                    "coordinated": data["Coordinated"],
                    "lv1": data["LV1"],
                    "lv2": data["LV2"],
                    "lv3": data["LV3"],
                    "lv4": data["LV4"],
                    "lv5": data["LV5"],
                    "lv6": data["LV6"],
                    "lv7": data["LV7"],
                    "lv8": data["LV8"],
                    "lv9": data["LV8"],
                    "lv10": data["LV10"],
                    "_resonance_energy": data["共鳴解放能量"],
                    "_concerto_energy": data["協奏能量"],
                    "_hardness": data["共振度上限"],
                    "_toughness": data["韌性"],
                    "sta_regen": data["回復耐力值"],
                    "resonance_energy_regen": data["回復共鳴能量"],
                    "concerto_regen": data["回復協奏能量"],
                    "sta_cost": data["耐力消耗"],
                    "concerto_cost": data["消耗協奏能量"],
                    "resonance_cost": data["消耗共鳴能量"],
                    "cd": data["冷卻時間"],
                    "duration": data["持續時間"],
                }
                skill_list.append(new_row)
            info["skills"] = skill_list

        # skill_info
        skill_info_fpath = resonator_folder_path / "技能文本.json"
        if skill_info_fpath.exists():
            skill_info_dict = {}
            with skill_info_fpath.open(mode="r", encoding="utf-8") as fp:
                skill_info = json.load(fp)
                skill_info_dict["normal_attack"] = {
                    "name": skill_info["常態攻擊"]["名稱"],
                    "description": skill_info["常態攻擊"]["描述"],
                }
                skill_info_dict["resonance_skill"] = {
                    "name": skill_info["共鳴技能"]["名稱"],
                    "description": skill_info["共鳴技能"]["描述"],
                }
                skill_info_dict["forte_circuit"] = {
                    "name": skill_info["共鳴回路"]["名稱"],
                    "description": skill_info["共鳴回路"]["描述"],
                }
                skill_info_dict["resonance_liberation"] = {
                    "name": skill_info["共鳴解放"]["名稱"],
                    "description": skill_info["共鳴解放"]["描述"],
                }
                skill_info_dict["intro_skill"] = {
                    "name": skill_info["變奏技能"]["名稱"],
                    "description": skill_info["變奏技能"]["描述"],
                }
                skill_info_dict["outro_skill"] = {
                    "name": skill_info["延奏技能"]["名稱"],
                    "description": skill_info["延奏技能"]["描述"],
                }

                skill_info_dict["inherent_skill_1"] = {
                    "name": skill_info["固有技能1"]["名稱"],
                    "description": skill_info["固有技能1"]["描述"],
                }
                skill_info_dict["inherent_skill_2"] = {
                    "name": skill_info["固有技能2"]["名稱"],
                    "description": skill_info["固有技能2"]["描述"],
                }

                skill_info_dict["chain1"] = {
                    "name": skill_info["共鳴鏈1"]["名稱"],
                    "description": skill_info["共鳴鏈1"]["描述"],
                }
                skill_info_dict["chain2"] = {
                    "name": skill_info["共鳴鏈2"]["名稱"],
                    "description": skill_info["共鳴鏈2"]["描述"],
                }
                skill_info_dict["chain3"] = {
                    "name": skill_info["共鳴鏈3"]["名稱"],
                    "description": skill_info["共鳴鏈3"]["描述"],
                }
                skill_info_dict["chain4"] = {
                    "name": skill_info["共鳴鏈4"]["名稱"],
                    "description": skill_info["共鳴鏈4"]["描述"],
                }
                skill_info_dict["chain5"] = {
                    "name": skill_info["共鳴鏈5"]["名稱"],
                    "description": skill_info["共鳴鏈5"]["描述"],
                }
                skill_info_dict["chain6"] = {
                    "name": skill_info["共鳴鏈6"]["名稱"],
                    "description": skill_info["共鳴鏈6"]["描述"],
                }

            info["skill_infos"] = skill_info_dict

        # save
        new_info_fpath = new_home / no / "info.json"
        os.makedirs(new_info_fpath.parent, exist_ok=True)

        print(info)

        with new_info_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(info, fp, ensure_ascii=False)

    names.sort(key=lambda name: name2no[name])
    new_name2no = {}
    for name in names:
        new_name2no[name] = name2no[name]

    new_fpath = Path(f"./build/migrate/cache/resonator_name_to_no.json")
    os.makedirs(new_fpath.parent, exist_ok=True)

    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_name2no, fp, ensure_ascii=False)


@app.command()
def weapon_cn():
    home = Path("./dev/wiki/zh_cn/weapon")
    name2no = {}
    for fpath in home.glob("*.html"):
        fname = fpath.stem
        pattern = r"^(.*?)\s*\((\d+)\)$"
        match = re.search(pattern, fname)
        if match:
            name2no[match[1]] = match[2]

    names = list(name2no.keys())
    names.sort(key=lambda name: name2no[name])
    new_name2no = {}
    name2name = {}
    for name in names:
        name2name[name] = name
        new_name2no[name] = name2no[name]

    new_fpath = Path(f"./build/migrate/cache/weapon_name_to_no.json")
    os.makedirs(new_fpath.parent, exist_ok=True)
    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_name2no, fp, ensure_ascii=False)

    new_fpath = Path(f"./build/migrate/locale/zh_TW/weapon/name.json")
    os.makedirs(new_fpath.parent, exist_ok=True)
    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(name2name, fp, ensure_ascii=False)


@app.command()
def weapon_tw():
    weapons_fpath = Path("cache/v1/zh_tw/output/weapons_info_tw.json")
    with weapons_fpath.open(mode="r", encoding="utf-8") as fp:
        weapons = json.load(fp)

    for weapon in weapons:
        no = weapon["no"]
        new_info_path = Path((f"./build/migrate/data/weapons/{no}/info.json"))
        os.makedirs(new_info_path.parent, exist_ok=True)
        with new_info_path.open(mode="w", encoding="utf-8") as fp:
            json.dump(weapon, fp, ensure_ascii=False)


@app.command()
def docs(new_fpath: str = "./build/migrate/templates.json"):
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

    new_fpath = Path(new_fpath)
    with new_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(new_docs, fp, indent=4, ensure_ascii=False)


@app.command()
def templates(force: bool = False, new_home: str = "./build/migrate/templates/"):
    home: Path = Path("./cache/v1/zh_tw/custom/template")
    new_home: Path = Path(new_home)
    new_set = set()
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

        new_fpath = new_home / f"{hashed_id}.json"
        new_set.add(hashed_id)
        skip = False
        if new_fpath.exists():
            t0 = fpath.stat().st_mtime
            t1 = new_fpath.stat().st_mtime
            if t1 > t0:
                skip = True
        if not skip or force:
            os.makedirs(new_fpath.parent, exist_ok=True)
            with new_fpath.open(mode="w", encoding="utf-8") as fp:
                json.dump(new_template, fp, ensure_ascii=False)
    for fpath in new_home.glob("*.json"):
        hashed_id = fpath.stem
        if hashed_id not in new_set:
            fpath.unlink()


@app.command()
def minify_damage_analysis(
    force: bool = False, new_home: str = "./build/migrate/data/calculation/template"
):
    home: Path = Path("./build/html/cache/resonator/template")
    new_home: Path = Path(new_home)

    hashed_ids = set()
    new_set = set()
    for hashed_id_folder_path in home.glob("*"):
        hashed_id = hashed_id_folder_path.stem
        hashed_ids.add(hashed_id)
        for affix_policy_folder_path in hashed_id_folder_path.glob("*"):
            # Damage analysis
            affix_policy = affix_policy_folder_path.stem
            damage_analysis_fpath = affix_policy_folder_path / "damage_analysis.json"
            with damage_analysis_fpath.open(mode="r", encoding="utf-8") as fp:
                damage_analysis = json.load(fp)
                del damage_analysis["output_methods"]

            skip_damage_analysis = False
            new_damage_analysis_fpath = (
                new_home / hashed_id / affix_policy / "damage_analysis.json"
            )
            new_set.add(f"{hashed_id}/{affix_policy}/damage_analysis.json")
            if new_damage_analysis_fpath.exists():
                t0 = damage_analysis_fpath.stat().st_mtime
                t1 = new_damage_analysis_fpath.stat().st_mtime
                if t1 > t0:
                    skip_damage_analysis = True
            if not skip_damage_analysis or force:
                os.makedirs(new_damage_analysis_fpath.parent, exist_ok=True)
                with new_damage_analysis_fpath.open(mode="w", encoding="utf-8") as fp:
                    json.dump(damage_analysis, fp, ensure_ascii=False)

            # Echo comparison
            for echo_comparison_fpath in affix_policy_folder_path.glob(
                "echo_comparison/*.json"
            ):
                skip_echo_comparison = False
                fname = echo_comparison_fpath.name
                with echo_comparison_fpath.open(mode="r", encoding="utf-8") as fp:
                    echo_comparison = json.load(fp)
                    del echo_comparison["base_damage"]

                new_echo_comparison_fpath = (
                    new_home / hashed_id / affix_policy / "echo_comparison" / fname
                )
                new_set.add(f"{hashed_id}/{affix_policy}/echo_comparison/{fname}")
                if new_echo_comparison_fpath.exists():
                    t0 = echo_comparison_fpath.stat().st_mtime
                    t1 = new_echo_comparison_fpath.stat().st_mtime
                    if t1 > t0:
                        skip_echo_comparison = True

                if not skip_echo_comparison or force:
                    os.makedirs(new_echo_comparison_fpath.parent, exist_ok=True)
                    with new_echo_comparison_fpath.open(
                        mode="w", encoding="utf-8"
                    ) as fp:
                        json.dump(echo_comparison, fp, ensure_ascii=False)

    # clean
    for hashed_id_folder_path in new_home.glob("*"):
        hashed_id = hashed_id_folder_path.stem
        if hashed_id not in hashed_ids:
            shutil.rmtree(hashed_id_folder_path, ignore_errors=True)
            continue
        for affix_policy_folder_path in hashed_id_folder_path.glob("*"):
            affix_policy = affix_policy_folder_path.stem
            damage_analysis_fpath = affix_policy_folder_path / "damage_analysis.json"
            if damage_analysis_fpath.exists():
                id = f"{hashed_id}/{affix_policy}/damage_analysis.json"
                if id not in new_set:
                    damage_analysis_fpath.unlink()
            for echo_comparison_fpath in affix_policy_folder_path.glob(
                "echo_comparison/*.json"
            ):
                fname = echo_comparison_fpath.name
                if echo_comparison_fpath.exists():
                    id = f"{hashed_id}/{affix_policy}/echo_comparison/{fname}"
                    if id not in new_set:
                        echo_comparison_fpath.unlink()


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
