import json
import os
from collections import defaultdict
from pathlib import Path

import requests
from typer import Typer

from ww.commands.crawl.echo import EchoParser
from ww.commands.crawl.hakush import HakushResonator
from ww.commands.crawl.id_parser import id_parser
from ww.commands.crawl.resonator import ResonatorParser, ResonatorParser2
from ww.commands.crawl.weapon import WeaponParser, save_weapons

app = Typer(name="crawl")

RESONATOR_IDS_PATH = "./cache/v1/zh_tw/raw/resonator_id.json"
WEAPON_IDS_PATH = "./cache/v1/zh_tw/raw/weapon_id.json"
MONSTER_IDS_PATH = "./cache/v1/zh_tw/raw/monster_id.json"

RESONATORS_HOME_PATH = "./cache/v1/zh_tw/output/resonators"
WEAPONS_HOME_PATH = "./cache/v1/zh_tw/output/weapons"
ECHOES_HOME_PATH = "./cache/v1/zh_tw/output/echoes"


@app.command()
def get_resonator_ids():
    id_parser("https://wuthering.wiki/cn/index.html", RESONATOR_IDS_PATH)


@app.command()
def get_weapon_ids():
    id_parser("https://wuthering.wiki/cn/weapons.html", WEAPON_IDS_PATH)


@app.command()
def get_monster_ids():
    id_parser("https://wuthering.wiki/cn/monsters.html", MONSTER_IDS_PATH)


@app.command()
def get_resonator(home: str):
    home = Path(home)
    for fpath in home.glob("*.html"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            text = fp.read()

        parser = ResonatorParser(text)
        data = parser.get_data()
        data_str = json.dumps(data, indent=4, ensure_ascii=False)
        print(data_str)

        fpath_out = Path(RESONATORS_HOME_PATH) / f"{fpath.stem}.json"
        os.makedirs(fpath_out.parent, exist_ok=True)
        with fpath_out.open(mode="w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)


@app.command()
def parse_resonators(home: str):
    home = Path(home)
    for fpath in home.glob("*.json"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            text = fp.read()
        parser = ResonatorParser2(text)
        # return


@app.command()
def parse_resonator_stat(home: str):
    home = Path(home)
    s = set()
    for fpath in home.glob("*.json"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            text = fp.read()
        parser = ResonatorParser2(text)
        s |= parser.get_stat()
    s = list(s)
    s.sort()
    print(s)


@app.command()
def get_resonator_jsons(host: str, home: str):
    if not host.endswith("/"):
        host += "/"
    resp = requests.get(f"{host}ww/data/character.json")
    data = resp.json()
    nos = list(data.keys())
    nos.sort()

    home: Path = Path(home)
    os.makedirs(home, exist_ok=True)
    for no in nos:
        api = f"{host}ww/data/zh/character/{no}.json"
        resp = requests.get(api)
        data = resp.json()
        fpath = home / f"{no}.json"
        with fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)


@app.command()
def get_weapon(home: str):
    home = Path(home)
    for fpath in home.glob("*.html"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            text = fp.read()

        parser = WeaponParser(text)
        data = parser.get_data()
        data_str = json.dumps(data, indent=4, ensure_ascii=False)
        print(data_str)

        fpath_out = Path(WEAPONS_HOME_PATH) / f"{fpath.stem}.json"
        os.makedirs(fpath_out.parent, exist_ok=True)
        with fpath_out.open(mode="w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)


@app.command()
def get_weapon_2(home: str):
    save_weapons(home)


@app.command()
def get_echo(home: str):
    home = Path(home)
    data = {}
    for fpath in home.glob("*.html"):
        with fpath.open(mode="r", encoding="utf-8") as fp:
            text = fp.read()

        parser = EchoParser(text)
        name, description = parser.get_data()
        data[name] = description
    data_str = json.dumps(data, indent=4, ensure_ascii=False)
    print(data_str)
    fpath_out = Path(ECHOES_HOME_PATH) / "echo_skill_descriptions.json"
    os.makedirs(fpath_out.parent, exist_ok=True)
    with fpath_out.open(mode="w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


@app.command()
def get_hakush_resonator(source: str, target: str, cn2tw: str):
    hakush = HakushResonator(source, target, cn2tw)
    hakush.save_info()
    hakush.save_py_attr()
    hakush.save_py_tsv()
    hakush.save_py_skill_info()


@app.command()
def get_hakush_resonators(source_home: str, target: str, cn2tw: str):
    source_home_path = Path(source_home)
    for source in source_home_path.glob("*.json"):
        hakush = HakushResonator(source, target, cn2tw)
        hakush.save_info()
        hakush.save_py_attr()
        hakush.save_py_tsv()
        hakush.save_py_skill_info()


def get_text2key(fpath: str):
    p = Path(fpath)

    with p.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)

    text2key = defaultdict(list)
    for row in data:
        key = row["Id"]
        text = row["Content"]
        text2key[text].append(key)
    return text2key


def get_key2text(fpath: str):
    p = Path(fpath)

    with p.open(mode="r", encoding="utf-8") as fp:
        data = json.load(fp)

    key2text = {}
    for row in data:
        key = row["Id"]
        text = row["Content"]
        key2text[key] = text
    return key2text


@app.command()
def cn_text2key(cn: str = "./dev/lang/cn.json"):
    cn_text2key = get_text2key(cn)

    cn_text2key_fpath = "./dev/lang/cn_text2key.json"
    cn_text2key_fpath = Path(cn_text2key_fpath)
    with cn_text2key_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(cn_text2key, fp, indent=4, ensure_ascii=False)


@app.command()
def cn2tw(cn: str = "./dev/lang/cn.json", tw: str = "./dev/lang/tw.json"):
    cn_text2key = get_text2key(cn)
    tw_key2text = get_key2text(tw)

    cn2tw = {}
    for key, value in cn_text2key.items():
        cn2tw[key] = tw_key2text[value[0]]

    cn2tw_fpath = "./dev/lang/cn2tw.json"
    cn2tw_fpath = Path(cn2tw_fpath)
    with cn2tw_fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(cn2tw, fp, indent=4, ensure_ascii=False)
