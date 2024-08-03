from enum import Enum

BUFF_ID: str = "代稱"
BUFF_NAME: str = "名稱"
BUFF_SUFFIX: str = "字尾"
BUFF_SOURCE: str = "來源"
BUFF_TYPE: str = "增益種類"
BUFF_ELEMENT: str = "增益屬性"
BUFF_SKILL_TYPE: str = "技能加成種類"
BUFF_OBJECT: str = "對象"
BUFF_VALUE: str = "數值"
BUFF_DURATION: str = "持續時間(s)"


class ResonatorBuffEnum(str, Enum):
    ID: str = BUFF_ID
    NAME: str = BUFF_NAME
    SUFFIX: str = BUFF_SUFFIX
    SOURCE: str = BUFF_SOURCE
    TYPE: str = BUFF_TYPE
    ELEMENT: str = BUFF_ELEMENT
    SKILL_TYPE: str = BUFF_SKILL_TYPE
    OBJECT: str = BUFF_OBJECT
    VALUE: str = BUFF_VALUE
    DURATION: str = BUFF_DURATION


class WeaponBuffEnum(str, Enum):
    ID: str = BUFF_ID
    NAME: str = BUFF_NAME
    SUFFIX: str = BUFF_SUFFIX
    TYPE: str = BUFF_TYPE
    ELEMENT: str = BUFF_ELEMENT
    SKILL_TYPE: str = BUFF_SKILL_TYPE
    VALUE: str = BUFF_VALUE
    DURATION: str = BUFF_DURATION


class EchoBuffEnum(str, Enum):
    ID: str = BUFF_ID
    NAME: str = BUFF_NAME
    SUFFIX: str = BUFF_SUFFIX
    TYPE: str = BUFF_TYPE
    ELEMENT: str = BUFF_ELEMENT
    SKILL_TYPE: str = BUFF_SKILL_TYPE
    OBJECT: str = BUFF_OBJECT
    VALUE: str = BUFF_VALUE
    DURATION: str = BUFF_DURATION


class EchoSonataBuffEnum(str, Enum):
    ID: str = BUFF_ID
    NAME: str = BUFF_NAME
    SUFFIX: str = BUFF_SUFFIX
    TYPE: str = BUFF_TYPE
    ELEMENT: str = BUFF_ELEMENT
    SKILL_TYPE: str = BUFF_SKILL_TYPE
    OBJECT: str = BUFF_OBJECT
    VALUE: str = BUFF_VALUE
    DURATION: str = BUFF_DURATION
