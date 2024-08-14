from pathlib import Path


def get_url(path: Path) -> str:
    abs_path = path.resolve()
    parts = []
    for part in abs_path.parts:
        parts.append(part.replace("\\", ""))
    file_url = "/".join(parts)
    return f"file:///{file_url}"
