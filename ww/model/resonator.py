from decimal import Decimal
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict

from ww.locale import ZhTwEnum, _
from ww.model.element import ElementEnum
from ww.model.resonator_skill import ResonatorSkillBonusTypeEnum
from ww.utils.number import get_number

ResonatorID = str
ResonatorName = str


class ResonatorStatTsvColumnEnum(str, Enum):
    LEVEL: str = _(ZhTwEnum.LEVEL)
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)


class ResonatorTsvColumnEnum(str, Enum):
    ID: str = "角色代稱"
    PREFIX: str = "字首"
    SUFFIX: str = "字尾"
    NAME: str = "角色名稱"

    WEAPON_NAME: str = "武器名稱"
    WEAPON_LEVEL: str = "武器等級"
    WEAPON_RANK: str = "武器諧振"

    LEVEL: str = "角色等級"
    RESONANCE_CHAIN: str = "共鳴鏈"
    MAX_STA: str = "耐力上限"

    NORMAL_ATTACK_LV: str = "常態攻擊LV"
    RESONANCE_SKILL_LV: str = "共鳴技能LV"
    RESONANCE_LIBERATION_LV: str = "共鳴解放LV"
    FORTE_CIRCUIT_LV: str = "共鳴回路LV"
    INTRO_SKILL_LV: str = "變奏技能LV"
    OUTRO_SKILL_LV: str = "延奏技能LV"

    STAT_BONUS_HP_P: str = "生命百分比"
    STAT_BONUS_ATK_P: str = "攻擊百分比"
    STAT_BONUS_DEF_P: str = "防禦百分比"
    STAT_BONUS_CRIT_RATE: str = "暴擊"
    STAT_BONUS_CRIT_DMG: str = "暴擊傷害"

    STAT_BONUS_GLACIO_DMG_BONUS: str = "冷凝加成"
    STAT_BONUS_FUSION_DMG_BONUS: str = "熱熔加成"
    STAT_BONUS_ELECTRO_DMG_BONUS: str = "導電加成"
    STAT_BONUS_AERO_DMG_BONUS: str = "氣動加成"
    STAT_BONUS_SPECTRO_DMG_BONUS: str = "衍射加成"
    STAT_BONUS_HAVOC_DMG_BONUS: str = "湮滅加成"
    STAT_BONUS_HEALING_BONUS: str = "治療效果加成"

    STAT_BONUS_RESONANCE_SKILL_BONUS: str = "共鳴技能加成"
    STAT_BONUS_BASIC_ATTACK_BONUS: str = "普攻加成"
    STAT_BONUS_HEAVY_ATTACK_BONUS: str = "重擊加成"
    STAT_BONUS_RESONANCE_LIBERATION_BONUS: str = "共鳴解放加成"

    INHERENT_SKILL_1: str = "固有一階"
    INHERENT_SKILL_2: str = "固有二階"

    STAT_BONUS_PHYSICAL_DMG_RES: str = "物理抗性"
    STAT_BONUS_GLACIO_DMG_RES: str = "冷凝抗性"
    STAT_BONUS_FUSION_DMG_RES: str = "熱熔抗性"
    STAT_BONUS_ELECTRO_DMG_RES: str = "導電抗性"
    STAT_BONUS_AERO_DMG_RES: str = "氣動抗性"
    STAT_BONUS_SPECTRO_DMG_RES: str = "衍射抗性"
    STAT_BONUS_HAVOC_DMG_RES: str = "湮滅抗性"

    ECHO_1: str = "聲骸1"
    ECHO_2: str = "聲骸2"
    ECHO_3: str = "聲骸3"
    ECHO_4: str = "聲骸4"
    ECHO_5: str = "聲骸5"


