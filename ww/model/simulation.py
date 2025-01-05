from enum import Enum


class SimulationTypeEnum(str, Enum):
    THEORY_1: str = "theory_1"
    HALF_BUILT_ATK: str = "half_built_atk"
    HALF_BUILT_SKILL_BONUS: str = "half_built_skill_bonus"
