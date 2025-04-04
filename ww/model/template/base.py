from decimal import Decimal
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from ww.model.template.buff_table import (
    TemplateBuffTableColumnEnum,
    TemplateBuffTableRowModel,
)
from ww.tables.resonator import get_resonator_element
from ww.utils import get_md5


class TemplateResonatorModel(BaseModel):
    resonator_name: str = ""
    resonator_chain: str = ""
    resonator_weapon_name: str = ""
    resonator_weapon_rank: str = ""
    resonator_inherent_skill_1: Optional[bool] = None
    resonator_inherent_skill_2: Optional[bool] = None
    resonator_base_attr: str = ""
    resonator_skill_bonus: str = ""  # ResonatorSkillBonusTypeEnum
    resonator_energy_regen: str = ""
    resonator_echo_1: str = ""
    resonator_echo_sonata_1: str = ""
    resonator_echo_sonata_2: str = ""
    resonator_echo_sonata_3: str = ""
    resonator_echo_sonata_4: str = ""
    resonator_echo_sonata_5: str = ""
    resonator_echo_cost_1: str = ""
    resonator_echo_cost_2: str = ""
    resonator_echo_cost_3: str = ""
    resonator_echo_cost_4: str = ""
    resonator_echo_cost_5: str = ""
    resonator_echo_affix_1: str = ""
    resonator_echo_affix_2: str = ""
    resonator_echo_affix_3: str = ""
    resonator_echo_affix_4: str = ""
    resonator_echo_affix_5: str = ""

    def check(cls) -> bool:
        if not cls.resonator_name:
            return True
        return (
            cls.resonator_weapon_name
            and cls.resonator_weapon_rank
            and cls.resonator_base_attr
            and cls.resonator_skill_bonus
            and cls.resonator_echo_1
            and cls.resonator_echo_sonata_1
            and cls.resonator_echo_sonata_2
            and cls.resonator_echo_sonata_3
            and cls.resonator_echo_sonata_4
            and cls.resonator_echo_sonata_5
        )

    def are_custom_echoes(cls) -> bool:
        return (
            cls.resonator_echo_cost_1
            and cls.resonator_echo_cost_2
            and cls.resonator_echo_cost_3
            and cls.resonator_echo_cost_4
            and cls.resonator_echo_cost_5
            and cls.resonator_echo_affix_1
            and cls.resonator_echo_affix_2
            and cls.resonator_echo_affix_3
            and cls.resonator_echo_affix_4
            and cls.resonator_echo_affix_5
        )

    def get_row(cls):
        resonator_inherent_skill_1 = cls.resonator_inherent_skill_1
        if resonator_inherent_skill_1 is None:
            resonator_inherent_skill_1 = ""
        else:
            resonator_inherent_skill_1 = str(int(resonator_inherent_skill_1))

        resonator_inherent_skill_2 = cls.resonator_inherent_skill_2
        if resonator_inherent_skill_2 is None:
            resonator_inherent_skill_2 = ""
        else:
            resonator_inherent_skill_2 = str(int(resonator_inherent_skill_2))

        return [
            cls.resonator_name,
            cls.resonator_chain,
            cls.resonator_weapon_name,
            cls.resonator_weapon_rank,
            resonator_inherent_skill_1,
            resonator_inherent_skill_2,
            cls.resonator_base_attr,
            cls.resonator_skill_bonus,
            cls.resonator_energy_regen,
            cls.resonator_echo_1,
            cls.resonator_echo_sonata_1,
            cls.resonator_echo_sonata_2,
            cls.resonator_echo_sonata_3,
            cls.resonator_echo_sonata_4,
            cls.resonator_echo_sonata_5,
            cls.resonator_echo_cost_1,
            cls.resonator_echo_cost_2,
            cls.resonator_echo_cost_3,
            cls.resonator_echo_cost_4,
            cls.resonator_echo_cost_5,
            cls.resonator_echo_affix_1,
            cls.resonator_echo_affix_2,
            cls.resonator_echo_affix_3,
            cls.resonator_echo_affix_4,
            cls.resonator_echo_affix_5,
        ]

    def get_sonatas(cls) -> List[str]:
        return [
            cls.resonator_echo_sonata_1,
            cls.resonator_echo_sonata_2,
            cls.resonator_echo_sonata_3,
            cls.resonator_echo_sonata_4,
            cls.resonator_echo_sonata_5,
        ]


