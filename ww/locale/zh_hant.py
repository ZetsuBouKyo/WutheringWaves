from enum import Enum


class ZhHantEnum(str, Enum):
    RESONATOR: str = "共鳴者"
    RESONATOR_1: str = "共鳴者1"
    RESONATOR_2: str = "共鳴者2"
    RESONATOR_3: str = "共鳴者3"
    WEAPON: str = "武器"
    BUFF: str = "增益"
    NAME: str = "名稱"

    GLACIO: str = "冷凝"
    FUSION: str = "熱熔"
    ELECTRO: str = "導電"
    AERO: str = "氣動"
    SPECTRO: str = "衍射"
    HAVOC: str = "湮滅"

    LOAD: str = "讀檔"
    LOADING: str = "讀檔中..."
    LOADED: str = "讀檔完成。"
    SAVE: str = "存檔"
    SAVING: str = "存檔中..."
    SAVED: str = "存檔完成。"
    FILE_EXISTS: str = "檔案已存在"
    FILE_OVERWRITE_OR_NOT: str = "確定要覆蓋檔案"

    CALCULATE: str = "計算"
    DELETE: str = "刪除"

    WARNING: str = "警告"

    LOAD_SELECTED_TEMPLATE_ID: str = "讀取選取的模板ID"
    DELETE_SELECTED_TEMPLATE_ID: str = "刪除選取的模板ID"
    TO_SELECT_TEMPLATE_ID: str = "請選擇要讀取的模板ID。"
    TO_SELECT_TEMPLATE_ID_TO_DELETE: str = "請選擇要刪除的模板ID。"

    CONFIRM_DELETE_TEMPLATE: str = "確定要刪除模板"

    TEMPLATE_ID_MUST_NOT_EMPTY: str = "模板ID不該是空值。"

    PROGRESS_BAR: str = "進度條"

    TAB_BASIC: str = "基本資料"
    TAB_OUTPUT_METHOD: str = "輸出手法"
    TAB_DAMAGE_DISTRIBUTION: str = "傷害占比"
    TAB_HELP: str = "說明"
    TAB_ANALYSIS: str = "分析"

    TAB_ATTR: str = "屬性"
    TAB_SKILL: str = "技能"

    LEVEL: str = "等級"
    ENERGY_REGEN: str = "共鳴效率"

    MAGNIFIER: str = "倍率"
    AMPLIFIER: str = "加深"
    HP_P: str = "生命百分比"
    HP: str = "生命"
    ATK_P: str = "攻擊百分比"
    ATK: str = "攻擊"
    DEF_P: str = "防禦百分比"
    DEF: str = "防禦"
    CRIT_RATE: str = "暴擊"
    CRIT_DMG: str = "暴擊傷害"
    ADDITION: str = "加成"
    SKILL_DMG_ADDITION: str = "招式倍率"
    IGNORE_DEF: str = "忽視防禦"
    REDUCE_RES: str = "抗性降低"

    WEAPON_ATK_P_INCREASE: str = "攻擊提升"
    WEAPON_ATTRIBUTE_DMG_BONUS_INCREASE: str = "全屬性傷害加成提升"
    WEAPON_ENERGY_REGEN_INCREASE: str = "共鳴效率提升"

    NORMAL_ATTACK: str = "常態攻擊"
    RESONANCE_SKILL: str = "共鳴技能"
    RESONANCE_LIBERATION: str = "共鳴解放"
    INTRO_SKILL: str = "變奏技能"
    OUTRO_SKILL: str = "延奏技能"
    FORTE_CIRCUIT: str = "共鳴回路"

    DAMAGE_DISTRIBUTION_BASIC: str = "[傷害占比]普攻"
    DAMAGE_DISTRIBUTION_HEAVY: str = "[傷害占比]重擊"
    DAMAGE_DISTRIBUTION_SKILL: str = "[傷害占比]共鳴技能"
    DAMAGE_DISTRIBUTION_LIBERATION: str = "[傷害占比]共鳴解放"
    DAMAGE_DISTRIBUTION_INTRO: str = "[傷害占比]變奏"
    DAMAGE_DISTRIBUTION_OUTRO: str = "[傷害占比]延奏"
    DAMAGE_DISTRIBUTION_ECHO: str = "[傷害占比]聲骸"
    DAMAGE_DISTRIBUTION_NONE: str = "[傷害占比]無"

    BASIC: str = "普攻"
    HEAVY: str = "重擊"
    SKILL: str = "共鳴技能"
    LIBERATION: str = "共鳴解放"
    INTRO: str = "變奏"
    OUTRO: str = "延奏"
    ECHO: str = "聲骸"
    NONE: str = "無"

    DAMAGE: str = "[計算]傷害"
    DAMAGE_NO_CRIT: str = "[計算]無暴擊傷害"
    DAMAGE_CRIT: str = "[計算]暴擊傷害"

    FINAL_ELEMENT: str = "[總]屬性"
    FINAL_BONUS_TYPE: str = "[總]加成種類"
    FINAL_SKILL_DMG: str = "[總]技能倍率"

    FINAL_ATK: str = "[總]攻擊"
    FINAL_ATK_ADDITION: str = "[總]額外攻擊"
    FINAL_ATK_P: str = "[總]攻擊百分比"
    FINAL_CRIT_RATE: str = "[總]暴擊"
    FINAL_CRIT_DMG: str = "[總]暴擊傷害"
    FINAL_BONUS: str = "[總]加成區百分比"

    SHOW_4_STAR: str = "顯示四星"
    TOTAL_PULLS: str = "全部喚取數量"
    TOTAL_5_STAR_PULLS: str = "全部五星喚取數量"
    REMAINED_4_STAR_ABOVE_PULLS: str = "四星以上墊抽"
    REMAINED_5_STAR_PULLS: str = "五星墊抽"
    FROM_OLD_TO_NEW: str = "從舊到新"
    AVERAGE_PITY_5_STAR: str = "平均五星保底"
    AVERAGE_PITY_4_STAR: str = "平均四星保底"

    POOL_NAME_MUST_NOT_EMPTY: str = "喚取池子名稱不該是空值。"
    POOL_NAME_NOT_LEGAL: str = "喚取池子名稱錯誤。"

    WUTHERING_WAVES_DEBUG_FILE_NOT_FOUND: str = "請選擇 'debug.log' 檔案。"
    WUTHERING_WAVES_DEBUG_FILE_SHOULD_BE_COPIED: str = (
        "建議將 'debug.log' 複製到其他資料夾再進行分析。"
    )
