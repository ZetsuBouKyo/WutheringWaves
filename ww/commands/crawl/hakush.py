import json
import os
from collections import deque
from pathlib import Path

from ww.utils.number import get_number


def get_icon_fpath(icon: str) -> str:
    if not icon:
        return ""
    icon = icon.replace("/Game/Aki/", "/assets/")
    icon = icon.split(".")[0] + ".webp"
    return icon


class HakushResonator:
    def __init__(self, source: str, target: str, cn2tw: str, items: str):
        source_path = Path(source)
        if not source_path.exists():
            print(f"{source} not found.")
            return

        self.target_path = Path(target)
        if self.target_path.exists() and not self.target_path.is_dir():
            return

        with source_path.open(mode="r", encoding="utf-8") as fp:
            self.data = json.load(fp)

        cn2tw_fpath = Path(cn2tw)
        if cn2tw_fpath.exists():
            with cn2tw_fpath.open(mode="r", encoding="utf-8") as fp:
                self.cn2tw_data = json.load(fp)
        else:
            self.cn2tw_data = {}

        items_fpath = Path(items)
        self.items_data = {}
        if items_fpath.exists():
            with items_fpath.open(mode="r", encoding="utf-8") as fp:
                self.items_data = json.load(fp)

    def get_skill_list(self, skill):
        level = skill.get("Level", {})
        skill_list = []
        for row in level.values():
            data = {
                "name": self.cn2tw(row["Name"]),
                "format": self.cn2tw(row["Format"]),
                "param": row["Param"],
            }
            skill_list.append(data)
        return skill_list

    def cn2tw(self, cn: str) -> str:
        if not cn:
            return cn
        return self.cn2tw_data.get(cn, cn)

    def save_info(self):
        id = self.data.get("Id", None)
        if id is None:
            return
        rarity = self.data.get("Rarity", "")
        weapon_id = self.data.get("Weapon", "")
        element_id = self.data.get("Element", "")
        info = {
            "id": id,
            "rarity": rarity,
            "weapon_id": weapon_id,
            "element_id": element_id,
        }

        tags = []
        raw_tags = self.data.get("Tag", {})
        for raw_tag in raw_tags.values():
            tag = {}
            for key in raw_tag.keys():
                tag[key.lower()] = self.cn2tw(raw_tag[key])
            tag["icon"] = tag["icon"].replace(
                "UIResources/Common/Atlas/RoleLabel", "Static"
            )
            tags.append(tag)
        info["tags"] = tags

        info["name"] = self.cn2tw(self.data.get("Name", ""))
        info["nick_name"] = self.cn2tw(self.data.get("NickName", ""))
        info["desc"] = self.cn2tw(self.data.get("Desc", ""))
        info["icon"] = get_icon_fpath(self.data.get("Icon", ""))
        info["background"] = get_icon_fpath(self.data.get("Background", ""))

        # Consume
        total_skill_consume = {}
        info_skill_trees = self.data.get("SkillTrees", {})
        for skill_tree in info_skill_trees.values():
            skill = skill_tree.get("Skill", {})
            skill_type = skill.get("Type", None)
            if skill_type is None:
                skill_tree_consume = skill_tree.get("Consume", {})
                for consume in skill_tree_consume:
                    item_id = consume["Key"]
                    item_value = consume["Value"]

                    item_id_str = str(item_id)
                    item_data = self.items_data.get(item_id_str, {})
                    item_name = self.cn2tw(item_data.get("name", ""))
                    item_icon = get_icon_fpath(item_data.get("icon", ""))

                    if total_skill_consume.get(item_id_str, None) is None:
                        total_skill_consume[item_id_str] = {
                            "id": item_id,
                            "name": item_name,
                            "icon": item_icon,
                            "value": item_value,
                        }
                    else:
                        total_skill_consume[item_id_str]["value"] += item_value
            skill_consume = skill.get("Consume", {})
            for consumes in skill_consume.values():
                for consume in consumes:
                    item_id = consume["Key"]
                    item_value = consume["Value"]

                    item_id_str = str(item_id)
                    item_data = self.items_data.get(item_id_str, {})
                    item_name = self.cn2tw(item_data.get("name", ""))
                    item_icon = get_icon_fpath(item_data.get("icon", ""))

                    if total_skill_consume.get(item_id_str, None) is None:
                        total_skill_consume[item_id_str] = {
                            "id": item_id,
                            "name": item_name,
                            "icon": item_icon,
                            "value": item_value,
                        }
                    else:
                        total_skill_consume[item_id_str]["value"] += item_value
        total_ascension_consume = {}
        info_ascensions = self.data.get("Ascensions", {})
        for ascensions in info_ascensions.values():
            for ascension in ascensions:
                item_id = ascension["Key"]
                item_value = ascension["Value"]

                item_id_str = str(item_id)
                item_data = self.items_data.get(item_id_str, {})
                item_name = self.cn2tw(item_data.get("name", ""))
                item_icon = get_icon_fpath(item_data.get("icon", ""))

                if total_ascension_consume.get(item_id_str, None) is None:
                    total_ascension_consume[item_id_str] = {
                        "id": item_id,
                        "name": item_name,
                        "icon": item_icon,
                        "value": item_value,
                    }
                else:
                    total_ascension_consume[item_id_str]["value"] += item_value
        info["consume"] = {
            "levels": {
                "2": {
                    "id": 2,
                    "name": "貝幣",
                    "icon": "/assets/UI/UIResources/Common/Image/IconA/T_IconA_hsb_UI.webp",
                    "value": 853000,
                }
            },
            "skills": total_skill_consume,
            "ascensions": total_ascension_consume,
        }

        chara_info = self.data.get("CharaInfo", {})
        new_chara_info = {}
        for key, value in chara_info.items():
            new_chara_info[key.lower()] = self.cn2tw(value)
        info["chara_info"] = new_chara_info

        info["stories"] = []
        stories = self.data.get("Stories", [])
        for story in stories:
            new_story = {}
            for key, value in story.items():
                new_story[key.lower()] = self.cn2tw(value)
            info["stories"].append(new_story)

        info["voices"] = []
        voices = self.data.get("Voices", [])
        for voice in voices:
            del voice["Voice"]
            new_voice = {}
            for key, value in voice.items():
                new_voice[key.lower()] = self.cn2tw(value)
            info["voices"].append(new_voice)

        info["goods"] = []
        goods = self.data.get("Goods", [])
        for good in goods:
            new_good = {}
            for key, value in good.items():
                new_good[key.lower()] = self.cn2tw(value)
            new_good["icon"] = get_icon_fpath(new_good["icon"])
            info["goods"].append(new_good)

        special_cook = self.data.get("SpecialCook", {})
        if type(special_cook) != dict:
            special_cook = {}
        info["special_cook"] = {}
        for key, value in special_cook.items():
            info["special_cook"][key.lower()] = self.cn2tw(value)
        if info["special_cook"].get("icon", None) is not None:
            info["special_cook"]["icon"] = get_icon_fpath(info["special_cook"]["icon"])

        info["stats"] = {}
        info["total_exp"] = 0
        stats = self.data.get("Stats", {})
        level_exp = self.data.get("LevelEXP", [])
        level_exp_i = 0
        for levels in stats.values():
            is_first = True
            hp = -float("inf")
            for level, stat in levels.items():
                level_int = int(level)

                new_stat = {}
                for key, value in stat.items():
                    new_key = key.lower()
                    new_stat[new_key] = int(value)
                    if new_key == "life" and value < hp:
                        raise ValueError("HP order error")
                    hp = value
                new_stat["exp"] = level_exp[level_exp_i]
                info["total_exp"] += new_stat["exp"]
                level_exp_i += 1

                if level_int % 10 == 0 and is_first:
                    level += "+"
                info["stats"][level] = new_stat

                is_first = False

        fhome = self.target_path / str(id)
        os.makedirs(fhome, exist_ok=True)

        fpath = fhome / "info.json"
        with fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(info, fp, ensure_ascii=False, indent=4)

    def save_py_attr(self):
        id = self.data.get("Id", None)
        if id is None:
            return

        rows = [["等級", "生命", "攻擊", "防禦"]]
        stats: dict = self.data.get("Stats", None)
        if stats is None:
            return

        for levels in stats.values():
            first = True
            for level, info in levels.items():
                hp = info.get("Life", "")
                atk = info.get("Atk", "")
                defense = info.get("Def", "")

                level_int = int(level)
                hp = f"{int(hp):,}"
                atk = f"{int(atk):,}"
                defense = f"{int(defense):,}"

                if level == "1":
                    rows.append([level, hp, atk, defense])
                elif level_int % 10 == 0:
                    if first:
                        level += "+"
                    rows.append([level, hp, atk, defense])

                first = False

        lines = []
        for row in rows:
            line = "\t".join(row)
            lines.append(line)

        data = "\n".join(lines)
        fhome = self.target_path / str(id)
        os.makedirs(fhome, exist_ok=True)

        fpath = fhome / "屬性.tsv"
        with fpath.open(mode="w", encoding="utf-8") as fp:
            fp.write(data)

    def save_py_skill_info(self):
        id = self.data.get("Id", None)
        if id is None:
            return

        skill_trees: dict = self.data.get("SkillTrees", None)
        if skill_trees is None:
            return

        key_order = [
            "常態攻擊",
            "共鳴技能",
            "共鳴回路",
            "共鳴解放",
            "變奏技能",
            "延奏技能",
            "固有技能1",
            "固有技能2",
            "共鳴鏈1",
            "共鳴鏈2",
            "共鳴鏈3",
            "共鳴鏈4",
            "共鳴鏈5",
            "共鳴鏈6",
        ]

        info_1 = {}

        for skill_tree in skill_trees.values():
            skill_tree_node_type = skill_tree.get("NodeType", None)
            if skill_tree_node_type is None:
                continue
            elif (
                skill_tree_node_type == 1
                or skill_tree_node_type == 2
                or skill_tree_node_type == 3
            ):
                skill = skill_tree.get("Skill", None)
                if skill is None:
                    continue

                skill_name = skill.get("Name", "")
                skill_desc = self.cn2tw(skill.get("Desc", ""))
                skill_param = skill.get("Param", [])
                skill_desc = skill_desc.format(*skill_param)

                skill_list = []
                skill_type = skill.get("Type", None)
                if skill_type is None:
                    continue
                if skill_type == "常态攻击":
                    skill_type = "常態攻擊"
                elif skill_type == "共鸣技能":
                    skill_type = "共鳴技能"
                elif skill_type == "共鸣解放":
                    skill_type = "共鳴解放"
                elif skill_type == "变奏技能":
                    skill_type = "變奏技能"
                elif skill_type == "共鸣回路":
                    skill_type = "共鳴回路"
                elif skill_type == "延奏技能":
                    skill_type = "延奏技能"
                elif skill_type == "固有技能":
                    skill_consumes = skill.get("Consume", {})
                    skill_consume = skill_consumes["1"]
                    for item in skill_consume:
                        if item["Key"] == 2:
                            if item["Value"] == 10000:
                                skill_type = "固有技能1"
                            elif item["Value"] == 20000:
                                skill_type = "固有技能2"
                else:
                    continue
                skill_list = self.get_skill_list(skill)

                info_1[skill_type] = {
                    "名稱": self.cn2tw(skill_name),
                    "描述": skill_desc,
                    "技能列表": skill_list,
                }
                print(skill_type)

        chains: dict = self.data.get("Chains", {})
        for chain_index, chain in chains.items():
            chain_title = f"共鳴鏈{chain_index}"
            chain_name = self.cn2tw(chain.get("Name", ""))
            chain_desc = self.cn2tw(chain.get("Desc", ""))
            chain_param = chain.get("Param", "")
            chain_desc = chain_desc.format(*chain_param)
            info_1[chain_title] = {
                "名稱": chain_name,
                "描述": chain_desc,
            }

        info_2 = {}
        for key in key_order:
            info_2[key] = info_1[key]

        fhome = self.target_path / str(id)
        os.makedirs(fhome, exist_ok=True)

        fpath = fhome / "技能文本.json"
        with fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(info_2, fp, ensure_ascii=False, indent=4)

    def save_py_tsv(self):
        id = self.data.get("Id", None)
        if id is None:
            return

        col_names = [
            "技能加成種類",
            "技能加成種類2",
            "代稱",
            "種類",
            "Entry#",
            "屬性",
            "Type",
            "Base Attribute",
            "LV1",
            "LV2",
            "LV3",
            "LV4",
            "LV5",
            "LV6",
            "LV7",
            "LV8",
            "LV9",
            "LV10",
            "共鳴解放能量",
            "協奏能量",
            "共振度上限",
            "韌性",
            "Coordinated",
            "Type",
        ]
        rows = [col_names]

        skill_trees: dict = self.data.get("SkillTrees", None)
        if skill_trees is None:
            return

        for skill_tree in skill_trees.values():
            skill_tree_node_type = skill_tree.get("NodeType", None)
            if skill_tree_node_type is None:
                continue
            elif skill_tree_node_type == 1 or skill_tree_node_type == 2:
                skill = skill_tree.get("Skill", None)
                if skill is None:
                    continue

                skill_type = skill.get("Type", None)
                if skill_type is None:
                    continue
                if skill_type == "常态攻击":
                    skill_type = "常態攻擊"
                elif skill_type == "共鸣技能":
                    skill_type = "共鳴技能"
                elif skill_type == "共鸣解放":
                    skill_type = "共鳴解放"
                elif skill_type == "变奏技能":
                    skill_type = "變奏技能"
                elif skill_type == "共鸣回路":
                    skill_type = "共鳴回路"
                else:
                    continue
                print(skill_type)

                # 處理補師的治療量轉entry
                lvs = deque([])
                skill_levels: dict = skill.get("Level", {})
                for skill_level in skill_levels.values():
                    skill_level_name = skill_level.get("Name", "")
                    if "治疗量" in skill_level_name:
                        skill_level_param = skill_level.get("Param", None)
                        if len(skill_level_param) != 1:
                            print("Param length != 1")
                        if skill_level_param is not None:
                            lvs.append(skill_level_param[0][:10])

                damage = skill.get("Damage", None)
                if damage is None:
                    continue
                for r4, entry in enumerate(damage.values()):
                    row = [""] * len(col_names)
                    row[3] = skill_type
                    row[4] = str(r4 + 1)

                    entry_element_no = entry.get("Element", "")
                    entry_element = "-"
                    if entry_element_no == 0:
                        entry_element = "-"  # Healing
                    elif entry_element_no == 1:
                        entry_element = "冷凝"
                    elif entry_element_no == 2:
                        entry_element = "熱熔"
                    elif entry_element_no == 3:
                        entry_element = "導電"
                    elif entry_element_no == 4:
                        entry_element = "氣動"
                    elif entry_element_no == 5:
                        entry_element = "衍射"
                    elif entry_element_no == 6:
                        entry_element = "湮滅"
                    row[5] = entry_element

                    if entry_element_no == 0:
                        row[6] = "Healing"
                    elif 7 > entry_element_no > 0:
                        row[6] = "Damage"
                    else:
                        print("Element not between 0~6")
                        continue

                    entry_related_property = entry.get("RelatedProperty", "")
                    if entry_related_property == "攻击":
                        entry_related_property = "攻擊"
                    elif entry_related_property == "生命":
                        entry_related_property = "生命"
                    elif entry_related_property == "防御":
                        entry_related_property = "防禦"
                    else:
                        continue
                    row[7] = entry_related_property

                    entry_type_no = entry.get("Type", "")
                    if entry_type_no == 0:
                        entry_type = "Basic"
                    elif entry_type_no == 1:
                        entry_type = "Heavy"
                    elif entry_type_no == 2:
                        entry_type = "Liberation"
                    elif entry_type_no == 3:
                        entry_type = "Intro"
                    elif entry_type_no == 4:
                        entry_type = "Skill"
                    elif entry_type_no == 5:
                        entry_type = "Echo"
                    elif entry_type_no == 7:
                        entry_type = "Outro"
                    else:
                        entry_type = ""
                    row[23] = entry_type

                    # 共鳴解放能量 = ? / 100
                    entry_energy = entry.get("Energy", "")
                    entry_energy = get_number(entry_energy) / get_number(100.0)
                    entry_energy = f"{entry_energy:,.2f}"
                    row[18] = entry_energy

                    # 協奏能量 = ? / 100
                    entry_element_power = entry.get("ElementPower", "")
                    entry_element_power = get_number(entry_element_power) / get_number(
                        100.0
                    )
                    entry_element_power = f"{entry_element_power:,.2f}"
                    row[19] = entry_element_power

                    # 共振度上限 = ? / 10000
                    entry_hardness_lv = entry.get("HardnessLv", "")
                    entry_hardness_lv = get_number(entry_hardness_lv) / get_number(
                        10000.0
                    )
                    entry_hardness_lv = f"{entry_hardness_lv:,.2f}"
                    row[20] = entry_hardness_lv

                    # 韌性 = ? / 10000
                    entry_tough_lv = entry.get("ToughLv", "")
                    entry_tough_lv = get_number(entry_tough_lv) / get_number(10000.0)
                    entry_tough_lv = f"{entry_tough_lv:,.4f}"
                    row[21] = entry_tough_lv

                    # Levels 8-17
                    if entry_element_no != 0:
                        entry_rate_lvs = entry.get("RateLv", [])
                        if len(entry_rate_lvs) >= 10:
                            for i in range(10):
                                j = i + 8
                                entry_rate_lv = get_number(
                                    entry_rate_lvs[i]
                                ) / get_number(10000.0)
                                entry_rate_lv = f"{entry_rate_lv:.2%}"
                                row[j] = entry_rate_lv
                    elif entry_element_no == 0 and len(lvs) > 0:
                        entry_rate_lvs = lvs.popleft()
                        if entry_rate_lvs:
                            for i in range(10):
                                row[i] = entry_rate_lvs[i]
                    rows.append(row)
                    print(row)

        lines = []
        for row in rows:
            line = "\t".join(row)
            lines.append(line)

        output = "\n".join(lines)
        fhome = self.target_path / str(id)
        os.makedirs(fhome, exist_ok=True)

        fpath = fhome / "技能.tsv"
        with fpath.open(mode="w", encoding="utf-8") as fp:
            fp.write(output)


