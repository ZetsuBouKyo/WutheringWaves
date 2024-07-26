from pathlib import Path
from typing import Any, List, Optional

from ww.model.templates import TemplatesEnum
from ww.tables.crud import search
from ww.utils.pd import get_df

TEMPLATES_HOME_PATH = "./cache/自訂/模板"


def get_template_ids() -> List[str]:
    home = Path(TEMPLATES_HOME_PATH)
    return [t.stem for t in home.glob("*")]
