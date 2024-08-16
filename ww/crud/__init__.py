from typing import List

from ww.model import SkillBaseAttrEnum
from ww.model.element import ElementEnum
from ww.model.template.buff_table import TemplateRowBuffTypeEnum
from ww.model.template.template_row import TemplateRowActionEnum


def get_elements() -> List[str]:
    return [e.value for e in ElementEnum]


def get_buff_types() -> List[str]:
    return [e.value for e in TemplateRowBuffTypeEnum]


def get_actions() -> List[str]:
    return [e.value for e in TemplateRowActionEnum]


def get_skill_base_attributes() -> List[str]:
    return [e.value for e in SkillBaseAttrEnum]
