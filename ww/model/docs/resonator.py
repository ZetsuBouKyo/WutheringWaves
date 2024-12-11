from typing import List

from pydantic import BaseModel


class DocsResonatorModel(BaseModel):
    name: str = ""
    template_ids: List[str] = []
