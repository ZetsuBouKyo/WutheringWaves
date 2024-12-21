from typing import List

from pydantic import BaseModel

from ww.model.docs.resonator import DocsResonatorModel


class DocsTierModel(BaseModel):
    template_ids: List[str] = []


class DocsModel(BaseModel):
    resonators: List[DocsResonatorModel] = []
    tier: DocsTierModel = DocsTierModel()
