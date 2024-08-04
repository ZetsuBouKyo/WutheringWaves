from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from ww.model.template.template_row import TemplateRowBuffTypeEnum


class TemplateBuffTableRowEnum(str, Enum):
    NAME: str = "名稱"
    TYPE: str = "種類"
    VALUE: str = "數值"
    STACK: str = "層數"
    DURATION: str = "持續時間(s)"


class TemplateBuffTableRowModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str = ""
    type: Union[TemplateRowBuffTypeEnum, str] = ""
    value: str = ""
    stack: str = ""
    duration: str = ""

    @field_validator("type")
    @classmethod
    def name_must_contain_space(cls, v: Optional[str]) -> str:
        if v not in TemplateRowBuffTypeEnum._value2member_map_:
            return ""
        return v
