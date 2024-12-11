import hashlib
from pathlib import Path
from typing import Union

from jinja2 import Template


def get_local_file_url(path: Union[str, Path]) -> str:
    if type(path) == str:
        path = Path(path)
    abs_path = path.resolve()
    parts = []
    for part in abs_path.parts:
        parts.append(part.replace("\\", ""))
    file_url = "/".join(parts)
    return f"file:///{file_url}"


def get_jinja2_template(path: str) -> Template:
    fpath = Path(path)
    if not fpath.exists():
        raise FileNotFoundError("Jinja2 template not found")

    with fpath.open(mode="r", encoding="utf-8") as fp:
        template = Template(fp.read())

    return template


def get_md5(s: str, digit: int = 8):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:digit]
