from collections import OrderedDict
from decimal import Decimal
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from ww.model.buff import SkillBonusTypeEnum
from ww.model.resonator import ResonatorName
from ww.model.resonator_skill import ResonatorSkillTypeEnum
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


class TemplateResonatorSkillDamageDistributionModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str = ""
    name: str = ""
    type: Optional[ResonatorSkillTypeEnum] = None
    damage: Decimal = Decimal("0.0")


class TemplateResonatorDamageDistributionModel(BaseModel):
    resonator_id: str = ""
    resonator_name: str = ""

    basic: Decimal = Decimal("0.0")
    heavy: Decimal = Decimal("0.0")
    skill: Decimal = Decimal("0.0")
    liberation: Decimal = Decimal("0.0")
    intro: Decimal = Decimal("0.0")
    outro: Decimal = Decimal("0.0")
    echo: Decimal = Decimal("0.0")
    coordinated_attack: Decimal = Decimal("0.0")
    none: Decimal = Decimal("0.0")

    aero_erosion: Decimal = Decimal("0.0")
    spectro_frazzle: Decimal = Decimal("0.0")

    normal_attack: Decimal = Decimal("0.0")
    resonance_skill: Decimal = Decimal("0.0")
    resonance_liberation: Decimal = Decimal("0.0")
    intro_skill: Decimal = Decimal("0.0")
    forte_circuit: Decimal = Decimal("0.0")
    outro_skill: Decimal = Decimal("0.0")

    damage: Decimal = Decimal("0.0")
    damage_no_crit: Decimal = Decimal("0.0")
    damage_crit: Decimal = Decimal("0.0")

    skills: Dict[str, TemplateResonatorSkillDamageDistributionModel] = {}

    def get_damage_string_with_percentage(cls, name: str) -> str:
        damage = getattr(cls, name)
        return get_damage_string_with_percentage(damage, cls.damage)

    def get_damage(cls, name: str) -> Decimal:
        damage = getattr(cls, name)
        return damage

    def get_skill_damages(cls) -> List[TemplateResonatorSkillDamageDistributionModel]:
        skills_dict: Dict[str, TemplateResonatorSkillDamageDistributionModel] = {}
        for skill in cls.skills.values():
            skill_id = skill.id
            skill_name = skill_id
            if "-" in skill_id:
                skill_id_split: str = skill_id.split("-")
                if skill_id_split[-1].isdigit():
                    skill_name_split = skill_id_split[:-1]
                    skill_name = "".join(skill_name_split)

            if skills_dict.get(skill_name, None) is None:
                skills_dict[skill_name] = TemplateResonatorSkillDamageDistributionModel(
                    name=skill_name, type=skill.type, damage=skill.damage
                )
            else:
                skills_dict[skill_name].damage += skill.damage

        skills: List[TemplateResonatorSkillDamageDistributionModel] = list(
            skills_dict.values()
        )
        skills.sort(
            key=lambda skill: skill.damage,
            reverse=True,
        )
        return skills

    def get_resonator_skill_base_damage(
        cls, skill_enum: Union[SkillBonusTypeEnum, ResonatorSkillTypeEnum]
    ) -> Decimal:
        base_damage = Decimal("0.0")
        for e in skill_enum:
            base_damage += cls.get_damage(e.name.lower())
        return base_damage


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

    def get_max_dps(cls) -> Decimal:
        if not cls.damage or not cls.duration_1 or not cls.duration_2:
            return Decimal("0.0")
        durations = [cls.get_duration_1(), cls.get_duration_2()]
        duration = min(durations)
        if duration >= Decimal(0.0):
            return cls.damage / duration
        return Decimal("0.0")

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

    def get_resonator_max_dps(cls, resonator_name: str) -> Decimal:
        resonator = cls.resonators.get(resonator_name, None)
        if resonator is None or not cls.damage:
            return Decimal("0.0")
        max_dps = cls.get_max_dps()
        dps = max_dps * resonator.damage / cls.damage
        return dps

    def get_team_resonator_damages(cls) -> List[Decimal]:
        damages = []
        for _, resonator in cls.resonators.items():
            damages.append(resonator.damage)
        return damages
