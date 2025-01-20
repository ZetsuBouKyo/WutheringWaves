from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from ww.locale import ZhTwEnum, _


class EchoTsvColumnEnum(str, Enum):
    PRIMARY_KEY: str = "名稱"
    COST: str = "COST"


class EchoSkillTsvColumnEnum(str, Enum):
    PRIMARY_KEY: str = "代稱"
    ELEMENT: str = "屬性"
    BASE_ATTRIBUTE: str = "Base Attribute"
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
    FROSTY_RESOLVE: str = "凌冽決斷之心"
    ETERNAL_RADIANCE: str = "此間永駐之光"
    MIDNIGHT_VEIL: str = "幽夜隱匿之帷"
    EMPYREAN_ANTHEM: str = "高天共奏之曲"
    TIDEBREAKING_COURAGE: str = "無懼浪濤之勇"


class ResonatorEchoTsvColumnEnum(str, Enum):
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
    MAIN_HEALING_BONUS: str = "[主]治療加成"

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


def get_resonator_echo_main_dmg_bonus(
    element: str, e: ResonatorEchoTsvColumnEnum = ResonatorEchoTsvColumnEnum
) -> str:
    bonus = f"[主]{element}加成"
    assert bonus in [
        e.MAIN_GLACIO_DMG_BONUS.value,
        e.MAIN_FUSION_DMG_BONUS.value,
        e.MAIN_ELECTRO_DMG_BONUS.value,
        e.MAIN_AERO_DMG_BONUS.value,
        e.MAIN_SPECTRO_DMG_BONUS.value,
        e.MAIN_HAVOC_DMG_BONUS.value,
    ]
    return bonus


class EchoesModelEnum(str, Enum):
    AFFIXES_15_1: str = _(ZhTwEnum.ECHOES_AFFIXES_15_1)
    AFFIXES_20_SMALL: str = _(ZhTwEnum.ECHOES_AFFIXES_20_SMALL)
    AFFIXES_20_BASIC_ATK: str = _(ZhTwEnum.ECHOES_AFFIXES_20_BASIC_ATK)
    AFFIXES_20_HEAVY_ATK: str = _(ZhTwEnum.ECHOES_AFFIXES_20_HEAVY_ATK)
    AFFIXES_20_RESONANCE_SKILL: str = _(ZhTwEnum.ECHOES_AFFIXES_20_RESONANCE_SKILL)
    AFFIXES_20_RESONANCE_LIBERATION: str = _(
        ZhTwEnum.ECHOES_AFFIXES_20_RESONANCE_LIBERATION
    )


class EchoModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    cost: Optional[int] = None
    sonatas: List[EchoSonataEnum] = []


class EchoMainAffixModel(BaseModel):
    hp: Decimal = Decimal(0.0)
    hp_p: Decimal = Decimal(0.0)
    atk: Decimal = Decimal(0.0)
    atk_p: Decimal = Decimal(0.0)
    def_p: Decimal = Decimal(0.0)

    crit_rate: Decimal = Decimal(0.0)
    crit_dmg: Decimal = Decimal(0.0)

    glacio: Decimal = Decimal(0.0)
    fusion: Decimal = Decimal(0.0)
    electro: Decimal = Decimal(0.0)
    aero: Decimal = Decimal(0.0)
    spectro: Decimal = Decimal(0.0)
    havoc: Decimal = Decimal(0.0)

    healing: Decimal = Decimal(0.0)
    energy_regen: Decimal = Decimal(0.0)


class EchoMainAffixesModel(BaseModel):
    cost_4: EchoMainAffixModel = EchoMainAffixModel()
    cost_3: EchoMainAffixModel = EchoMainAffixModel()
    cost_1: EchoMainAffixModel = EchoMainAffixModel()


class EchoSubAffixesModel(BaseModel):
    hp: List[Decimal] = []
    hp_p: List[Decimal] = []
    atk: List[Decimal] = []
    atk_p: List[Decimal] = []
    def_: List[Decimal] = []
    def_p: List[Decimal] = []

    crit_rate: List[Decimal] = []
    crit_dmg: List[Decimal] = []

    resonance_skill: List[Decimal] = []
    basic_attack: List[Decimal] = []
    heavy_attack: List[Decimal] = []
    resonance_liberation: List[Decimal] = []

    energy_regen: List[Decimal] = []
