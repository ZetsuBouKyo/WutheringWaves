from copy import deepcopy
from typing import List

from ww.model.pool import GachaPoolTypeEnum, PoolModel
from ww.model.pool.id_to_name import resonators, weapons


def get_pool_by_ids(ids: List[str], pool: PoolModel = PoolModel()):
    pool.total = len(ids)
    count_4_or_5 = 0
    count_5 = 0
    for id in ids:
        count_4_or_5 += 1
        count_5 += 1
        resonator = deepcopy(resonators.get(id, None))
        weapon = deepcopy(weapons.get(id, None))

        if resonator is not None and type(resonator) != str:
            if resonator.star < 4:
                continue
            if resonator.star == 5:
                if resonator.permanent:
                    pool.standard_resonator_5 += 1
                else:
                    pool.featured_resonator_5 += 1
                resonator.number = count_5
                count_5 = 0
                count_4_or_5 = 0
            elif resonator.star == 4:
                resonator.number = count_4_or_5
                count_4_or_5 = 0
            pool.results.append(resonator)

        if weapon is not None and type(weapon) != str:
            if weapon.star < 4:
                continue
            elif weapon.star == 5:
                if weapon.permanent:
                    pool.standard_weapon_5 += 1
                else:
                    pool.featured_weapon_5 += 1
                weapon.number = count_5
                count_5 = 0
                count_4_or_5 = 0
            elif weapon.star == 4:
                weapon.number = count_4_or_5
                count_4_or_5 = 0
            pool.results.append(weapon)

    pool.remainder_5 = count_5
    pool.remainder_4_or_5 = count_4_or_5

    if pool.featured_resonator_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.FEATURED_RESONATOR_CONVENE.value
    elif pool.featured_weapon_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.FEATURED_WEAPON_CONVENE.value
    elif pool.standard_weapon_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.STANDARD_WEAPON_CONVENE.value
    elif pool.standard_resonator_5 > 0:
        pool.pool_type = GachaPoolTypeEnum.STANDARD_RESONATOR_CONVENE.value

    return pool


def parse(data: dict):
    pool = PoolModel()

    d = data.get("data", [])
    if len(d) == 0:
        return pool
    d = d[0]

    properties = d.get("properties", None)
    if properties is None:
        return pool

    gacha_item_id = properties.get("gacha_item_id", None)
    if gacha_item_id is None:
        return pool

    gacha_item_ids = gacha_item_id.split(",")
    gacha_item_ids = gacha_item_ids[::-1]
    pool.total = len(gacha_item_ids)
    if pool.total < 160:
        return pool

    return get_pool_by_ids(gacha_item_ids, pool=pool)
