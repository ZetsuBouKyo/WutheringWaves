from enum import Enum


class ResonatorsEnum(str, Enum):
    ID = "角色代稱"
    PREFIX: str = "字首"
    SUFFIX: str = "字尾"
    NAME = "角色名稱"

    WEAPON_NAME = "武器名稱"
    WEAPON_LEVEL = "武器等級"
    WEAPON_RANK = "武器諧振"

    LEVEL = "角色等級"
    RESONANCE_CHAIN = "共鳴鏈"
    MAX_STA = "耐力上限"

    NORMAL_ATTACK_LV = "常態攻擊LV"
    RESONANCE_SKILL_LV = "共鳴技能LV"
    FORTE_CIRCUIT_LV = "共鳴回路LV"
    RESONANCE_LIBERATION_LV = "共鳴解放LV"
    INTRO_SKILL_LV = "變奏技能LV"
    OUTRO_SKILL_LV = "延奏技能LV"

    STAT_BONUS_HP_P = "生命百分比"
    STAT_BONUS_ATK_P = "攻擊百分比"
    STAT_BONUS_DEF_P = "防禦百分比"
    STAT_BONUS_CRIT_RATE = "暴擊"
    STAT_BONUS_CRIT_DMG = "暴擊傷害"

    STAT_BONUS_GLACIO_DMG_BONUS = "冷凝加成"
    STAT_BONUS_FUSION_DMG_BONUS = "熱熔加成"
    STAT_BONUS_ELECTRO_DMG_BONUS = "導電加成"
    STAT_BONUS_AERO_DMG_BONUS = "氣動加成"
    STAT_BONUS_SPECTRO_DMG_BONUS = "衍射加成"
    STAT_BONUS_HAVOC_DMG_BONUS = "湮滅加成"
    STAT_BONUS_HEALING_BONUS = "治療效果加成"

    INHERENT_SKILL_1 = "固有一階"
    INHERENT_SKILL_2 = "固有二階"

    STAT_BONUS_PHYSICAL_DMG_RES = "物理抗性"
    STAT_BONUS_GLACIO_DMG_RES = "冷凝抗性"
    STAT_BONUS_FUSION_DMG_RES = "熱熔抗性"
    STAT_BONUS_ELECTRO_DMG_RES = "導電抗性"
    STAT_BONUS_AERO_DMG_RES = "氣動抗性"
    STAT_BONUS_SPECTRO_DMG_RES = "衍射抗性"
    STAT_BONUS_HAVOC_DMG_RES = "湮滅抗性"

    ECHO_1 = "聲骸1"
    ECHO_2 = "聲骸2"
    ECHO_3 = "聲骸3"
    ECHO_4 = "聲骸4"
    ECHO_5 = "聲骸5"


