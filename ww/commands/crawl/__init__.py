import json
from pathlib import Path

import requests
from typer import Typer

from ww.commands.crawl.html_parser import WutheringWikiHTMLParser

app = Typer(name="crawl")

RESONATOR_IDS_PATH = "./cache/v1/zh_tw/raw/resonator_id.json"
WEAPON_IDS_PATH = "./cache/v1/zh_tw/raw/weapon_id.json"
MONSTER_IDS_PATH = "./cache/v1/zh_tw/raw/monster_id.json"


def parser(url: str, fpath: str):
    resp = requests.get(url)
    html = resp.text

    parser = WutheringWikiHTMLParser("itementry")
    parser.feed(html)

    ids = parser.current_ids
    names = parser.current_names
    data = {}
    for i in range(len(ids)):
        data[ids[i]] = names[i]

    fpath = Path(fpath)
    with fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


@app.command()
def get_resonator_ids():
    parser("https://wuthering.wiki/cn/index.html", RESONATOR_IDS_PATH)


@app.command()
def get_weapon_ids():
    parser("https://wuthering.wiki/cn/weapons.html", WEAPON_IDS_PATH)


@app.command()
def get_monster_ids():
    parser("https://wuthering.wiki/cn/monsters.html", MONSTER_IDS_PATH)
