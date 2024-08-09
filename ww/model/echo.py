from enum import Enum


class EchoListEnum(str, Enum):
    PRIMARY_KEY: str = "名稱"
    COST: str = "COST"


class EchoSkillEnum(str, Enum):
    PRIMARY_KEY: str = "代稱"
    ELEMENT: str = "屬性"
    DMG: str = "倍率"


class EchoSonataEnum(str, Enum):
    LINGERING_TUNES: str = "不絕餘音"
    MOONLIT_CLOUDS: str = "輕雲出月"
    FREEZING_FROST: str = "凝夜白霜"
    MOLTEN_RIFT: str = "熔山裂谷"
    VOID_THUNDER: str = "徹空冥雷"
    SIERRA_GALE: str = "嘯谷長風"
    CELESTIAL_LIGHT: str = "浮星祛暗"
    SUN_SINKING_ECLIPSE: str = "沉日劫明"
    REJUVENATING_GLOW: str = "隱世回光"


class EchoesEnum(str, Enum):
    ID: str = "代稱"
    COST: str = "COST"
    PREFIX: str = "字首"
    SUFFIX: str = "字尾"
    NAME: str = "名稱"
    ELEMENT: str = "屬性"
    ECHO_SONATA: str = "合鳴效果"

    MAIN_HP: str = "[主]生命"
    MAIN_ATK: str = "[主]攻擊"
    MAIN_HP_P: str = "[主]生命百分比"
    MAIN_ATK_P: str = "[主]攻擊百分比"
    MAIN_DEF_P: str = "[主]防禦百分比"
    MAIN_CRIT_RATE: str = "[主]暴擊"
    MAIN_CRIT_DMG: str = "[主]暴擊傷害"
    MAIN_ENERGY_REGEN: str = "[主]共鳴效率"

    MAIN_GLACIO_DMG_BONUS: str = "[主]冷凝加成"
    MAIN_FUSION_DMG_BONUS: str = "[主]熱熔加成"
    MAIN_ELECTRO_DMG_BONUS: str = "[主]導電加成"
    MAIN_AERO_DMG_BONUS: str = "[主]氣動加成"
    MAIN_SPECTRO_DMG_BONUS: str = "[主]衍射加成"
    MAIN_HAVOC_DMG_BONUS: str = "[主]湮滅加成"
    MAIN_HEALING_BONUS: str = "[主]治療效果加成百分比"

    SUB_HP: str = "[副]生命"
    SUB_HP_P: str = "[副]生命百分比"
    SUB_ATK: str = "[副]攻擊"
    SUB_ATK_P: str = "[副]攻擊百分比"
    SUB_DEF: str = "[副]防禦"
    SUB_DEF_P: str = "[副]防禦百分比"
    SUB_CRIT_RATE: str = "[副]暴擊"
    SUB_CRIT_DMG: str = "[副]暴擊傷害"
    SUB_ENERGY_REGEN: str = "[副]共鳴效率"

    SUB_RESONANCE_SKILL_DMG_BONUS = "[副]共鳴技能傷害加成"
    SUB_BASIC_ATTACK_DMG_BONUS = "[副]普攻傷害加成"
    SUB_HEAVY_ATTACK_DMG_BONUS = "[副]重擊傷害加成"
    SUB_RESONANCE_LIBERATION_DMG_BONUS = "[副]共鳴解放傷害加成"
