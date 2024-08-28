from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel

from ww.model.resonator import ResonatorName
from ww.utils.number import get_number


def get_damage_string_with_percentage(
    numerator: Optional[Decimal], denominator: Optional[Decimal]
) -> str:
    numerator = get_number(numerator)
    denominator = get_number(denominator)
    if not numerator or not denominator:
        return "0.00 (0.00%)"
    percentage = numerator / denominator

    percentage_str = f"{percentage:.2%}"
    damage_distribution_str = f"{numerator:,.2f}"

    return f"{damage_distribution_str} ({percentage_str})"


class TemplateResonatorDamageDistributionModel(BaseModel):
    resonator_name: str = ""
    resonator_id: str = ""

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
        return get_damage_string_with_percentage(damage, cls.damage)


class TemplateDamageDistributionModel(BaseModel):
    template_id: str = ""
    monster_id: str = ""

    duration_1: str = ""
    duration_2: str = ""

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    resonators: Dict[ResonatorName, TemplateResonatorDamageDistributionModel] = {}

    def get_damage_string_with_percentage(cls, resonator_name: str) -> str:
        resonator = cls.resonators.get(resonator_name, None)
        if resonator is None:
            return "0.00 (0.00%)"

        return get_damage_string_with_percentage(resonator.damage, cls.damage)

    def get_duration_1(cls) -> Decimal:
        return get_number(cls.duration_1)

    def get_duration_2(cls) -> Decimal:
        return get_number(cls.duration_2)