class ResonatorTsvModel(BaseModel):
    id: str = "角色代稱"
    prefix: str = "字首"
    suffix: str = "字尾"
    name: str = "角色名稱"

    weapon_name: str = "武器名稱"
    weapon_level: str = "武器等級"
    weapon_rank: str = "武器諧振"

    level: str = "角色等級"
    resonance_chain: str = "共鳴鏈"
    max_sta: str = "耐力上限"

    normal_attack_lv: str = "常態攻擊lv"
    resonance_skill_lv: str = "共鳴技能lv"
    resonance_liberation_lv: str = "共鳴解放lv"
    forte_circuit_lv: str = "共鳴回路lv"
    intro_skill_lv: str = "變奏技能lv"
    outro_skill_lv: str = "延奏技能lv"

    stat_bonus_hp_p: str = "生命百分比"
    stat_bonus_atk_p: str = "攻擊百分比"
    stat_bonus_def_p: str = "防禦百分比"
    stat_bonus_crit_rate: str = "暴擊"
    stat_bonus_crit_dmg: str = "暴擊傷害"

    stat_bonus_glacio_dmg_bonus: str = "冷凝加成"
    stat_bonus_fusion_dmg_bonus: str = "熱熔加成"
    stat_bonus_electro_dmg_bonus: str = "導電加成"
    stat_bonus_aero_dmg_bonus: str = "氣動加成"
    stat_bonus_spectro_dmg_bonus: str = "衍射加成"
    stat_bonus_havoc_dmg_bonus: str = "湮滅加成"
    stat_bonus_healing_bonus: str = "治療效果加成"

    stat_bonus_resonance_skill_bonus: str = "共鳴技能加成"
    stat_bonus_basic_attack_bonus: str = "普攻加成"
    stat_bonus_heavy_attack_bonus: str = "重擊加成"
    stat_bonus_resonance_liberation_bonus: str = "共鳴解放加成"

    inherent_skill_1: str = "固有一階"
    inherent_skill_2: str = "固有二階"

    stat_bonus_physical_dmg_res: str = "物理抗性"
    stat_bonus_glacio_dmg_res: str = "冷凝抗性"
    stat_bonus_fusion_dmg_res: str = "熱熔抗性"
    stat_bonus_electro_dmg_res: str = "導電抗性"
    stat_bonus_aero_dmg_res: str = "氣動抗性"
    stat_bonus_spectro_dmg_res: str = "衍射抗性"
    stat_bonus_havoc_dmg_res: str = "湮滅抗性"

    echo_1: str = "聲骸1"
    echo_2: str = "聲骸2"
    echo_3: str = "聲骸3"
    echo_4: str = "聲骸4"
    echo_5: str = "聲骸5"


CALCULATED_RESONATORS_DMG_BONUS_PREFIX: str = "角色"
CALCULATED_RESONATORS_DMG_BONUS_SUFFIX: str = "傷害加成面板"


