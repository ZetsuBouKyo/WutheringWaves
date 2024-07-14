from decimal import Decimal

import numpy as np


def get_number(n: str) -> float:
    if n is None:
        return Decimal("0.0")
    elif n is np.nan:
        return Decimal("0.0")

    if "," in n:
        n = n.replace(",", "")

    if "%" in n:
        n = n.replace("%", "")
        return Decimal(n) / Decimal("100.0")

    return Decimal(n)
