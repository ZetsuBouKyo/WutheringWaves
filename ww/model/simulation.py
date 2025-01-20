from enum import Enum


class SimulationTypeEnum(str, Enum):
    AFFIXES_15_1: str = "theory_1"
    AFFIXES_20_SMALL: str = "half_built_small"
    HALF_BUILT_SKILL_BONUS: str = "half_built_skill_bonus"
