from typing import Dict, List

from pydantic import BaseModel

from ww.crud.template import get_template
from ww.utils import get_md5


class DocsTemplateModel(BaseModel):
    id: str = ""
    is_tier: bool = False
    is_1_1_tier: bool = False
    is_2_1_tier: bool = False
    is_3_1_tier: bool = False
    is_4_1_tier: bool = False
    is_5_1_tier: bool = False
    is_6_1_tier: bool = False
    is_6_5_tier: bool = False
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


class DocsTierModel(BaseModel):
    title: str = ""
    msg: str = ""

    ids: List[str] = []


class DocsTiersModel(BaseModel):
    t: DocsTierModel = DocsTierModel()
    t_1_1: DocsTierModel = DocsTierModel()
    t_2_1: DocsTierModel = DocsTierModel()
    t_3_1: DocsTierModel = DocsTierModel()
    t_4_1: DocsTierModel = DocsTierModel()
    t_5_1: DocsTierModel = DocsTierModel()
    t_6_1: DocsTierModel = DocsTierModel()
    t_6_5: DocsTierModel = DocsTierModel()
