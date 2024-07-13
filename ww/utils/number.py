from typing import Optional


def get_number(n: Optional[str]) -> Optional[float]:
    if n is None:
        return None

    if "," in n:
        n = n.replace(",", "")
        return float(n)

    if "%" in n:
        n = n.replace("%", "")
        return float(n) / 100.0

    return float(n)
