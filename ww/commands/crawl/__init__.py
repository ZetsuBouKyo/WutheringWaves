import json
import os
from pathlib import Path

from typer import Typer

from ww.commands.crawl.echo import EchoParser
from ww.commands.crawl.id_parser import id_parser
from ww.commands.crawl.resonator import ResonatorParser
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
