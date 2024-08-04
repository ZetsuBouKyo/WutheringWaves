from typing import List

from pydantic import BaseModel

from ww.model.template.buff_table import (
    TemplateBuffTableRowEnum,
    TemplateBuffTableRowModel,
)
from ww.model.template.resonator_table import TemplateResonatorTableRowEnum
from ww.model.template.template_row import (
    TEMPLATE_BONUS,
    TemplateRowActionEnum,
    TemplateRowBuffTypeEnum,
    TemplateRowEnum,
)
from ww.model.template.tsv import CalculatedTemplateEnum, TemplateEnum

__all__ = [
    "TEMPLATE_BONUS",
    "TemplateBuffTableRowEnum",
    "TemplateBuffTableRowModel",
    "TemplateResonatorTableRowEnum",
    "TemplateRowActionEnum",
    "TemplateRowBuffTypeEnum",
    "TemplateRowEnum",
    "CalculatedTemplateEnum",
    "TemplateEnum",
]


class TemplateResonatorModel(BaseModel):
    resonator_name: str = ""
    resonator_chain: str = ""
    resonator_weapon_name: str = ""
    resonator_weapon_rank: str = ""
    resonator_inherent_skill_1: bool = None
    resonator_inherent_skill_2: bool = None
    resonator_echo_1: str = ""
    resonator_echo_sonata_1: str = ""
    resonator_echo_sonata_2: str = ""
    resonator_echo_sonata_3: str = ""
    resonator_echo_sonata_4: str = ""
    resonator_echo_sonata_5: str = ""


class TemplateRowBuffModel(BaseModel): ...


class TemplateRowModel(BaseModel):
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


class TemplateModel(BaseModel):
    id: str = ""

    test_resonator_id_1: str = ""
    test_resonator_id_2: str = ""
    test_resonator_id_3: str = ""

    monster_id: str = ""
    description: str = ""

    resonators: List[TemplateResonatorModel] = []
    rows: List[TemplateRowModel] = []
