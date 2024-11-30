from typing import Dict, List

from pydantic import BaseModel


class DamageCompareModel(BaseModel):
    id: str = ""
    data: Dict[str, List[str]] = {}
