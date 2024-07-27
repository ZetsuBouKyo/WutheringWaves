import re
from typing import List


def _convert(text) -> int:
    return int(text) if text.isdigit() else text


def alphanum_sorting(ls: List[str]) -> List[str]:
    ls.sort(key=lambda text: [_convert(c) for c in re.split("([0-9]+)", text)])
    return ls