class CalculatedResonatorsEnum(str, Enum):
    ID = "角色代稱"

    # Resonator Stat
    HP = "角色生命"
    ATK = "角色攻擊"
    DEF = "角色防禦"

    # Resonator Base Stat
    BASE_CRIT_RATE = "角色基礎暴擊"
    BASE_CRIT_DMG = "角色基礎暴擊傷害"
    BASE_ENERGY_REGEN = "角色基礎共鳴效率"

    # Calculated
    CALCULATED_HP = "角色生命面板"
    CALCULATED_HP_P = "角色生命百分比面板"
    CALCULATED_ATK = "角色攻擊面板"
    CALCULATED_ATK_P = "角色攻擊百分比面板"
    CALCULATED_DEF = "角色防禦面板"
    CALCULATED_DEF_P = "角色防禦百分比面板"
    CALCULATED_CRIT_RATE = "角色暴擊面板"
    CALCULATED_CRIT_DMG = "角色暴傷面板"
    CALCULATED_ENERGY_REGEN = "角色共鳴效率面板"

    CALCULATED_RESONANCE_SKILL_DMG_BONUS = "角色共鳴技能傷害加成面板"
    CALCULATED_BASIC_ATTACK_DMG_BONUS = "角色普攻傷害加成面板"
    CALCULATED_HEAVY_ATTACK_DMG_BONUS = "角色重擊傷害加成面板"
    CALCULATED_RESONANCE_LIBERATION_DMG_BONUS = "角色共鳴解放傷害加成面板"
    CALCULATED_PHYSICAL_DMG_BONUS = "角色物理傷害加成面板"
    CALCULATED_GLACIO_DMG_BONUS = "角色冷凝傷害加成面板"
    CALCULATED_FUSION_DMG_BONUS = "角色熱熔傷害加成面板"
    CALCULATED_ELECTRO_DMG_BONUS = "角色導電傷害加成面板"
    CALCULATED_AERO_DMG_BONUS = "角色氣動傷害加成面板"
    CALCULATED_SPECTRO_DMG_BONUS = "角色衍射傷害加成面板"
    CALCULATED_HAVOC_DMG_BONUS = "角色湮滅傷害加成面板"

    CALCULATED_PHYSICAL_DMG_RES = "角色物理傷害抗性面板"
    CALCULATED_GLACIO_DMG_RES = "角色冷凝傷害抗性面板"
    CALCULATED_FUSION_DMG_RES = "角色熱熔傷害抗性面板"
    CALCULATED_ELECTRO_DMG_RES = "角色導電傷害抗性面板"
    CALCULATED_AERO_DMG_RES = "角色氣動傷害抗性面板"
    CALCULATED_SPECTRO_DMG_RES = "角色衍射傷害抗性面板"
    CALCULATED_HAVOC_DMG_RES = "角色湮滅傷害抗性面板"

    CALCULATED_HEALING_BONUS = "角色治療效果加成面板"

    # Weapon
    WEAPON_ATK = "[主]武器攻擊"
    WEAPON_HP_P = "[副]武器生命百分比"
    WEAPON_ATK_P = "[副]武器攻擊百分比"
    WEAPON_DEF_P = "[副]武器防禦百分比"
    WEAPON_CRIT_RATE = "[副]武器暴擊"
    WEAPON_CRIT_DMG = "[副]武器暴擊傷害"
    WEAPON_ENERGY_REGEN = "[副]武器共鳴效率"

    WEAPON_RANK_ATK_P = "武器諧振攻擊提升"
    WEAPON_RANK_ENERGY_REGEN = "武器諧振共鳴效率提升"
    WEAPON_RANK_ATTRIBUTE_DMG_BONUS = "武器諧振全屬性傷害加成提升"

    # Echo
    ECHO_HP = "聲骸生命"
    ECHO_HP_P = "聲骸生命百分比"
    ECHO_ATK = "聲骸攻擊"
    ECHO_ATK_P = "聲骸攻擊百分比"
    ECHO_DEF = "聲骸防禦"
    ECHO_DEF_P = "聲骸防禦百分比"
    ECHO_CRIT_RATE = "聲骸暴擊"
    ECHO_CRIT_DMG = "聲骸暴擊傷害"
    ECHO_ENERGY_REGEN = "聲骸共鳴效率"

    ECHO_RESONANCE_SKILL_DMG_BONUS = "聲骸共鳴技能傷害加成"
    ECHO_BASIC_ATTACK_DMG_BONUS = "聲骸普攻傷害加成"
    ECHO_HEAVY_ATTACK_DMG_BONUS = "聲骸重擊傷害加成"
    ECHO_RESONANCE_LIBERATION_DMG_BONUS = "聲骸共鳴解放傷害加成"
    ECHO_GLACIO_DMG_BONUS = "聲骸冷凝加成"
    ECHO_FUSION_DMG_BONUS = "聲骸熱熔加成"
    ECHO_ELECTRO_DMG_BONUS = "聲骸導電加成"
    ECHO_AERO_DMG_BONUS = "聲骸氣動加成"
    ECHO_SPECTRO_DMG_BONUS = "聲骸衍射加成"
    ECHO_HAVOC_DMG_BONUS = "聲骸湮滅加成"
    ECHO_HEALING_BONUS = "聲骸治療效果加成百分比"
