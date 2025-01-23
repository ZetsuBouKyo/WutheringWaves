import json
from pathlib import Path

from html2text import html2text
from lxml import html

from ww.commands.crawl.utils import clear_text
from ww.locale import ZhTwEnum, _

WEAPONS_INFO_FPATH = "./cache/v1/zh_tw/output/weapons_info.json"


class WeaponParser:
    def __init__(self, html_str: str):
        self.html_str = html_str
        self.tree = html.fromstring(self.html_str)
        self.data = {}

    def get_name_pattern(self) -> str:
        return f'//span[@class="skillname"]'

    def get_description_pattern(self) -> str:
        return f'//span[@class="skilldescription"]'

    def parse(self, pattern: str, key_name: str):
        elements = self.tree.xpath(pattern)
        if elements:
            length = len(elements)
            if length != 1:
                print(f"Elements: {length}")
                return
            for element in elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)

                print(h_text)
                self.data[key_name] = h_text

    def get_data(self):
        self.parse(self.get_name_pattern(), _(ZhTwEnum.NAME))
        self.parse(self.get_description_pattern(), _(ZhTwEnum.DESCRIPTION))
        return self.data


def get_text(tree, pattern) -> str:
    elements = tree.xpath(pattern)
    if elements:
        length = len(elements)
        if length != 1:
            print(f"Elements: {length}")
            return ""
        for element in elements:
            h = html.tostring(element, pretty_print=True, method="html", encoding=str)

            h_text = html2text(h)
            h_text = clear_text(h_text)

    return h_text


class WeaponsParser:

    def __init__(self, home: str, weapons_info_fpath: str = WEAPONS_INFO_FPATH):
        self.home = Path(home)
        self.weapons_info_fpath = Path(weapons_info_fpath)
        self._weapons = []

    def parse(self):
        for fpath in self.home.glob("*.html"):
            with fpath.open(mode="r", encoding="utf-8") as fp:
                html_str = fp.read()
            tree = html.fromstring(html_str)
            weapon = self.get_weapon(tree)
            self._weapons.append(weapon)

    def save(self):
        if len(self._weapons) == 0:
            return
        with self.weapons_info_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(self._weapons, fp, indent=4, ensure_ascii=False)

    def get_weapon_no(self, tree) -> str:
        title = get_text(tree, "//title")
        no = title.split(" ")[-1][1:-1]
        return no

    def get_weapon_star(self, tree) -> str:
        raw = get_text(tree, '//span[@class="baseinfo"]')
        raw = raw.split("\n")
        raw = raw[0].replace("品质: ", "").replace("-star", "")
        return raw

    def get_weapon(self, tree) -> dict:
        weapon = {
            "no": self.get_weapon_no(tree),
            "name": get_text(tree, '//span[@class="name"]'),
            "star": self.get_weapon_star(tree),
            "skill_name": get_text(tree, '//span[@class="skillname"]'),
            "skill_description": get_text(tree, '//span[@class="skilldescription"]'),
        }
        return weapon


def save_weapons(home: str):
    parser = WeaponsParser(home)
    parser.parse()
    parser.save()
