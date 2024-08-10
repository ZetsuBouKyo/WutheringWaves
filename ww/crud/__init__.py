from typing import List

from ww.model.element import ElementEnum


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]
