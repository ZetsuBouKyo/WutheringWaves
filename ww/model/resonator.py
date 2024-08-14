from enum import Enum

from pydantic import BaseModel, ConfigDict

from ww.locale import ZhTwEnum, _


class ResonatorStatColumnEnum(str, Enum):
    LEVEL: str = _(ZhTwEnum.LEVEL)
    HP: str = _(ZhTwEnum.HP)
    ATK: str = _(ZhTwEnum.ATK)
    DEF: str = _(ZhTwEnum.DEF)


class ResonatorColumnEnum(str, Enum):
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


CALCULATED_RESONATORS_DMG_BONUS_PREFIX: str = "角色"
CALCULATED_RESONATORS_DMG_BONUS_SUFFIX: str = "傷害加成面板"


class CalculatedResonatorColumnEnum(str, Enum):
    ID: str = "角色代稱"

    # Resonator Stat
    HP: str = "角色生命"
    ATK: str = "角色攻擊"
    DEF: str = "角色防禦"

    # Resonator Base Stat
    BASE_CRIT_RATE: str = "角色基礎暴擊"
    BASE_CRIT_DMG: str = "角色基礎暴擊傷害"
    BASE_ENERGY_REGEN: str = "角色基礎共鳴效率"

    # Calculated
    CALCULATED_HP: str = "角色生命面板"
    CALCULATED_HP_P: str = "角色生命百分比面板"
    CALCULATED_ATK: str = "角色攻擊面板"
    CALCULATED_ATK_P: str = "角色攻擊百分比面板"
    CALCULATED_DEF: str = "角色防禦面板"
    CALCULATED_DEF_P: str = "角色防禦百分比面板"
    CALCULATED_CRIT_RATE: str = "角色暴擊面板"
    CALCULATED_CRIT_DMG: str = "角色暴傷面板"
    CALCULATED_ENERGY_REGEN: str = "角色共鳴效率面板"

    CALCULATED_RESONANCE_SKILL_DMG_BONUS: str = "角色共鳴技能傷害加成面板"
    CALCULATED_BASIC_ATTACK_DMG_BONUS: str = "角色普攻傷害加成面板"
    CALCULATED_HEAVY_ATTACK_DMG_BONUS: str = "角色重擊傷害加成面板"
    CALCULATED_RESONANCE_LIBERATION_DMG_BONUS: str = "角色共鳴解放傷害加成面板"

    CALCULATED_PHYSICAL_DMG_BONUS: str = "角色物理傷害加成面板"
    CALCULATED_GLACIO_DMG_BONUS: str = "角色冷凝傷害加成面板"
    CALCULATED_FUSION_DMG_BONUS: str = "角色熱熔傷害加成面板"
    CALCULATED_ELECTRO_DMG_BONUS: str = "角色導電傷害加成面板"
    CALCULATED_AERO_DMG_BONUS: str = "角色氣動傷害加成面板"
    CALCULATED_SPECTRO_DMG_BONUS: str = "角色衍射傷害加成面板"
    CALCULATED_HAVOC_DMG_BONUS: str = "角色湮滅傷害加成面板"

    CALCULATED_PHYSICAL_DMG_RES: str = "角色物理傷害抗性面板"
    CALCULATED_GLACIO_DMG_RES: str = "角色冷凝傷害抗性面板"
    CALCULATED_FUSION_DMG_RES: str = "角色熱熔傷害抗性面板"
    CALCULATED_ELECTRO_DMG_RES: str = "角色導電傷害抗性面板"
    CALCULATED_AERO_DMG_RES: str = "角色氣動傷害抗性面板"
    CALCULATED_SPECTRO_DMG_RES: str = "角色衍射傷害抗性面板"
    CALCULATED_HAVOC_DMG_RES: str = "角色湮滅傷害抗性面板"

    CALCULATED_HEALING_BONUS: str = "角色治療效果加成面板"

    # Weapon
    WEAPON_ATK: str = "[主]武器攻擊"
    WEAPON_HP_P: str = "[副]武器生命百分比"
    WEAPON_ATK_P: str = "[副]武器攻擊百分比"
    WEAPON_DEF_P: str = "[副]武器防禦百分比"
    WEAPON_CRIT_RATE: str = "[副]武器暴擊"
    WEAPON_CRIT_DMG: str = "[副]武器暴擊傷害"
    WEAPON_ENERGY_REGEN: str = "[副]武器共鳴效率"

    WEAPON_RANK_ATK_P: str = "武器諧振攻擊提升"
    WEAPON_RANK_ENERGY_REGEN: str = "武器諧振共鳴效率提升"
    WEAPON_RANK_ATTRIBUTE_DMG_BONUS: str = "武器諧振全屬性傷害加成提升"

    # Echo
    ECHO_HP: str = "聲骸生命"
    ECHO_HP_P: str = "聲骸生命百分比"
    ECHO_ATK: str = "聲骸攻擊"
    ECHO_ATK_P: str = "聲骸攻擊百分比"
    ECHO_DEF: str = "聲骸防禦"
    ECHO_DEF_P: str = "聲骸防禦百分比"
    ECHO_CRIT_RATE: str = "聲骸暴擊"
    ECHO_CRIT_DMG: str = "聲骸暴擊傷害"
    ECHO_ENERGY_REGEN: str = "聲骸共鳴效率"

    ECHO_RESONANCE_SKILL_DMG_BONUS: str = "聲骸共鳴技能傷害加成"
    ECHO_BASIC_ATTACK_DMG_BONUS: str = "聲骸普攻傷害加成"
    ECHO_HEAVY_ATTACK_DMG_BONUS: str = "聲骸重擊傷害加成"
    ECHO_RESONANCE_LIBERATION_DMG_BONUS: str = "聲骸共鳴解放傷害加成"
    ECHO_GLACIO_DMG_BONUS: str = "聲骸冷凝加成"
    ECHO_FUSION_DMG_BONUS: str = "聲骸熱熔加成"
    ECHO_ELECTRO_DMG_BONUS: str = "聲骸導電加成"
    ECHO_AERO_DMG_BONUS: str = "聲骸氣動加成"
    ECHO_SPECTRO_DMG_BONUS: str = "聲骸衍射加成"
    ECHO_HAVOC_DMG_BONUS: str = "聲骸湮滅加成"
    ECHO_HEALING_BONUS: str = "聲骸治療效果加成百分比"


class CalculatedResonatorModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str = ""

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
    weapon_rank_energy_regen: str = ""
    weapon_rank_attribute_dmg_bonus: str = ""

    # echo
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