class TemplateRowBuffModel(BaseModel):
    bonus_magnifier: Decimal = Decimal("0.0")
    bonus_amplifier: Decimal = Decimal("0.0")
    bonus_hp_p: Decimal = Decimal("0.0")
    bonus_hp: Decimal = Decimal("0.0")
    bonus_atk_p: Decimal = Decimal("0.0")
    bonus_atk: Decimal = Decimal("0.0")
    bonus_def_p: Decimal = Decimal("0.0")
    bonus_def: Decimal = Decimal("0.0")
    bonus_crit_rate: Decimal = Decimal("0.0")
    bonus_crit_dmg: Decimal = Decimal("0.0")
    bonus_addition: Decimal = Decimal("0.0")
    bonus_skill_dmg_addition: Decimal = Decimal("0.0")
    bonus_ignore_def: Decimal = Decimal("0.0")
    bonus_reduce_res: Decimal = Decimal("0.0")


class TemplateRowModel(BaseModel):
    labels: List[str] = []
    resonator_name: str = ""
    real_dmg_no_crit: str = ""
    real_dmg_crit: str = ""
    action: str = ""
    skill_id: str = ""
    skill_bonus_type: str = ""
    hit: str = "1"
    buffs: List[TemplateBuffTableRowModel] = []
    resonating_spin_concerto_regen: str = ""
    accumulated_resonating_spin_concerto_regen: str = ""
    time_start: str = ""
    time_end: str = ""
    cumulative_time: str = ""
    frame: str = ""
    comment: str = ""

    def get_labels_str(cls) -> str:
        return ", ".join(cls.labels)

    def get_buff_names(cls) -> List[str]:
        return [buff.name for buff in cls.buffs if buff.name]

    def get_buffs_str(cls) -> str:
        buff_data = {e.value: [] for e in TemplateBuffTableColumnEnum}

        for buff in cls.buffs:
            # Tool tips
            buff_data[TemplateBuffTableColumnEnum.NAME.value].append(buff.name)
            buff_data[TemplateBuffTableColumnEnum.TYPE.value].append(buff.type)
            buff_data[TemplateBuffTableColumnEnum.VALUE.value].append(buff.value)
            buff_data[TemplateBuffTableColumnEnum.STACK.value].append(buff.stack)
            buff_data[TemplateBuffTableColumnEnum.DURATION.value].append(buff.duration)

        df = pd.DataFrame(buff_data)
        return df.to_html()

    def get_element(cls):
        return get_resonator_element(cls.resonator_name)


class TemplateLabelModel(BaseModel):
    name: str = ""
    duration_1: str = ""
    duration_2: str = ""

    def get_row(cls):
        return [cls.name, cls.duration_1, cls.duration_2]


class TemplateModel(BaseModel):
    id: str = ""

    labels: List[TemplateLabelModel] = []

    test_resonator_id_1: str = ""
    test_resonator_id_2: str = ""
    test_resonator_id_3: str = ""

    duration_1: str = ""
    duration_2: str = ""

    monster_id: str = ""
    description: str = ""

    resonators: List[TemplateResonatorModel] = []
    rows: List[TemplateRowModel] = []

    def get_title(cls) -> str:
        resonator_names = [name for name in cls.get_resonator_names() if name]
        return ", ".join(resonator_names)

    def get_md5(cls) -> str:
        return get_md5(cls.id)

    def get_buff_names(cls) -> List[str]:
        buffs_set = set()
        for row in cls.rows:
            buffs_set |= set(row.get_buff_names())
        buffs = list(buffs_set)
        buffs.sort()
        return buffs

    def get_label(cls, label_name: str) -> Optional[TemplateLabelModel]:
        for label in cls.labels:
            if label.name == label_name:
                return label
        return None

    def get_label_names(cls) -> List[str]:
        return [label.name for label in cls.labels]

    def get_resonator(cls, resonator_name: str) -> Optional[TemplateResonatorModel]:
        for resonator in cls.resonators:
            if resonator.resonator_name == resonator_name:
                return resonator
        return None

    def get_resonator_names(cls) -> List[str]:
        return [
            resonator.resonator_name
            for resonator in cls.resonators
            if resonator.resonator_name
        ]

    def get_sonatas(cls, resonator_name: str) -> List[str]:
        for resonator in cls.resonators:
            if resonator.resonator_name == resonator_name:
                return resonator.get_sonatas()
        return []

    def get_base_attr(cls, resonator_name: str) -> str:
        for resonator in cls.resonators:
            if resonator.resonator_name == resonator_name:
                return resonator.resonator_base_attr
        return ""

    def get_skill_bonus(cls, resonator_name: str) -> str:
        for resonator in cls.resonators:
            if resonator.resonator_name == resonator_name:
                return resonator.resonator_skill_bonus
        return ""

    def get_echo_1(cls, resonator_name: str) -> str:
        for resonator in cls.resonators:
            if resonator.resonator_name == resonator_name:
                return resonator.resonator_echo_1
        return ""
