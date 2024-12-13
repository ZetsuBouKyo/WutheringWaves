from decimal import Decimal
from typing import List

from ww.utils.number import get_number

DEFAULT_MAX_DAMAGE = 1000000
DAMAGE_TICK = 500000


def get_max_damage(
    dmgs: List[Decimal],
    default_max_damage: Decimal = Decimal(DEFAULT_MAX_DAMAGE),
    tick: Decimal = Decimal(DAMAGE_TICK),
) -> Decimal:
    if len(dmgs) == 0:
        return default_max_damage

    max_dmg = -Decimal("Infinity")
    for dmg in dmgs:
        dmg = get_number(dmg)
        if dmg > max_dmg:
            max_dmg = dmg
    if max_dmg < default_max_damage:
        return default_max_damage

    quotient, remainder = divmod(max_dmg, tick)
    if remainder > Decimal(0):
        return (quotient + 1) * tick
    return quotient * tick