class CalculatedResonatorTsvColumnEnum(str, Enum):
    ID: str = _(ZhTwEnum.RESONATOR_ID)
    NAME: str = _(ZhTwEnum.RESONATOR_NAME)

    # Resonator Stat
    HP: str = _(ZhTwEnum.RESONATOR_HP)
    ATTACK: str = _(ZhTwEnum.RESONATOR_ATK)
    DEFENSE: str = _(ZhTwEnum.RESONATOR_DEF)

    # Resonator Base Stat
    BASE_CRIT_RATE: str = _(ZhTwEnum.RESONATOR_BASE_CRIT_RATE)
    BASE_CRIT_DMG: str = _(ZhTwEnum.RESONATOR_BASE_CRIT_DMG)
    BASE_ENERGY_REGEN: str = _(ZhTwEnum.RESONATOR_BASE_ENERGY_REGEN)

    # Calculated
    CALCULATED_HP: str = _(ZhTwEnum.CALCULATED_RESONATOR_HP)
    CALCULATED_HP_P: str = _(ZhTwEnum.CALCULATED_RESONATOR_HP_P)
    CALCULATED_ATK: str = _(ZhTwEnum.CALCULATED_RESONATOR_ATK)
    CALCULATED_ATK_P: str = _(ZhTwEnum.CALCULATED_RESONATOR_ATK_P)
    CALCULATED_DEF: str = _(ZhTwEnum.CALCULATED_RESONATOR_DEF)
    CALCULATED_DEF_P: str = _(ZhTwEnum.CALCULATED_RESONATOR_DEF_P)
    CALCULATED_CRIT_RATE: str = _(ZhTwEnum.CALCULATED_RESONATOR_CRIT_RATE)
    CALCULATED_CRIT_DMG: str = _(ZhTwEnum.CALCULATED_RESONATOR_CRIT_DMG)
    CALCULATED_ENERGY_REGEN: str = _(ZhTwEnum.CALCULATED_RESONATOR_ENERGY_REGEN)

    CALCULATED_RESONANCE_SKILL_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_RESONANCE_SKILL_DMG_BONUS
    )
    CALCULATED_BASIC_ATTACK_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_BASIC_ATTACK_DMG_BONUS
    )
    CALCULATED_HEAVY_ATTACK_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_HEAVY_ATTACK_DMG_BONUS
    )
    CALCULATED_RESONANCE_LIBERATION_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_RESONANCE_LIBERATION_DMG_BONUS
    )

    CALCULATED_PHYSICAL_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_PHYSICAL_DMG_BONUS
    )
    CALCULATED_GLACIO_DMG_BONUS: str = _(ZhTwEnum.CALCULATED_RESONATOR_GLACIO_DMG_BONUS)
    CALCULATED_FUSION_DMG_BONUS: str = _(ZhTwEnum.CALCULATED_RESONATOR_FUSION_DMG_BONUS)
    CALCULATED_ELECTRO_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_ELECTRO_DMG_BONUS
    )
    CALCULATED_AERO_DMG_BONUS: str = _(ZhTwEnum.CALCULATED_RESONATOR_AERO_DMG_BONUS)
    CALCULATED_SPECTRO_DMG_BONUS: str = _(
        ZhTwEnum.CALCULATED_RESONATOR_SPECTRO_DMG_BONUS
    )
    CALCULATED_HAVOC_DMG_BONUS: str = _(ZhTwEnum.CALCULATED_RESONATOR_HAVOC_DMG_BONUS)

    CALCULATED_PHYSICAL_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_PHYSICAL_DMG_RES)
    CALCULATED_GLACIO_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_GLACIO_DMG_RES)
    CALCULATED_FUSION_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_FUSION_DMG_RES)
    CALCULATED_ELECTRO_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_ELECTRO_DMG_RES)
    CALCULATED_AERO_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_AERO_DMG_RES)
    CALCULATED_SPECTRO_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_SPECTRO_DMG_RES)
    CALCULATED_HAVOC_DMG_RES: str = _(ZhTwEnum.CALCULATED_RESONATOR_HAVOC_DMG_RES)

    CALCULATED_HEALING_BONUS: str = _(ZhTwEnum.CALCULATED_RESONATOR_HEALING_BONUS)

    # Weapon
    WEAPON_ATK: str = _(ZhTwEnum.RESONATOR_WEAPON_ATK)
    WEAPON_HP_P: str = _(ZhTwEnum.RESONATOR_WEAPON_HP_P)
    WEAPON_ATK_P: str = _(ZhTwEnum.RESONATOR_WEAPON_ATK_P)
    WEAPON_DEF_P: str = _(ZhTwEnum.RESONATOR_WEAPON_DEF_P)
    WEAPON_CRIT_RATE: str = _(ZhTwEnum.RESONATOR_WEAPON_CRIT_RATE)
    WEAPON_CRIT_DMG: str = _(ZhTwEnum.RESONATOR_WEAPON_CRIT_DMG)
    WEAPON_ENERGY_REGEN: str = _(ZhTwEnum.RESONATOR_WEAPON_ENERGY_REGEN)

    WEAPON_RANK_ATK_P: str = _(ZhTwEnum.RESONATOR_WEAPON_RANK_ATK_P)
    WEAPON_RANK_HP_P: str = _(ZhTwEnum.RESONATOR_WEAPON_RANK_HP_P)
    WEAPON_RANK_ENERGY_REGEN: str = _(ZhTwEnum.RESONATOR_WEAPON_RANK_ENERGY_REGEN)
    WEAPON_RANK_ATTRIBUTE_DMG_BONUS: str = _(
        ZhTwEnum.RESONATOR_WEAPON_RANK_ATTRIBUTE_DMG_BONUS
    )

    # Echo
    ECHO_1: str = _(ZhTwEnum.RESONATOR_ECHO_1)
    ECHO_SONATA_1: str = _(ZhTwEnum.RESONATOR_ECHO_SONATA_1)
    ECHO_2: str = _(ZhTwEnum.RESONATOR_ECHO_2)
    ECHO_SONATA_2: str = _(ZhTwEnum.RESONATOR_ECHO_SONATA_2)
    ECHO_3: str = _(ZhTwEnum.RESONATOR_ECHO_3)
    ECHO_SONATA_3: str = _(ZhTwEnum.RESONATOR_ECHO_SONATA_3)
    ECHO_4: str = _(ZhTwEnum.RESONATOR_ECHO_4)
    ECHO_SONATA_4: str = _(ZhTwEnum.RESONATOR_ECHO_SONATA_4)
    ECHO_5: str = _(ZhTwEnum.RESONATOR_ECHO_5)
    ECHO_SONATA_5: str = _(ZhTwEnum.RESONATOR_ECHO_SONATA_5)

    ECHO_HP: str = _(ZhTwEnum.RESONATOR_ECHO_HP)
    ECHO_HP_P: str = _(ZhTwEnum.RESONATOR_ECHO_HP_P)
    ECHO_ATK: str = _(ZhTwEnum.RESONATOR_ECHO_ATK)
    ECHO_ATK_P: str = _(ZhTwEnum.RESONATOR_ECHO_ATK_P)
    ECHO_DEF: str = _(ZhTwEnum.RESONATOR_ECHO_DEF)
    ECHO_DEF_P: str = _(ZhTwEnum.RESONATOR_ECHO_DEF_P)
    ECHO_CRIT_RATE: str = _(ZhTwEnum.RESONATOR_ECHO_CRIT_RATE)
    ECHO_CRIT_DMG: str = _(ZhTwEnum.RESONATOR_ECHO_CRIT_DMG)
    ECHO_ENERGY_REGEN: str = _(ZhTwEnum.RESONATOR_ECHO_ENERGY_REGEN)

    ECHO_RESONANCE_SKILL_DMG_BONUS: str = _(
        ZhTwEnum.RESONATOR_ECHO_RESONANCE_SKILL_DMG_BONUS
    )
    ECHO_BASIC_ATTACK_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_BASIC_ATTACK_DMG_BONUS)
    ECHO_HEAVY_ATTACK_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_HEAVY_ATTACK_DMG_BONUS)
    ECHO_RESONANCE_LIBERATION_DMG_BONUS: str = _(
        ZhTwEnum.RESONATOR_ECHO_RESONANCE_LIBERATION_DMG_BONUS
    )
    ECHO_GLACIO_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_GLACIO_DMG_BONUS)
    ECHO_FUSION_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_FUSION_DMG_BONUS)
    ECHO_ELECTRO_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_ELECTRO_DMG_BONUS)
    ECHO_AERO_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_AERO_DMG_BONUS)
    ECHO_SPECTRO_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_SPECTRO_DMG_BONUS)
    ECHO_HAVOC_DMG_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_HAVOC_DMG_BONUS)
    ECHO_HEALING_BONUS: str = _(ZhTwEnum.RESONATOR_ECHO_HEALING_BONUS)


