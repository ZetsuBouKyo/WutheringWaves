from enum import Enum


class ResonatorBuffEnum(str, Enum):
    ID: str = "代稱"
    RESONATOR_NAME: str = "角色"
    SOURCE: str = "來源"
    TYPE: str = "增益種類"
    ELEMENT: str = "增益屬性"
    SKILL_TYPE: str = "技能加成種類"
    OBJECT: str = "對象"
    VALUE: str = "數值"
    DURATION: str = "持續時間(s)"


class WeaponBuffEnum(str, Enum):
    ID: str = "代稱"
    WEAPON_NAME: str = "武器"
    TYPE: str = "增益種類"
    ELEMENT: str = "增益屬性"
    SKILL_TYPE: str = "技能加成種類"
    VALUE: str = "數值"
    DURATION: str = "持續時間(s)"


class EchoBuffEnum(str, Enum):
    ID: str = "代稱"
    ECHO_NAME: str = "聲骸"
    TYPE: str = "增益種類"
    ELEMENT: str = "增益屬性"
    SKILL_TYPE: str = "技能加成種類"
    OBJECT: str = "對象"
    VALUE: str = "數值"
    DURATION: str = "持續時間(s)"


class EchoSonataBuffEnum(str, Enum):
    ID: str = "代稱"
    ECHO_SONATA_NAME: str = "合鳴"
    TYPE: str = "增益種類"
    ELEMENT: str = "增益屬性"
    SKILL_TYPE: str = "技能加成種類"
    OBJECT: str = "對象"
    VALUE: str = "數值"
    DURATION: str = "持續時間(s)"
