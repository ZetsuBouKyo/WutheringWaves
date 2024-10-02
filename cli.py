import os
import shutil
from pathlib import Path

import PyInstaller.__main__
import tomli
from typer import Option, Typer

from ww.commands.crawl import app as crawl
from ww.commands.custom import app as custom
from ww.commands.resonator import app as resonator
from ww.commands.weapon import app as weapon

_help = """
The CLI for ZetsuBou
"""

app = Typer(rich_markup_mode="rich", help=_help)

app.add_typer(crawl)
app.add_typer(custom)
app.add_typer(resonator)
app.add_typer(weapon)


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        toml_dict = tomli.load(f)
        version = toml_dict.get("tool", {}).get("poetry", {}).get("version", "")

    return version


@app.command()
def build(version: str = Option(get_version())):
    if not version:
        return
    # PyInstaller.__main__.run(["-y", "app.spec"])

    home = Path("./dist/releases")

    app_fname = "app.exe"
    app_path = Path("./dist") / app_fname
    if not app_path.exists():
        return

    version_1 = version
    version_2 = f"{version}-ZetsuBouKyo"

    version_1_path = home / version_1
    version_2_path = home / version_2
    os.makedirs(version_1_path, exist_ok=True)
    os.makedirs(version_2_path, exist_ok=True)

    # Copy common folders
    folder_names = ["assets", "data", "docs", "html"]
    version_paths = [version_1_path, version_2_path]
    for version_path in version_paths:
        for name in folder_names:
            copied_folder_path = version_path / name
            os.makedirs(copied_folder_path, exist_ok=True)
            shutil.copytree(name, copied_folder_path, dirs_exist_ok=True)

    # Copy `cache/v1/zh_tw/custom`
    cache_custom_path = "cache/v1/zh_tw/custom"
    copied_cache_custom_path = version_2_path / cache_custom_path
    os.makedirs(copied_cache_custom_path, exist_ok=True)
    shutil.copytree(cache_custom_path, copied_cache_custom_path, dirs_exist_ok=True)

    # Copy `cache/v1/zh_tw/output/[calculated]resonators.tsv`
    cache_calculated_resonators_fpath = (
        "cache/v1/zh_tw/output/[calculated]resonators.tsv"
    )
    copied_cache_calculated_resonators_fpath = (
        version_2_path
        / "cache"
        / "v1"
        / "zh_tw"
        / "output"
        / "[calculated]resonators.tsv"
    )
    os.makedirs(copied_cache_calculated_resonators_fpath.parent, exist_ok=True)
    shutil.copy(
        cache_calculated_resonators_fpath, copied_cache_calculated_resonators_fpath
    )

    # Copy `app.exe`
    app_1_path = version_1_path / app_fname
    app_2_path = version_2_path / app_fname
    shutil.copy(app_path, app_1_path)
    shutil.copy(app_path, app_2_path)

    # Zip
    zip_1_fpath = home / version_1
    zip_2_fpath = home / version_2
    shutil.make_archive(zip_1_fpath, "zip", version_1_path)
    shutil.make_archive(zip_2_fpath, "zip", version_2_path)


if __name__ == "__main__":
    app()
