from pathlib import Path
from typing import Union


def get_local_file_url(path: Union[str, Path]) -> str:
    if type(path) == str:
        path = Path(path)
    abs_path = path.resolve()
    parts = []
    for part in abs_path.parts:
        parts.append(part.replace("\\", ""))
    file_url = "/".join(parts)
    return f"file:///{file_url}"
