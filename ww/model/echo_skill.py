from enum import Enum


class EchoSkillEnum(str, Enum):
    SKILL_ID: str = "代稱"
    SKILL_ELEMENT: str = "屬性"
    SKILL_DMG: str = "倍率"
