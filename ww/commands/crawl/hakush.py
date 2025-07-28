import json
import os
from collections import deque
from pathlib import Path

from ww.utils.number import get_number


class HakushResonator:
    def __init__(self, source: str, target: str):
        source_path = Path(source)
        if not source_path.exists():
            print(f"{source} not found.")
            return

        self.target_path = Path(target)
        if self.target_path.exists() and not self.target_path.is_dir():
            return

        with source_path.open(mode="r", encoding="utf-8") as fp:
            self.data = json.load(fp)

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
                skill_desc = skill.get("Desc", "")

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
                info_1[skill_type] = {
                    "名稱": skill_name,
                    "描述": skill_desc,
                }
                print(skill_type)

        chains: dict = self.data.get("Chains", {})
        for chain_index, chain in chains.items():
            chain_title = f"共鳴鏈{chain_index}"
            chain_name = chain.get("Name", "")
            chain_desc = chain.get("Desc", "")
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
                    elif entry_element_no == 0:
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
