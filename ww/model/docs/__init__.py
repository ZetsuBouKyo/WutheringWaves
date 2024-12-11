from typing import List

from pydantic import BaseModel

from ww.model.docs.resonator import DocsResonatorModel


class DocsModel(BaseModel):
    resonators: List[DocsResonatorModel] = []
