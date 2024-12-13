from pathlib import Path
from typing import Optional

import mistune

DOCS_HOME_PATH = "./docs/app/home.md"

DOCS_GACHA_FILE_PATH = "./docs/app/gacha/file.md"


def _get_html(fpath: str) -> Optional[str]:
    p = Path(fpath)
    if not p.exists():
        return None
    with p.open(mode="r", encoding="utf-8") as fp:
        text = fp.read()

    return mistune.html(text)


def get_home_html() -> Optional[str]:
    return _get_html(DOCS_HOME_PATH)


def get_gacha_file_html() -> Optional[str]:
    return _get_html(DOCS_GACHA_FILE_PATH)
