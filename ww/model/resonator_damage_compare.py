from typing import Dict, List

from pydantic import BaseModel


class ResonatorDamageCompareModel(BaseModel):
    id: str = ""
    data: Dict[str, List[str]] = {}
