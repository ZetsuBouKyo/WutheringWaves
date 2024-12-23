from typing import Dict, List

from pydantic import BaseModel


class DocsTemplateModel(BaseModel):
    id: str = ""
    is_tier: bool = False
    echo_comparison: List[str] = []


class DocsComparisonModel(BaseModel):
    title: str = ""
    template_ids: List[str] = []


class DocsModel(BaseModel):
    templates: List[DocsTemplateModel] = []
    comparison: Dict[str, List[DocsComparisonModel]] = {}
