from decimal import Decimal
from typing import Dict

from pydantic import BaseModel

from ww.model.resonator import ResonatorName


class TemplateResonatorDamageDistributionModel(BaseModel):
    resonator_name: str = ""
    resonater_id: str = ""

    basic: Decimal = Decimal("0.0")
    heavy: Decimal = Decimal("0.0")
    skill: Decimal = Decimal("0.0")
    liberation: Decimal = Decimal("0.0")
    intro: Decimal = Decimal("0.0")
    outro: Decimal = Decimal("0.0")
    echo: Decimal = Decimal("0.0")
    none: Decimal = Decimal("0.0")

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    def get_damage_string_with_percentage(cls, bonus_type: str) -> str:
        damage = getattr(cls, bonus_type)
        percentage = damage / cls.damage

        percentage_str = f"{percentage:.2%}"
        damage_distribution_str = f"{damage:.2f}"

        return f"{damage_distribution_str} ({percentage_str})"


class TemplateDamageDistributionModel(BaseModel):
    template_id: str = ""
    monster_id: str = ""

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    resonators: Dict[ResonatorName, TemplateResonatorDamageDistributionModel] = {}
