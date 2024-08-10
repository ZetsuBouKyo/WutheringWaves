import json
import os
from pathlib import Path
from typing import List, Optional

from ww.model.template import TemplateModel

TEMPLATE_HOME_PATH = "./cache/v1/zh_tw/custom/template"


def get_template_path(
    template_id: str, template_home_path: str = TEMPLATE_HOME_PATH
) -> Optional[Path]:
    if not template_id:
        return None
    template_fname = f"{template_id}.json"
    template_home_path = Path(template_home_path)
    template_path = template_home_path / template_fname
    return template_path


def get_template(
    tempalte_id: str, template_home_path: str = TEMPLATE_HOME_PATH
) -> Optional[TemplateModel]:
    template_path = get_template_path(
        tempalte_id, template_home_path=template_home_path
    )
    if template_path is None or template_path.is_dir() or not template_path.exists():
        return None
    with template_path.open(mode="r", encoding="utf-8") as fp:
        template = json.load(fp)
    return TemplateModel(**template)


def get_template_ids(template_home_path: str = TEMPLATE_HOME_PATH) -> List[str]:
    home_path = Path(template_home_path)
    names = [p.stem for p in home_path.glob("*.json")]
    return names


def save_template(
    tempalte_id: str,
    tempalte: TemplateModel,
    template_home_path: str = TEMPLATE_HOME_PATH,
):
    template_home_path = Path(template_home_path)
    os.makedirs(template_home_path, exist_ok=True)

    template_path = get_template_path(
        tempalte_id, template_home_path=template_home_path
    )

    with template_path.open(mode="w", encoding="utf-8") as fp:
        data = tempalte.model_dump_json(indent=4)
        fp.write(data)