class ToCalculateResonatorModel(BaseModel):
    normal_attack_lv: str = ""
    resonance_skill_lv: str = ""
    resonance_liberation_lv: str = ""
    forte_circuit_lv: str = ""
    intro_skill_lv: str = ""
    outro_skill_lv: str = ""

    level: str = ""

    def get_level(cls) -> Decimal:
        level = cls.level
        level = level.replace("+", "")
        return get_number(level)

    calculated_hp_p: str = ""
    resonator_hp: str = ""
    echo_hp: str = ""

    def get_calculated_hp_p(cls) -> Decimal:
        return get_number(cls.calculated_hp_p)

    def get_resonator_hp(cls) -> Decimal:
        return get_number(cls.resonator_hp)

    def get_echo_hp(cls) -> Decimal:
        return get_number(cls.echo_hp)

    calculated_atk_p: str = ""
    resonator_atk: str = ""
    weapon_atk: str = ""
    echo_atk: str = ""

    def get_calculated_atk_p(cls) -> Decimal:
        return get_number(cls.calculated_atk_p)

    def get_resonator_atk(cls) -> Decimal:
        return get_number(cls.resonator_atk)

    def get_weapon_atk(cls) -> Decimal:
        return get_number(cls.weapon_atk)

    def get_echo_atk(cls) -> Decimal:
        return get_number(cls.echo_atk)

    calculated_def_p: str = ""
    resonator_def: str = ""
    echo_def: str = ""

    def get_calculated_def_p(cls) -> Decimal:
        return get_number(cls.calculated_def_p)

    def get_resonator_def(cls) -> Decimal:
        return get_number(cls.resonator_def)

    def get_echo_def(cls) -> Decimal:
        return get_number(cls.echo_def)

    calculated_crit_rate: str = ""
    calculated_crit_dmg: str = ""

    def get_calculated_crit_rate(cls) -> Decimal:
        return get_number(cls.calculated_crit_rate)

    def get_calculated_crit_dmg(cls) -> Decimal:
        return get_number(cls.calculated_crit_dmg)

    calculated_physical_bonus: str = ""
    calculated_glacio_bonus: str = ""
    calculated_fusion_bonus: str = ""
    calculated_electro_bonus: str = ""
    calculated_aero_bonus: str = ""
    calculated_spectro_bonus: str = ""
    calculated_havoc_bonus: str = ""

    def get_calculated_element_bonus(cls, element: Union[str, ElementEnum]) -> Decimal:
        value = ""
        if element == ElementEnum.PHYSICAL.value:
            value = cls.calculated_physical_bonus
        elif element == ElementEnum.GLACIO.value:
            value = cls.calculated_glacio_bonus
        elif element == ElementEnum.FUSION.value:
            value = cls.calculated_fusion_bonus
        elif element == ElementEnum.ELECTRO.value:
            value = cls.calculated_electro_bonus
        elif element == ElementEnum.AERO.value:
            value = cls.calculated_aero_bonus
        elif element == ElementEnum.SPECTRO.value:
            value = cls.calculated_spectro_bonus
        elif element == ElementEnum.HAVOC.value:
            value = cls.calculated_havoc_bonus
        return get_number(value)

    calculated_basic_bonus: str = ""
    calculated_heavy_bonus: str = ""
    calculated_resonance_skill_bonus: str = ""
    calculated_resonance_liberation_bonus: str = ""

    def get_calculated_skill_bonus(
        cls, bonus_type: Union[str, ResonatorSkillBonusTypeEnum]
    ) -> Decimal:
        value = ""
        if bonus_type == ResonatorSkillBonusTypeEnum.BASIC.value:
            value = cls.calculated_basic_bonus
        elif bonus_type == ResonatorSkillBonusTypeEnum.HEAVY.value:
            value = cls.calculated_heavy_bonus
        elif bonus_type == ResonatorSkillBonusTypeEnum.RESONANCE_SKILL.value:
            value = cls.calculated_resonance_skill_bonus
        elif bonus_type == ResonatorSkillBonusTypeEnum.RESONANCE_LIBERATION.value:
            value = cls.calculated_resonance_liberation_bonus

        return get_number(value)


