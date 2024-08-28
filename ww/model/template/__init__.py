from decimal import Decimal
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from ww.model.template.buff_table import (
    TemplateBuffTableColumnEnum,
    TemplateBuffTableRowModel,
)
from ww.model.template.calculated_row import (
    CalculatedTemplateColumnEnum,
    CalculatedTemplateRowModel,
)
from ww.model.template.damage import (
    TemplateDamageDistributionModel,
    TemplateResonatorDamageDistributionModel,
)
from ww.model.template.html import (
    TemplateHtmlOutputMethodActionModel,
    TemplateHtmlOutputMethodModel,
    TemplateHtmlResonatorModel,
)
from ww.model.template.label import TemplateLabelTableColumnEnum
from ww.model.template.resonator_table import TemplateResonatorTableColumnEnum
from ww.model.template.template_row import (
    TEMPLATE_BONUS,
    TemplateColumnEnum,
    TemplateRowActionEnum,
    TemplateRowBuffTypeEnum,
)
from ww.model.template.tsv import TemplateEnum

__all__ = [
    "TEMPLATE_BONUS",
    "CalculatedTemplateColumnEnum",
    "CalculatedTemplateRowModel",
    "TemplateBuffTableColumnEnum",
    "TemplateBuffTableRowModel",
    "TemplateColumnEnum",
    "TemplateDamageDistributionModel",
    "TemplateEnum",
    "TemplateHtmlOutputMethodActionModel",
    "TemplateHtmlOutputMethodModel",
    "TemplateHtmlResonatorModel",
    "TemplateLabelTableColumnEnum",
    "TemplateResonatorDamageDistributionModel",
    "TemplateResonatorTableColumnEnum",
    "TemplateRowActionEnum",
    "TemplateRowBuffTypeEnum",
]


class TemplateResonatorModel(BaseModel):
    resonator_name: str = ""
    resonator_chain: str = ""
    resonator_weapon_name: str = ""
    resonator_weapon_rank: str = ""
    resonator_inherent_skill_1: Optional[bool] = None
    resonator_inherent_skill_2: Optional[bool] = None
    resonator_echo_1: str = ""
    resonator_echo_sonata_1: str = ""
    resonator_echo_sonata_2: str = ""
    resonator_echo_sonata_3: str = ""
    resonator_echo_sonata_4: str = ""
    resonator_echo_sonata_5: str = ""

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
            cls.resonator_echo_1,
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
    buffs: List[TemplateBuffTableRowModel] = []
    resonating_spin_concerto_regen: str = ""
    accumulated_resonating_spin_concerto_regen: str = ""
    time_start: str = ""
    time_end: str = ""
    cumulative_time: str = ""
    frame: str = ""
    comment: str = ""

    def get_labels_str(cls):
        return ", ".join(cls.labels)

    def get_buffs_str(cls):
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

    def get_label(cls, label_name: str) -> Optional[TemplateLabelModel]:
        for label in cls.labels:
            if label.name == label_name:
                return label
        return None

    def get_label_names(cls) -> List[str]:
        return [label.name for label in cls.labels]
