from pathlib import Path
from typing import Optional

import mistune

DOCS_HOME_PATH = "./docs/home.md"


def get_home_html() -> Optional[str]:
    p = Path(DOCS_HOME_PATH)
    if not p.exists():
        return None
    with p.open(mode="r", encoding="utf-8") as fp:
        text = fp.read()

    return mistune.html(text)