class CalculatedResonatorModel(BaseModel):
    id: str = ""
    name: str = ""

    # resonator stat
    hp: str = ""
    attack: str = ""
    defense: str = ""

    # resonator base stat
    base_crit_rate: str = ""
    base_crit_dmg: str = ""
    base_energy_regen: str = ""

    # calculated
    calculated_hp: str = ""
    calculated_hp_p: str = ""
    calculated_atk: str = ""
    calculated_atk_p: str = ""
    calculated_def: str = ""
    calculated_def_p: str = ""
    calculated_crit_rate: str = ""
    calculated_crit_dmg: str = ""
    calculated_energy_regen: str = ""

    calculated_resonance_skill_dmg_bonus: str = ""
    calculated_basic_attack_dmg_bonus: str = ""
    calculated_heavy_attack_dmg_bonus: str = ""
    calculated_resonance_liberation_dmg_bonus: str = ""

    calculated_physical_dmg_bonus: str = ""
    calculated_glacio_dmg_bonus: str = ""
    calculated_fusion_dmg_bonus: str = ""
    calculated_electro_dmg_bonus: str = ""
    calculated_aero_dmg_bonus: str = ""
    calculated_spectro_dmg_bonus: str = ""
    calculated_havoc_dmg_bonus: str = ""

    calculated_physical_dmg_res: str = ""
    calculated_glacio_dmg_res: str = ""
    calculated_fusion_dmg_res: str = ""
    calculated_electro_dmg_res: str = ""
    calculated_aero_dmg_res: str = ""
    calculated_spectro_dmg_res: str = ""
    calculated_havoc_dmg_res: str = ""

    calculated_healing_bonus: str = ""

    # weapon
    weapon_atk: str = ""
    weapon_hp_p: str = ""
    weapon_atk_p: str = ""
    weapon_def_p: str = ""
    weapon_crit_rate: str = ""
    weapon_crit_dmg: str = ""
    weapon_energy_regen: str = ""

    weapon_rank_atk_p: str = ""
    weapon_rank_hp_p: str = ""
    weapon_rank_energy_regen: str = ""
    weapon_rank_attribute_dmg_bonus: str = ""

    # echo
    echo_1: str = ""
    echo_2: str = ""
    echo_3: str = ""
    echo_4: str = ""
    echo_5: str = ""
    echo_sonata_1: str = ""
    echo_sonata_2: str = ""
    echo_sonata_3: str = ""
    echo_sonata_4: str = ""
    echo_sonata_5: str = ""

    echo_hp: str = ""
    echo_hp_p: str = ""
    echo_atk: str = ""
    echo_atk_p: str = ""
    echo_def: str = ""
    echo_def_p: str = ""
    echo_crit_rate: str = ""
    echo_crit_dmg: str = ""
    echo_energy_regen: str = ""

    echo_resonance_skill_dmg_bonus: str = ""
    echo_basic_attack_dmg_bonus: str = ""
    echo_heavy_attack_dmg_bonus: str = ""
    echo_resonance_liberation_dmg_bonus: str = ""
    echo_glacio_dmg_bonus: str = ""
    echo_fusion_dmg_bonus: str = ""
    echo_electro_dmg_bonus: str = ""
    echo_aero_dmg_bonus: str = ""
    echo_spectro_dmg_bonus: str = ""
    echo_havoc_dmg_bonus: str = ""
    echo_healing_bonus: str = ""


