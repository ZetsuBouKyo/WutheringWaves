from decimal import Decimal, InvalidOperation
from typing import Optional, Union

import numpy as np

from ww.model import Number


def get_number(n: Optional[Number]) -> Decimal:
    if n is None or n == "" or n == np.nan:
        return Decimal("0.0")

    if type(n) is Decimal:
        return n
    elif type(n) is int or type(n) is float:
        return Decimal(n)

    if "," in n:
        n = n.replace(",", "")

    try:
        if "%" in n:
            n = n.replace("%", "")
            return Decimal(n) / Decimal("100.0")

        return Decimal(n)
    except (TypeError, InvalidOperation):
        return Decimal("0.0")


def get_string(n: Optional[str]) -> Optional[str]:
    if n is None:
        return ""
    elif n is np.nan:
        return ""
    return str(n)
