from typing import Dict, List

from pydantic import BaseModel

from ww.utils import get_md5


class DocsTemplateModel(BaseModel):
    id: str = ""
    is_tier: bool = False
    echo_comparison: List[str] = []


class DocsComparisonModel(BaseModel):
    title: str = ""
    template_ids: List[str] = []

    def get_md5(cls) -> str:
        return get_md5(cls.title)


class DocsModel(BaseModel):
    templates: List[DocsTemplateModel] = []
    comparisons: Dict[str, List[DocsComparisonModel]] = {}