# deprecated
class BaseResonatorModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    element: str = ""


class SimulatedResonatorModel(BaseModel):
    name: str = ""
    level: str = ""

    weapon_name: str = ""
    weapon_level: str = ""
    weapon_tune: str = ""

    normal_attack_lv: str = ""
    resonance_skill_lv: str = ""
    resonance_liberation_lv: str = ""
    forte_circuit_lv: str = ""
    intro_skill_lv: str = ""

    stat_bonus_hp_p: str = ""
    stat_bonus_atk_p: str = ""
    stat_bonus_def_p: str = ""
    stat_bonus_crit_rate: str = ""
    stat_bonus_crit_dmg: str = ""

    stat_bonus_glacio_dmg_bonus: str = ""
    stat_bonus_fusion_dmg_bonus: str = ""
    stat_bonus_electro_dmg_bonus: str = ""
    stat_bonus_aero_dmg_bonus: str = ""
    stat_bonus_spectro_dmg_bonus: str = ""
    stat_bonus_havoc_dmg_bonus: str = ""
    stat_bonus_healing_bonus: str = ""


class ResonatorStatBonusModel(BaseModel):
    hp_p: str = ""
    atk_p: str = ""
    def_p: str = ""
    crit_rate: str = ""
    crit_dmg: str = ""

    glacio: str = ""
    fusion: str = ""
    electro: str = ""
    aero: str = ""
    spectro: str = ""
    havoc: str = ""
    healing: str = ""

    resonance_skill: str = ""
    basic_attack: str = ""
    heavy_attack: str = ""
    resonance_liberation: str = ""


class ResonatorInformationModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    no: str = ""
    name: str = ""
    element: ElementEnum = ""
    rank: Optional[int] = None
    is_permanent: Optional[bool] = None

    stat_bonus: ResonatorStatBonusModel = ResonatorStatBonusModel()