class HakushEchoes:

    def __init__(
        self,
        source_home: str,
        target: str,
        cn2tw: str,
        monsterinfo: str,
        phantomitem: str,
        phantomskill: str,
        damage: str,
    ):
        self.source_home_path = Path(source_home)
        if not self.source_home_path.exists():
            print(f"{self.source_home_path} not found.")
            return

        self.target_path = Path(target)
        if self.target_path.exists() and not self.target_path.is_dir():
            return

        cn2tw_fpath = Path(cn2tw)
        if cn2tw_fpath.exists():
            with cn2tw_fpath.open(mode="r", encoding="utf-8") as fp:
                self.cn2tw_data = json.load(fp)
        else:
            self.cn2tw_data = {}

        monsterinfo_fpath = Path(monsterinfo)
        self.monsterinfo_data = {}
        if monsterinfo_fpath.exists():
            with monsterinfo_fpath.open(mode="r", encoding="utf-8") as fp:
                monsterinfo_data = json.load(fp)
            for m in monsterinfo_data:
                if self.monsterinfo_data.get(m["Id"], None) is not None:
                    print(m)
                self.monsterinfo_data[m["Id"]] = m

        phantomitem_fpath = Path(phantomitem)
        self.phantomitem_data = {}
        if phantomitem_fpath.exists():
            with phantomitem_fpath.open(mode="r", encoding="utf-8") as fp:
                phantomitem_data = json.load(fp)
            for item in phantomitem_data:
                monster_id = item["MonsterId"]
                skill_id = self.phantomitem_data.get(monster_id, None)
                new_skill_id = item["SkillId"]
                if skill_id is not None and skill_id != new_skill_id:
                    print("phantomitem", monster_id)
                self.phantomitem_data[monster_id] = new_skill_id

        phantomskill_fpath = Path(phantomskill)
        self.phantomskill_data = {}
        if phantomskill_fpath.exists():
            with phantomskill_fpath.open(mode="r", encoding="utf-8") as fp:
                phantomskill_data = json.load(fp)
            for skill in phantomskill_data:
                skill_id = skill["PhantomSkillId"]
                damage_ids = skill["SettleIds"]
                if self.phantomskill_data.get(skill_id, None) is not None:
                    print("phantomskill", skill_id)
                self.phantomskill_data[skill_id] = damage_ids

        damage_fpath = Path(damage)
        self.damage_data = {}
        if damage_fpath.exists():
            with damage_fpath.open(mode="r", encoding="utf-8") as fp:
                damage_data = json.load(fp)
            for damage in damage_data:
                damage_id = damage["Id"]
                self.damage_data[damage_id] = damage

    def get_monster_element_ids(self, id: int):
        info = self.monsterinfo_data.get(id, None)
        if info is None:
            return []
        return info["ElementIdArray"]

    def get_skill_id(self, monster_id: int):
        return self.phantomitem_data.get(monster_id, None)

    def get_damage_ids(self, skill_id: int):
        return self.phantomskill_data.get(skill_id, [])

    def get_damage(self, damage_id: int):
        damage = self.damage_data.get(damage_id, None)
        if damage is None:
            return {}
        return {
            "id": damage["Id"],
            "calculate_type_id": damage[
                "CalculateType"
            ],  # 0: Damage / 1: Healing / 2: ???
            "element_id": damage["Element"],  # 冷凝
            "type_id": damage["Type"],  # 普攻
            "smash_type_id": damage["SmashType"],
            "sub_type_ids": damage["SubType"],
            "cure_base_value": damage["CureBaseValue"],
            "related_property_id": damage["RelatedProperty"],  # 2: 生命 / 10: 防禦
            "rate_lv": damage["RateLv"],
            "energy": damage["Energy"],
            "element_power_type_id": damage["ElementPowerType"],
            "element_power": damage["ElementPower"],
            "hardness_lv": damage["HardnessLv"],
            "tough_lv": damage["ToughLv"],
            "formula_type_id": damage["FormulaType"],  # 1: xxx%+xx
            "immune_type_id": damage["ImmuneType"],
        }

    def cn2tw(self, cn: str) -> str:
        if not cn:
            return cn
        return self.cn2tw_data.get(cn, cn)

    def in_cn2tw(self, cn: str) -> bool:
        found = self.cn2tw_data.get(cn, None)
        return found is not None

    def save(self):
        sonata_table = []
        sonatas = {}
        rows = []
        for echo_fpath in self.source_home_path.glob("*.json"):
            with echo_fpath.open(mode="r", encoding="utf-8") as fp:
                echo_data = json.load(fp)

            id = echo_data["Id"]
            try:
                monster_info = echo_data["MonsterInfo"]
                code = echo_data["Code"]
                name = self.cn2tw(echo_data["Name"])
                type = self.cn2tw(echo_data["Type"])
                intensity = self.cn2tw(echo_data["Intensity"])
                intensity_code = echo_data["IntensityCode"]
                place = self.cn2tw(echo_data["Place"])
                icon = get_icon_fpath(echo_data["Icon"])
                element_ids = self.get_monster_element_ids(monster_info)
                cost = ""
                if intensity == "輕波級":
                    cost = "1"
                elif intensity == "巨浪級":
                    cost = "3"
                elif intensity == "怒濤級":
                    cost = "4"
                elif intensity == "海嘯級":
                    cost = "4"

                groups = echo_data["Group"].values()
                echo_sonatas = []
                echo_groups = []
                for group in groups:
                    group_id = group["Id"]

                    if not self.in_cn2tw(group["Name"]):
                        break
                    group_name = self.cn2tw(group["Name"])
                    if sonatas.get(group_name, None) is None:
                        sonatas[group_name] = {}
                        sonata_table.append((group_id, group_name))

                    group_icon = get_icon_fpath(group["Icon"])
                    group_color = group["Color"]
                    group_new_set = {}
                    group_set = group["Set"]

                    for num, s in group_set.items():
                        group_desc = self.cn2tw(s["Desc"])
                        group_param = s["Param"]
                        group_new_set[num] = {"desc": group_desc, "param": group_param}

                        if sonatas[group_name].get(num, None) is None:
                            sonatas[group_name][num] = group_desc

                    echo_sonatas.append(group_name)
                    new_group = {
                        "id": group_id,
                        "name": group_name,
                        "icon": group_icon,
                        "color": group_color,
                        "set": group_new_set,
                    }
                    echo_groups.append(new_group)
                else:
                    format_skill_desc = self.cn2tw(echo_data["Skill"]["Desc"])
                    skill_simple_desc = self.cn2tw(echo_data["Skill"]["SimpleDesc"])
                    skill_params = echo_data["Skill"]["Param"]
                    skill_param = skill_params[0]
                    for i in range(1, len(skill_params)):
                        next_skill_param = skill_params[i]
                        for j in range(len(skill_param)):
                            if skill_param[j] != next_skill_param[j]:
                                skill_param[j] += f"/{next_skill_param[j]}"
                    skill_desc = format_skill_desc.format(*skill_param)

                    # Skill ID
                    skill_id = self.get_skill_id(id)
                    echo_skill_damages = []
                    damage_ids = self.get_damage_ids(skill_id)
                    for damage_id in damage_ids:
                        echo_skill_damage = self.get_damage(damage_id)
                        echo_skill_damages.append(echo_skill_damage)

                    row = {
                        "id": id,
                        "monster_info": monster_info,
                        "skill_id": skill_id,
                        "damage_ids": damage_ids,
                        "damage": echo_skill_damages,
                        "code": code,
                        "name": name,
                        "type": type,
                        "element_ids": element_ids,
                        "cost": cost,
                        "intensity": intensity,
                        "intensity_code": intensity_code,
                        "place": place,
                        "icon": icon,
                        "sonatas": echo_sonatas,
                        "skill": {
                            "description": skill_desc,
                            "desc": format_skill_desc,
                            "simple_desc": skill_simple_desc,
                            "param": skill_params,
                        },
                        "groups": echo_groups,
                    }
                    rows.append(row)
            except:
                print(id)
                return

        sonata_table.sort(key=lambda sonata: sonata[0])
        new_sonatas = {}
        for _, sonata_name in sonata_table:
            new_sonatas[sonata_name] = sonatas[sonata_name]

        os.makedirs(self.target_path, exist_ok=True)

        rows_fpath = self.target_path / "infos.json"
        with rows_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(rows, fp, ensure_ascii=False, indent=4)

        sonatas_fpath = self.target_path / "sonatas.json"
        with sonatas_fpath.open(mode="w", encoding="utf-8") as fp:
            json.dump(new_sonatas, fp, ensure_ascii=False, indent=4)
