from enum import Enum
from typing import Union

from html2text import html2text
from lxml import html
from rich.console import Console
from rich.rule import Rule
from rich.style import Style
from rich.text import Text

from ww.commands.crawl.utils import clear_text
from ww.locale import ZhTwEnum, _


def print_divider(
    title: Union[str, Text] = "",
    characters: str = "─",
    text_style: Union[str, Style] = "",
    rule_style: Union[str, Style] = "rule.line",
):
    if type(title) is str:
        title = Text(text=title, style=text_style)

    console = Console()
    console.print(
        Rule(
            title=title,
            characters=characters,
            style=rule_style,
        )
    )


class _ResonatorSkillEnum(str, Enum):
    NORMAL_ATTACK: str = "常态攻击"
    RESONANCE_SKILL: str = "共鸣技能"
    FORTE_CIRCUIT: str = "共鸣回路"
    RESONANCE_LIBERATION: str = "共鸣解放"
    INTRO_SKILL: str = "变奏技能"
    OUTRO_SKILL: str = "延奏技能"


_skill_table = {
    _ResonatorSkillEnum.NORMAL_ATTACK.value: _(ZhTwEnum.NORMAL_ATTACK),
    _ResonatorSkillEnum.RESONANCE_SKILL.value: _(ZhTwEnum.RESONANCE_SKILL),
    _ResonatorSkillEnum.FORTE_CIRCUIT.value: _(ZhTwEnum.FORTE_CIRCUIT),
    _ResonatorSkillEnum.RESONANCE_LIBERATION.value: _(ZhTwEnum.RESONANCE_LIBERATION),
    _ResonatorSkillEnum.INTRO_SKILL.value: _(ZhTwEnum.INTRO_SKILL),
    _ResonatorSkillEnum.OUTRO_SKILL.value: _(ZhTwEnum.OUTRO_SKILL),
}

_chain_table = {
    1: _(ZhTwEnum.CHAIN_1),
    2: _(ZhTwEnum.CHAIN_2),
    3: _(ZhTwEnum.CHAIN_3),
    4: _(ZhTwEnum.CHAIN_4),
    5: _(ZhTwEnum.CHAIN_5),
    6: _(ZhTwEnum.CHAIN_6),
}


class ResonatorParser:
    def __init__(self, html_str: str):
        self.html_str = html_str
        self.tree = html.fromstring(self.html_str)
        self.data = {}

    def get_skill_pattern(self, skill: _ResonatorSkillEnum) -> str:
        skill = skill.value
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{skill}:")]/parent::*/following-sibling::div[@class="skilldescription"]'

    def get_skill_name_pattern(self, skill: _ResonatorSkillEnum) -> str:
        skill = skill.value
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{skill}:")]'

    def get_skill(self, skill: _ResonatorSkillEnum):
        print(skill.value)

        self.data[_skill_table[skill.value]] = {}

        skill_name_pattern = self.get_skill_name_pattern(skill)
        skill_name_elements = self.tree.xpath(skill_name_pattern)
        if skill_name_elements:
            skill_length = len(skill_name_elements)
            if skill_length != 1:
                print(f"Elements: {skill_length}")
                return
            for element in skill_name_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                skill_name = clear_text(h_text)
                skill_name = skill_name.replace(f"{skill.value}: ", "")

                print(skill_name)
                self.data[_skill_table[skill.value]][_(ZhTwEnum.NAME)] = skill_name

        skill_pattern = self.get_skill_pattern(skill)
        skill_elements = self.tree.xpath(skill_pattern)
        if skill_elements:
            skill_length = len(skill_elements)
            if skill_length != 1:
                print(f"Elements: {skill_length}")
                return
            for element in skill_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                skill_description = clear_text(h_text)
                print(skill_description)
                self.data[_skill_table[skill.value]][
                    _(ZhTwEnum.DESCRIPTION)
                ] = skill_description
                print_divider()

    def get_skills(self):
        for e in _ResonatorSkillEnum:
            self.get_skill(e)

    def get_chain_prefix(self, num: int) -> str:
        return f"Sequence Node {num}: "

    def get_chain_name_pattern(self, chain_prefix: str) -> str:
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{chain_prefix}")]'

    def get_chain_pattern(self, chain_prefix: str) -> str:
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{chain_prefix}")]/parent::*/following-sibling::span[@class="skilldescription"]'

    def get_chain(self, num: int):
        chain_prefix = self.get_chain_prefix(num)

        self.data[_chain_table[num]] = {}

        chain_name_pattern = self.get_chain_name_pattern(chain_prefix)
        chain_name_elements = self.tree.xpath(chain_name_pattern)
        if chain_name_elements:
            element_length = len(chain_name_elements)
            if element_length != 1:
                print(f"Elements: {element_length}")
                return
            for element in chain_name_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)
                h_text = h_text.replace(chain_prefix, "")

                print(h_text)
                self.data[_chain_table[num]][_(ZhTwEnum.NAME)] = h_text

        chain_pattern = self.get_chain_pattern(chain_prefix)
        chain_elements = self.tree.xpath(chain_pattern)
        if chain_elements:
            element_length = len(chain_elements)
            if element_length != 1:
                print(f"Elements: {element_length}")
                return
            for element in chain_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)
                print(h_text)
                self.data[_chain_table[num]][_(ZhTwEnum.DESCRIPTION)] = h_text
                print_divider()

    def get_chains(self):
        for i in range(1, 7):
            self.get_chain(i)

    def get_inherent_skill_name_pattern(self, prefix: str) -> str:
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{prefix}")]'

    def get_inherent_skill_pattern(self, prefix: str) -> str:
        return f'//span[@class="skillname-container"]/span[@class="skillname" and starts-with(text(), "{prefix}")]/parent::*/following-sibling::div[@class="skilldescription"]'

    def get_inherent_skills(self):
        prefix = "固有技能: "
        name_pattern = self.get_inherent_skill_name_pattern(prefix)
        name_elements = self.tree.xpath(name_pattern)
        names = []
        if name_elements:
            element_length = len(name_elements)
            if element_length != 1:
                print(f"Elements: {element_length}")

            for element in name_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)
                h_text = h_text.replace(prefix, "")
                names.append(h_text)

        skill_pattern = self.get_inherent_skill_pattern(prefix)
        skill_elements = self.tree.xpath(skill_pattern)
        skills = []
        if skill_elements:
            element_length = len(skill_elements)
            if element_length != 1:
                print(f"Elements: {element_length}")

            for element in skill_elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)
                skills.append(h_text)

        self.data[_(ZhTwEnum.INHERENT_SKILL_1)] = {
            _(ZhTwEnum.NAME): names[0],
            _(ZhTwEnum.DESCRIPTION): skills[0],
        }
        self.data[_(ZhTwEnum.INHERENT_SKILL_2)] = {
            _(ZhTwEnum.NAME): names[1],
            _(ZhTwEnum.DESCRIPTION): skills[1],
        }

    def get_data(self) -> str:
        self.get_skills()
        self.get_chains()
        self.get_inherent_skills()
        return self.data
