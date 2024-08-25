from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict

from ww.model.pool.id_to_name import GachaResonatorModel, GachaWeaponModel


class GachaPoolTypeEnum(str, Enum):
    FEATURED_RESONATOR_CONVENE: str = "角色活動喚取"
    FEATURED_WEAPON_CONVENE: str = "武器活動喚取"
    STANDARD_RESONATOR_CONVENE: str = "角色常駐喚取"
    STANDARD_WEAPON_CONVENE: str = "武器常駐喚取"


class PoolModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    total: int = 0
    standard_resonator_5: int = 0
    featured_resonator_5: int = 0
    standard_weapon_5: int = 0
    featured_weapon_5: int = 0

    remainder_5: int = 0
    remainder_4_or_5: int = 0

    pool_type: Optional[GachaPoolTypeEnum] = None
    results: List[Union[str, GachaResonatorModel, GachaWeaponModel]] = []
