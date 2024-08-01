import os
from pathlib import Path
from typing import List

from ww.model.template import TemplateModel

TEMPLATE_HOME_PATH = "./cache/v1/custom/template"


def get_template(tempalte_id: str) -> TemplateModel:
    template_home_path = Path(TEMPLATE_HOME_PATH)
    os.makedirs(template_home_path, exist_ok=True)
    template_path = template_home_path / tempalte_id
    if template_path.is_dir() or not template_path.exists():
        return TemplateModel()
    return
