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


def to_number_string(n) -> str:
    if not n:
        return ""
    if type(n) is str:
        n = Decimal(n)
    return f"{n:,.2f}"


def to_trimmed_number_string(n) -> str:
    if not n:
        return ""
    if type(n) is str:
        n = Decimal(n)
    return np.format_float_positional(n, 6, trim="-")


def get_string(n: Optional[str]) -> Optional[str]:
    if n is None:
        return ""
    elif n is np.nan:
        return ""
    return str(n)


def get_percentage_str(
    numerator: Optional[Decimal], denominator: Optional[Decimal]
) -> str:
    numerator = get_number(numerator)
    denominator = get_number(denominator)
    if not denominator:
        return "0.00%"
    percentage = numerator / denominator
    return f"{percentage:.2%}"


def to_percentage_str(percentage) -> str:
    percentage = get_number(percentage)
    return f"{percentage:.2%}"
