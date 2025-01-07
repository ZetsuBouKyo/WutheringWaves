from collections import OrderedDict
from copy import deepcopy
from typing import Dict, List, Optional

from ww.crud.template import get_template
from ww.model import Number, SkillBaseAttrEnum
from ww.model.buff import SkillBonusTypeEnum
from ww.model.echo import EchoSkillTsvColumnEnum
from ww.model.element import ElementEnum
from ww.model.monsters import MonsterTsvColumnEnum
from ww.model.resonator import (
    CALCULATED_RESONATORS_DMG_BONUS_PREFIX,
    CALCULATED_RESONATORS_DMG_BONUS_SUFFIX,
    CalculatedResonatorTsvColumnEnum,
    ResonatorTsvColumnEnum,
    ToCalculateResonatorModel,
)
from ww.model.resonator_skill import (
    ResonatorSkillBonusTypeEnum,
    ResonatorSkillTsvColumnEnum,
    ResonatorSkillTypeEnum,
)
from ww.model.template import (
    CalculatedTemplateRowModel,
    TemplateDamageDistributionModel,
    TemplateResonatorDamageDistributionModel,
    TemplateRowBuffModel,
    TemplateRowBuffTypeEnum,
    TemplateRowModel,
)
from ww.tables.echo import EchoSkillTable
from ww.tables.monster import MonstersTable
from ww.tables.resonator import (
    CalculatedResonatorsTable,
    ResonatorSkillTable,
    ResonatorsTable,
)
from ww.utils.number import get_number, get_string


def get_buffs(row: TemplateRowModel) -> TemplateRowBuffModel:
    buffs = TemplateRowBuffModel()
    for buff in row.buffs:
        if buff.type == TemplateRowBuffTypeEnum.MAGNIFIER.value:
            buffs.bonus_magnifier += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.AMPLIFIER.value:
            buffs.bonus_amplifier += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.HP_P.value:
            buffs.bonus_hp_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.HP.value:
            buffs.bonus_hp += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ATK_P.value:
            buffs.bonus_atk_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ATK.value:
            buffs.bonus_atk += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.DEF_P.value:
            buffs.bonus_def_p += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.DEF.value:
            buffs.bonus_def += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.CRIT_RATE.value:
            buffs.bonus_crit_rate += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.CRIT_DMG.value:
            buffs.bonus_crit_dmg += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.ADDITION.value:
            buffs.bonus_addition += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.SKILL_DMG_ADDITION.value:
            buffs.bonus_skill_dmg_addition += get_number(buff.value) * get_number(
                buff.stack
            )
        elif buff.type == TemplateRowBuffTypeEnum.IGNORE_DEF.value:
            buffs.bonus_ignore_def += get_number(buff.value) * get_number(buff.stack)
        elif buff.type == TemplateRowBuffTypeEnum.REDUCE_RES.value:
            buffs.bonus_reduce_res += get_number(buff.value) * get_number(buff.stack)
    return buffs


