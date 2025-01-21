from enum import Enum


class SimulationTypeEnum(str, Enum):
    AFFIXES_15_1: str = "affixes_15_1"
    AFFIXES_20_SMALL: str = "affixes_20_small"
    AFFIXES_20_SKILL_BONUS: str = "affixes_20_skill_bonus"
