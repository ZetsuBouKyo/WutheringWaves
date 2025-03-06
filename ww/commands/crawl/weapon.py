import json
import re
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
        self._passive_stat_bonus = set()

    def parse(self):
        for fpath in self.home.glob("*.html"):
            print(fpath)
            with fpath.open(mode="r", encoding="utf-8") as fp:
                html_str = fp.read()
            tree = html.fromstring(html_str)
            weapon = self.get_weapon(tree)
            self._weapons.append(weapon)
        print(self._passive_stat_bonus)

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

    def get_weapon_type(self, tree) -> str:
        raw = get_text(tree, '//span[@class="baseinfo"]')
        raw = raw.split("\n")
        raw = raw[1].replace("武器: ", "")
        return raw

    def get_attrs(self, tree):
        weapon_stat_bonus_to_eng = {
            "生命": "hp_p",
            "生命百分比": "hp_p",
            "暴击伤害": "crit_dmg",
            "防御": "def_p",
            "防御百分比": "def_p",
            "暴击": "crit_rate",
            "攻击": "atk_p",
            "攻击%": "atk_p",
            "攻击百分比": "atk_p",
            "共鸣效率": "energy_regen",
        }

        tables = tree.xpath('//table[@class="stats"]')
        table = tables[0]
        ths = table.xpath("//th")
        h = html.tostring(ths[2], pretty_print=True, method="html", encoding=str)
        h_text = html2text(h)
        h_text = clear_text(h_text)
        stat_bonus_name = weapon_stat_bonus_to_eng[h_text]
        trs = table.xpath("//tr")
        attrs = []
        tds = trs[0].xpath("//td")
        attr = {}
        for i, td in enumerate(tds):
            h = html.tostring(td, pretty_print=True, method="html", encoding=str)
            h_text = html2text(h)
            h_text = clear_text(h_text)
            if i % 3 == 0:
                attr["lv"] = h_text
            elif i % 3 == 1:
                attr["atk"] = h_text
            elif i % 3 == 2:
                attr[stat_bonus_name] = h_text
                attrs.append(attr)
                attr = {}
        return attrs

    def get_passive_buffs(self, description: str):
        first_line = description.split("，")[0].split("。")[0]
        # print(first_line)
        if "/" not in first_line:
            return []

        pattern = r"[\u4e00-\u9fff]+"
        matches = re.findall(pattern, first_line)
        text = "".join(matches)
        self._passive_stat_bonus.add(text)

        pattern = r"(\d+%)|(\d+\.\d+%)"
        percentages = re.findall(pattern, first_line)
        print(percentages)

        buffs = []
        for ps in percentages:
            p = ps[0]
            if not p:
                p = ps[1]
            if not p:
                return buffs
            buff = {}
            if text == "生命提升":
                buff = {"hp_p": p}
            elif text == "共鸣效率提升":
                buff = {"energy_regen": p}
            elif text == "共鸣解放伤害加成提升":
                buff = {"bonus_resonance_liberation": p}
            elif text == "普攻和重击伤害加成提升":
                buff = {"bonus_basic_attack": p, "bonus_heavy_attack": p}
            elif text == "共鸣技能伤害加成提升":
                buff = {"bonus_resonance_skill": p}
            elif text == "暴击提升":
                buff = {"crit_rate": p}
            elif text == "攻击提升":
                buff = {"atk_p": p}
            elif text == "全属性伤害加成提升":
                buff = {
                    "bonus_glacio": p,
                    "bonus_fusion": p,
                    "bonus_electro": p,
                    "bonus_aero": p,
                    "bonus_spectro": p,
                    "bonus_havoc": p,
                }
            if buff:
                buffs.append(buff)

        return buffs

    def get_weapon(self, tree) -> dict:
        attrs = self.get_attrs(tree)
        description = get_text(tree, '//span[@class="skilldescription"]')
        buffs = self.get_passive_buffs(description)
        weapon = {
            "no": self.get_weapon_no(tree),
            "name": get_text(tree, '//span[@class="name"]'),
            "star": self.get_weapon_star(tree),
            "type": self.get_weapon_type(tree).lower(),
            "passive": {
                "name": get_text(tree, '//span[@class="skillname"]'),
                "description": description,
                "passive_buffs": buffs,
            },
            "attrs": attrs,
        }
        return weapon


def save_weapons(home: str):
    parser = WeaponsParser(home)
    parser.parse()
    parser.save()
