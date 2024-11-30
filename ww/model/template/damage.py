from collections import OrderedDict
from decimal import Decimal
from typing import Dict, Optional

from pydantic import BaseModel

from ww.model.resonator import ResonatorName
from ww.utils.number import get_number, to_number_string, to_percentage_str


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

    normal_attack: Decimal = Decimal("0.0")
    resonance_skill: Decimal = Decimal("0.0")
    resonance_liberation: Decimal = Decimal("0.0")
    intro_skill: Decimal = Decimal("0.0")
    forte_circuit: Decimal = Decimal("0.0")
    outro_skill: Decimal = Decimal("0.0")

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    def get_damage_string_with_percentage(cls, name: str) -> str:
        damage = getattr(cls, name)
        return get_damage_string_with_percentage(damage, cls.damage)

    def get_damage(cls, name: str) -> Decimal:
        damage = getattr(cls, name)
        return damage


class TemplateDamageDistributionModel(BaseModel):
    template_id: str = ""
    monster_id: str = ""

    duration_1: str = ""
    duration_2: str = ""

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    resonators: Dict[ResonatorName, TemplateResonatorDamageDistributionModel] = (
        OrderedDict()
    )

    def get_damage_string_with_percentage(cls, resonator_name: str) -> str:
        resonator = cls.resonators.get(resonator_name, None)
        if resonator is None:
            return "0.00 (0.00%)"

        return get_damage_string_with_percentage(resonator.damage, cls.damage)

    def get_duration_1(cls) -> Decimal:
        return get_number(cls.duration_1)

    def get_duration_2(cls) -> Decimal:
        return get_number(cls.duration_2)

    def get_min_dps(cls) -> Optional[Decimal]:
        if not cls.damage or not cls.duration_1 or not cls.duration_2:
            return None
        durations = [cls.get_duration_1(), cls.get_duration_2()]
        duration = max(durations)
        if duration >= Decimal(0.0):
            return cls.damage / duration

    def get_min_dps_string(cls) -> Optional[str]:
        m = cls.get_min_dps()
        if m is None:
            return None
        return to_number_string(m)

    def get_max_dps(cls) -> Optional[Decimal]:
        if not cls.damage or not cls.duration_1 or not cls.duration_2:
            return None
        durations = [cls.get_duration_1(), cls.get_duration_2()]
        duration = min(durations)
        if duration >= Decimal(0.0):
            return cls.damage / duration

    def get_max_dps_string(cls) -> Optional[str]:
        m = cls.get_max_dps()
        if m is None:
            return None
        return to_number_string(m)

    def get_resonator_max_dps_percentage_string(cls, resonator_name: str) -> str:
        resonator = cls.resonators.get(resonator_name, None)
        if resonator is None or not cls.damage:
            return ""
        return to_percentage_str(resonator.damage / cls.damage)

    def get_resonator_max_dps(cls, resonator_name: str) -> Optional[Decimal]:
        resonator = cls.resonators.get(resonator_name, None)
        if resonator is None or not cls.damage:
            return None
        max_dps = cls.get_max_dps()
        dps = max_dps * resonator.damage / cls.damage
        return dps
