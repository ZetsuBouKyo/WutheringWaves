import numpy as np


def get_number(n: str) -> float:
    if n is None:
        return 0.0
    elif n is np.nan:
        return 0.0

    if "," in n:
        n = n.replace(",", "")
        return float(n)

    if "%" in n:
        n = n.replace("%", "")
        return float(n) / 100.0

    return float(n)