class Damage:

    def __init__(
        self,
        monster_id: Optional[str] = None,
        monster_level: Optional[Number] = None,
        monster_def: Optional[Number] = None,
        monster_res: Optional[Number] = None,
        resonators_table: Optional[Number] = None,
        calculated_resonators_table: Optional[Number] = None,
    ):
        if monster_id is not None:
            if (
                monster_level is not None
                or monster_def is not None
                or monster_res is not None
            ):
                raise ValueError
        self._monster_id = monster_id
        self._monster_level = get_number(monster_level)
        self._monster_def = get_number(monster_def)
        self._monster_res = get_number(monster_res)

        if resonators_table is None:
            self._resonators_table = ResonatorsTable()
        else:
            self._resonators_table = resonators_table
        if calculated_resonators_table is None:
            self._calculated_resonators_table = CalculatedResonatorsTable()
        else:
            self._calculated_resonators_table = calculated_resonators_table
        self.init()

    def init(self):
        self._echo_skill_table = EchoSkillTable()
        self._monsters_table = MonstersTable()

        if self._monster_id is not None:
            self._monster_level = get_number(
                self._monsters_table.search(
                    self._monster_id, MonsterTsvColumnEnum.LEVEL
                )
            )
            self._monster_def = get_number(
                self._monsters_table.search(self._monster_id, MonsterTsvColumnEnum.DEF)
            )

    def set_resonators_table(self, table: ResonatorsTable):
        self._resonators_table = table

    def set_calculated_resonators_table(self, table: CalculatedResonatorsTable):
        self._calculated_resonators_table = table

    def set_monster_id(self, id: str):
        self._monster_id = id
        self._monster_level = get_number(
            self._monsters_table.search(self._monster_id, MonsterTsvColumnEnum.LEVEL)
        )
        self._monster_def = get_number(
            self._monsters_table.search(self._monster_id, MonsterTsvColumnEnum.DEF)
        )

    def set_monster_res(self, res: Number):
        self._monster_res = get_number(res)

    def set_monster_level(self, level: Number):
        self._monster_level = get_number(level)

    def set_monster_def(self, defense: Number):
        self._monster_def = get_number(defense)

    def get_resonator_name_to_id(self, resonator_ids: str = []) -> Dict[str, str]:
        table = OrderedDict()

        for resonator_id in resonator_ids:
            if not resonator_id:
                continue
            resonator_name = self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.NAME.value
            )
            if resonator_name is None:
                continue
            if table.get(resonator_name, None) is not None:
                return OrderedDict()
            table[resonator_name] = resonator_id
        return table

    def get_calculated_row(
        self, resonator_id: Optional[str], row: TemplateRowModel
    ) -> Optional[CalculatedTemplateRowModel]:
        if resonator_id is None:
            return

        resonator_level_str: str = self._resonators_table.search(
            resonator_id, ResonatorTsvColumnEnum.LEVEL
        )

        resonator = ToCalculateResonatorModel()
        resonator.level = resonator_level_str

        # Resonator Skill Level
        resonator.normal_attack_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.NORMAL_ATTACK_LV.value
            )
        )
        resonator.resonance_skill_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.RESONANCE_SKILL_LV.value
            )
        )
        resonator.resonance_liberation_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.RESONANCE_LIBERATION_LV.value
            )
        )
        resonator.forte_circuit_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.FORTE_CIRCUIT_LV.value
            )
        )
        resonator.intro_skill_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.INTRO_SKILL_LV.value
            )
        )
        resonator.outro_skill_lv = str(
            self._resonators_table.search(
                resonator_id, ResonatorTsvColumnEnum.INTRO_SKILL_LV.value
            )
        )

        # HP Percentage
        resonator.calculated_hp_p = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.CALCULATED_HP_P
        )

        # HP
        resonator.resonator_hp = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.HP
        )

        # Additional HP
        resonator.echo_hp = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.ECHO_HP
        )

        # ATK Percentage
        resonator.calculated_atk_p = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.CALCULATED_ATK_P
        )

        # ATK
        resonator.resonator_atk = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.ATTACK
        )
        resonator.weapon_atk = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.WEAPON_ATK
        )

        # Additional ATK
        resonator.echo_atk = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.ECHO_ATK
        )

        # DEF Percentage
        resonator.calculated_def_p = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.CALCULATED_DEF_P
        )

        # DEF
        resonator.resonator_def = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.DEFENSE
        )

        # Additional DEF
        resonator.echo_def = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.ECHO_DEF
        )

        # CRIT Rate
        resonator.calculated_crit_rate = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_RATE
        )

        # CRIT DMG
        resonator.calculated_crit_dmg = self._calculated_resonators_table.search(
            resonator_id, CalculatedResonatorTsvColumnEnum.CALCULATED_CRIT_DMG
        )

        # BONUS
        resonator.calculated_physical_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.PHYSICAL.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_glacio_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.GLACIO.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_fusion_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.FUSION.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_electro_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.ELECTRO.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_aero_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.AERO.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_spectro_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.SPECTRO.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_havoc_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ElementEnum.HAVOC.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )

        resonator.calculated_basic_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ResonatorSkillBonusTypeEnum.BASIC.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_heavy_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ResonatorSkillBonusTypeEnum.HEAVY.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_resonance_skill_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ResonatorSkillBonusTypeEnum.RESONANCE_SKILL.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )
        resonator.calculated_resonance_liberation_bonus = self._calculated_resonators_table.search(
            resonator_id,
            f"{CALCULATED_RESONATORS_DMG_BONUS_PREFIX}{ResonatorSkillBonusTypeEnum.RESONANCE_LIBERATION.value}{CALCULATED_RESONATORS_DMG_BONUS_SUFFIX}",
        )

        return self.get_calculated_row_with_resonator(resonator, row)

    def get_calculated_row_with_resonator(
        self, resonator: ToCalculateResonatorModel, row: TemplateRowModel
    ) -> Optional[CalculatedTemplateRowModel]:

        resonator_name = row.resonator_name

        calculated_row = CalculatedTemplateRowModel()
        calculated_row.labels = row.labels
        calculated_row.resonator_name = resonator_name
        calculated_row.hits = row.hit
        calculated_row.real_dmg_crit = row.real_dmg_crit
        calculated_row.real_dmg_no_crit = row.real_dmg_no_crit

        manual_bonus_type = get_string(row.skill_bonus_type)

        resonator_level = resonator.get_level()

        # Action
        calculated_row.action = row.action

        # Time
        calculated_row.time_start = row.time_start
        calculated_row.time_end = row.time_end

        # Buffs
        buffs = get_buffs(row)
        calculated_row.buffs = row.buffs

        # Skill
        template_row_skill_id = row.skill_id

        # Resonator Skill Level
        resonator_skill_levels = {
            ResonatorTsvColumnEnum.NORMAL_ATTACK_LV.value: resonator.normal_attack_lv,
            ResonatorTsvColumnEnum.RESONANCE_SKILL_LV.value: resonator.resonance_skill_lv,
            ResonatorTsvColumnEnum.RESONANCE_LIBERATION_LV.value: resonator.resonance_liberation_lv,
            ResonatorTsvColumnEnum.FORTE_CIRCUIT_LV.value: resonator.forte_circuit_lv,
            ResonatorTsvColumnEnum.INTRO_SKILL_LV.value: resonator.intro_skill_lv,
            ResonatorTsvColumnEnum.OUTRO_SKILL_LV.value: resonator.outro_skill_lv,
        }

        # Resonator Skill
        resonator_skill_table = ResonatorSkillTable(resonator_name)

        resonator_skill_element = resonator_skill_table.search(
            template_row_skill_id, ResonatorSkillTsvColumnEnum.ELEMENT
        )
        resonator_skill_base_attr = resonator_skill_table.search(
            template_row_skill_id, ResonatorSkillTsvColumnEnum.BASE_ATTR
        )
        resonator_skill_type = resonator_skill_table.search(
            template_row_skill_id, ResonatorSkillTsvColumnEnum.TYPE_ZH_TW
        )
        resonator_skill_bonus_type = resonator_skill_table.search(
            template_row_skill_id, ResonatorSkillTsvColumnEnum.SKILL_BONUS_TYPE
        )
        resonator_skill_is_coordinated = resonator_skill_table.search(
            template_row_skill_id, ResonatorSkillTsvColumnEnum.COORDINATED
        )
        resonator_skill_lv = resonator_skill_levels.get(
            f"{resonator_skill_type}LV", None
        )
        resonator_skill_dmg = resonator_skill_table.search(
            template_row_skill_id, f"LV{resonator_skill_lv}"
        )
        if resonator_skill_dmg is not None:
            resonator_skill_dmg = get_number(resonator_skill_dmg)

        calculated_row.skill_id = template_row_skill_id
        calculated_row.resonator_skill_level = resonator_skill_lv
        calculated_row.resonator_skill_element = resonator_skill_element
        calculated_row.resonator_skill_base_attr = resonator_skill_base_attr
        calculated_row.resonator_skill_type = resonator_skill_type
        calculated_row.resonator_skill_type_bonus = resonator_skill_bonus_type
        calculated_row.resonator_skill_dmg = resonator_skill_dmg

        # Echo Skill
        echo_skill_element = self._echo_skill_table.search(
            template_row_skill_id, EchoSkillTsvColumnEnum.ELEMENT
        )
        echo_skill_base_attr = self._echo_skill_table.search(
            template_row_skill_id, EchoSkillTsvColumnEnum.BASE_ATTRIBUTE
        )
        echo_skill_dmg = self._echo_skill_table.search(
            template_row_skill_id, EchoSkillTsvColumnEnum.DMG
        )
        if echo_skill_dmg is not None:
            echo_skill_dmg = get_number(echo_skill_dmg)

        calculated_row.echo_element = echo_skill_element
        calculated_row.echo_skill_dmg = echo_skill_dmg

        # Base attribute
        if resonator_skill_base_attr is None:
            base_attr = echo_skill_base_attr
        else:
            base_attr = resonator_skill_base_attr
        calculated_row.result_skill_base_attribute = base_attr

        # Element
        if not ((resonator_skill_element is None) ^ (echo_skill_element is None)):
            # TODO: raise error
            # print("element")
            return

        if resonator_skill_element is None:
            element = echo_skill_element
        else:
            element = resonator_skill_element

        calculated_row.result_element = element

        # Skill DMG
        if not ((resonator_skill_dmg is None) ^ (echo_skill_dmg is None)):
            # TODO: raise error
            # print("skill dmg")
            return

        if resonator_skill_dmg is None:
            skill_dmg = echo_skill_dmg
        else:
            skill_dmg = resonator_skill_dmg
        calculated_row.result_skill_dmg = skill_dmg

        # Bonus Type
        if not (
            (resonator_skill_bonus_type is None)
            ^ (echo_skill_element is None or echo_skill_dmg is None)
        ):
            # TODO: raise error
            # print("bonus type")
            return

        if manual_bonus_type:
            bonus_type = manual_bonus_type
        elif echo_skill_element and echo_skill_dmg and echo_skill_base_attr:
            bonus_type = SkillBonusTypeEnum.ECHO.value
        elif resonator_skill_bonus_type:
            bonus_type = resonator_skill_bonus_type
        else:
            bonus_type = SkillBonusTypeEnum.NONE.value
        calculated_row.result_bonus_type = bonus_type

        calculated_row.result_bonus_types = [bonus_type]
        if resonator_skill_is_coordinated:
            calculated_row.result_bonus_types.append(
                SkillBonusTypeEnum.COORDINATED_ATTACK.value
            )

        # Monster
        if self._monster_id is not None:
            monster_res = get_number(
                self._monsters_table.search(self._monster_id, f"{element}抗性")
            )
        else:
            monster_res = self._monster_res
        monster_def = self._monster_def
        calculated_row.monster_level = self._monster_level
        calculated_row.monster_def = monster_def
        calculated_row.monster_res = monster_res

        # HP Percentage
        calculated_hp_p = resonator.get_calculated_hp_p()
        bonus_hp_p = buffs.bonus_hp_p
        result_hp_p = calculated_hp_p + bonus_hp_p
        calculated_row.result_hp_p = result_hp_p

        # HP
        resonator_hp = resonator.get_resonator_hp()
        result_hp = resonator_hp
        calculated_row.result_hp = result_hp

        # Additional HP
        echo_hp = resonator.get_echo_hp()
        bonus_hp = buffs.bonus_hp
        result_hp_addition = echo_hp + bonus_hp
        calculated_row.result_hp_addition = result_hp_addition

        # ATK Percentage
        calculated_atk_p = resonator.get_calculated_atk_p()
        bonus_atk_p = buffs.bonus_atk_p
        result_atk_p = calculated_atk_p + bonus_atk_p
        calculated_row.result_atk_p = result_atk_p

        # ATK
        resonator_atk = resonator.get_resonator_atk()
        weapon_atk = resonator.get_weapon_atk()
        result_atk = resonator_atk + weapon_atk
        calculated_row.result_atk = result_atk

        # Additional ATK
        echo_atk = resonator.get_echo_atk()
        bonus_atk = buffs.bonus_atk
        result_atk_addition = echo_atk + bonus_atk
        calculated_row.result_atk_addition = result_atk_addition

        # DEF Percentage
        calculated_def_p = resonator.get_calculated_def_p()
        bonus_def_p = buffs.bonus_def_p
        result_def_p = calculated_def_p + bonus_def_p
        calculated_row.result_def_p = result_def_p

        # DEF
        resonator_def = resonator.get_resonator_def()
        result_def = resonator_def
        calculated_row.result_def = result_def

        # Additional DEF
        echo_def = resonator.get_echo_def()
        bonus_def = buffs.bonus_def
        result_def_addition = echo_def + bonus_def
        calculated_row.result_def_addition = result_def_addition

        # CRIT Rate
        calculated_crit_rate = resonator.get_calculated_crit_rate()
        bonus_crit_rate = buffs.bonus_crit_rate
        result_crit_rate = calculated_crit_rate + bonus_crit_rate
        if result_crit_rate >= get_number("1.0"):
            result_crit_rate = get_number("1.0")
        calculated_row.result_crit_rate = result_crit_rate

        # CRIT DMG
        calculated_crit_dmg = resonator.get_calculated_crit_dmg()
        bonus_crit_dmg = buffs.bonus_crit_dmg
        result_crit_dmg = calculated_crit_dmg + bonus_crit_dmg
        calculated_row.result_crit_dmg = result_crit_dmg

        # BONUS
        calculated_element_bonus = resonator.get_calculated_element_bonus(element)
        calculated_skill_bonus = resonator.get_calculated_skill_bonus(bonus_type)

        template_bonus = buffs.bonus_addition
        result_bonus = (
            calculated_element_bonus + calculated_skill_bonus + template_bonus
        )

        # Other Bonus
        bonus_magnifier = buffs.bonus_magnifier
        bonus_amplifier = buffs.bonus_amplifier
        bonus_skill_dmg_addition = buffs.bonus_skill_dmg_addition
        bonus_ignore_def = buffs.bonus_ignore_def
        bonus_reduce_res = buffs.bonus_reduce_res

        # DMG
        if base_attr == SkillBaseAttrEnum.ATK.value:
            region_base_attr = (
                result_atk * (get_number("1.0") + result_atk_p) + result_atk_addition
            )
        elif base_attr == SkillBaseAttrEnum.DEF.value:
            region_base_attr = (
                result_def * (get_number("1.0") + result_def_p) + result_def_addition
            )
        elif base_attr == SkillBaseAttrEnum.HP.value:
            region_base_attr = (
                result_hp * (get_number("1.0") + result_hp_p) + result_hp_addition
            )
        else:
            return

        region_skill_dmg = skill_dmg + bonus_skill_dmg_addition
        calculated_row.resonator_skill_dmg = skill_dmg
        calculated_row.resonator_skill_dmg_addition = bonus_skill_dmg_addition

        region_bonus_magnifier = get_number("1.0") + bonus_magnifier
        calculated_row.result_magnifier = bonus_magnifier

        region_bonus_amplifier = get_number("1.0") + bonus_amplifier
        calculated_row.result_amplifier = bonus_amplifier

        region_bonus = get_number("1.0") + result_bonus
        calculated_row.result_bonus = result_bonus

        region_def = (get_number("800.0") + get_number("8.0") * resonator_level) / (
            get_number("800.0")
            + get_number("8.0") * resonator_level
            + monster_def * (1 - bonus_ignore_def)
        )
        calculated_row.resonator_level = resonator_level
        calculated_row.result_ignore_def = bonus_ignore_def

        region_bonus_reduce_res = get_number("1.0") + bonus_reduce_res - monster_res
        calculated_row.result_reduce_res = bonus_reduce_res

        region_crit_dmg = result_crit_dmg
        region_crit = (
            result_crit_dmg * result_crit_rate + get_number("1.0") - result_crit_rate
        )

        # Hit
        hit = get_number(row.hit)
        calculated_row.result_skill_hit = hit

        dmg_no_crit = (
            hit
            * region_base_attr
            * region_skill_dmg
            * region_bonus_magnifier
            * region_bonus_amplifier
            * region_bonus
            * region_def
            * region_bonus_reduce_res
        )

        dmg_crit = dmg_no_crit * region_crit_dmg
        dmg_avg = dmg_no_crit * region_crit

        calculated_row.damage = dmg_avg
        calculated_row.damage_no_crit = dmg_no_crit
        calculated_row.damage_crit = dmg_crit

        return calculated_row

    def get_default_row(self, row: TemplateRowModel) -> CalculatedTemplateRowModel:
        resonator_name = row.resonator_name

        calculated_row = CalculatedTemplateRowModel()
        calculated_row.labels = row.labels
        calculated_row.resonator_name = resonator_name
        calculated_row.hits = row.hit
        calculated_row.real_dmg_crit = row.real_dmg_crit
        calculated_row.real_dmg_no_crit = row.real_dmg_no_crit

        # Action
        calculated_row.action = row.action

        # Time
        calculated_row.time_start = row.time_start
        calculated_row.time_end = row.time_end

        # Buffs
        calculated_row.buffs = row.buffs

        return calculated_row

    def get_calculated_rows(
        self,
        template_id: str,
        r_id_1: str,
        r_id_2: str,
        r_id_3: str,
        monster_id: Optional[str] = None,
        is_default: bool = False,
    ) -> List[CalculatedTemplateRowModel]:
        self.init()
        if monster_id is not None:
            self.set_monster_id(monster_id)

        calculated_rows = []

        template = get_template(template_id)
        if template is None:
            return calculated_rows

        r_ids = [r_id_1, r_id_2, r_id_3]
        resonators_name2id = self.get_resonator_name_to_id(r_ids)

        for row in template.rows:
            resonator_name = row.resonator_name
            resonator_id = resonators_name2id.get(resonator_name, None)
            if resonator_id is None:
                continue
            calculated_row = self.get_calculated_row(resonator_id, row)
            if calculated_row is not None:
                calculated_rows.append(calculated_row)
            elif is_default:
                calculated_row = self.get_default_row(row)
                calculated_rows.append(calculated_row)

        return calculated_rows

    def extract_damage_distributions_from_rows_with_labels(
        self,
        resonator_name_to_id: Dict[str, str],
        template_id: str,
        monster_id: str,
        rows: List[CalculatedTemplateRowModel] = [],
        labels: Optional[List[str]] = None,
    ) -> Dict[str, TemplateDamageDistributionModel]:
        damage_distributions: Dict[str, TemplateDamageDistributionModel] = {}
        if not resonator_name_to_id:
            return damage_distributions

        template = get_template(template_id)
        if template is None:
            return damage_distributions

        for row in rows:
            _labels = deepcopy(row.labels)
            if "" not in _labels:
                _labels.append("")

            for label in _labels:
                if labels is not None and label not in labels:
                    continue

                if damage_distributions.get(label, None) is None:
                    damage_distributions[label] = TemplateDamageDistributionModel()

                    label_model = template.get_label(label)
                    if label_model is not None:
                        d1 = get_number(label_model.duration_1)
                        d2 = get_number(label_model.duration_2)
                        if d1 >= get_number("0.0") and d2 >= get_number("0.0"):
                            damage_distributions[label].duration_1 = (
                                label_model.duration_1
                            )
                            damage_distributions[label].duration_2 = (
                                label_model.duration_2
                            )
                    else:
                        damage_distributions[label].duration_1 = template.duration_1
                        damage_distributions[label].duration_2 = template.duration_2

                    if (
                        label == ""
                        and not damage_distributions[label].duration_1
                        and not damage_distributions[label].duration_2
                    ):
                        damage_distributions[label].duration_1 = template.duration_1
                        damage_distributions[label].duration_2 = template.duration_2

                    for resonator_name in resonator_name_to_id.keys():
                        resonator_id = resonator_name_to_id.get(resonator_name, None)
                        if resonator_id is None:
                            continue
                        damage_distributions[label].template_id = template_id
                        damage_distributions[label].monster_id = monster_id
                        damage_distributions[label].resonators[resonator_name] = (
                            TemplateResonatorDamageDistributionModel(
                                resonator_name=resonator_name,
                                resonator_id=resonator_id,
                            )
                        )

                resonator_name = row.resonator_name

                damage = get_number(row.damage)
                damage_no_crit = get_number(row.damage_no_crit)
                damage_crit = get_number(row.damage_crit)

                skill_bonus_type = row.result_bonus_type
                if skill_bonus_type == SkillBonusTypeEnum.BASIC.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].basic += damage
                elif skill_bonus_type == SkillBonusTypeEnum.HEAVY.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].heavy += damage
                elif skill_bonus_type == SkillBonusTypeEnum.SKILL.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].skill += damage
                elif skill_bonus_type == SkillBonusTypeEnum.LIBERATION.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].liberation += damage
                elif skill_bonus_type == SkillBonusTypeEnum.INTRO.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].intro += damage
                elif skill_bonus_type == SkillBonusTypeEnum.OUTRO.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].outro += damage
                elif skill_bonus_type == SkillBonusTypeEnum.ECHO.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].echo += damage
                else:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].none += damage

                skill_bonus_types = row.result_bonus_types
                if SkillBonusTypeEnum.COORDINATED_ATTACK.value in skill_bonus_types:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].coordinated_attack += damage

                resonator_skill_type = row.resonator_skill_type
                if resonator_skill_type == ResonatorSkillTypeEnum.NORMAL_ATTACK.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].normal_attack += damage
                elif (
                    resonator_skill_type == ResonatorSkillTypeEnum.RESONANCE_SKILL.value
                ):
                    damage_distributions[label].resonators[
                        resonator_name
                    ].resonance_skill += damage
                elif (
                    resonator_skill_type
                    == ResonatorSkillTypeEnum.RESONANCE_LIBERATION.value
                ):
                    damage_distributions[label].resonators[
                        resonator_name
                    ].resonance_liberation += damage
                elif resonator_skill_type == ResonatorSkillTypeEnum.INTRO_SKILL.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].intro_skill += damage
                elif resonator_skill_type == ResonatorSkillTypeEnum.OUTRO_SKILL.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].outro_skill += damage
                elif resonator_skill_type == ResonatorSkillTypeEnum.FORTE_CIRCUIT.value:
                    damage_distributions[label].resonators[
                        resonator_name
                    ].forte_circuit += damage

                damage_distributions[label].resonators[resonator_name].damage += damage
                damage_distributions[label].resonators[
                    resonator_name
                ].damage_no_crit += damage_no_crit
                damage_distributions[label].resonators[
                    resonator_name
                ].damage_crit += damage_crit

                damage_distributions[label].damage += damage
                damage_distributions[label].damage_no_crit += damage_no_crit
                damage_distributions[label].damage_crit += damage_crit
        return damage_distributions

    def extract_damage_distribution_from_rows(
        self,
        resonator_name_to_id: Dict[str, str],
        template_id: str,
        monster_id: str,
        rows: List[CalculatedTemplateRowModel] = [],
    ) -> TemplateDamageDistributionModel:
        damage_distributions = self.extract_damage_distributions_from_rows_with_labels(
            resonator_name_to_id, template_id, monster_id, rows
        )

        damage_distribution = damage_distributions.get(
            "", TemplateDamageDistributionModel()
        )

        return damage_distribution

    def get_damage_distributions_with_labels(
        self,
        template_id: str,
        r_id_1: str,
        r_id_2: str,
        r_id_3: str,
        monster_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, TemplateDamageDistributionModel]:
        rows = self.get_calculated_rows(template_id, r_id_1, r_id_2, r_id_3, monster_id)

        r_ids = [r_id_1, r_id_2, r_id_3]
        resonators_name2id = self.get_resonator_name_to_id(r_ids)

        return self.extract_damage_distributions_from_rows_with_labels(
            resonators_name2id, template_id, monster_id, rows, labels=labels
        )

    def get_damage_distribution(
        self,
        template_id: str,
        r_id_1: str,
        r_id_2: str,
        r_id_3: str,
        monster_id: Optional[str] = None,
        duration_1: str = "",
        duration_2: str = "",
    ) -> TemplateDamageDistributionModel:
        rows = self.get_calculated_rows(template_id, r_id_1, r_id_2, r_id_3, monster_id)

        r_ids = [r_id_1, r_id_2, r_id_3]
        resonators_name2id = self.get_resonator_name_to_id(r_ids)

        return self.extract_damage_distribution_from_rows(
            resonators_name2id,
            template_id,
            monster_id,
            rows,
            duration_1=duration_1,
            duration_2=duration_2,
        )
