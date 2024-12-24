from typing import Dict, List

from pydantic import BaseModel

from ww.crud.template import get_template
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

    def get_template_ids(cls) -> List[str]:
        template_ids = set()
        for template in cls.templates:
            template_ids.add(template.id)

        for comparisons in cls.comparisons.values():
            for comparison in comparisons:
                template_ids |= set(comparison.template_ids)

        template_ids = list(template_ids)
        template_ids.sort()
        return template_ids

    def check(cls) -> bool:
        template_ids = cls.get_template_ids()
        for template_id in template_ids:
            template = get_template(template_id)

            assert template.duration_1, template_id
            assert template.duration_2, template_id

            for resonator in template.resonators:
                assert resonator.check(), template_id
        return True
