from typing import List

from pydantic import BaseModel


class DocsTemplateModel(BaseModel):
    id: str = ""
    is_tier: bool = False
    echo_comparison: List[str] = []


class DocsModel(BaseModel):
    templates: List[DocsTemplateModel] = []
