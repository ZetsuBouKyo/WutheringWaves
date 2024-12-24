import json
import os
import shutil
import subprocess
from logging import DEBUG
from pathlib import Path
from time import time

import PyInstaller.__main__
import tomli
import yaml
from typer import Option, Typer

from ww.commands.analyze import app as analyze
from ww.commands.crawl import app as crawl
from ww.commands.custom import app as custom
from ww.commands.resonator import app as resonator
from ww.commands.weapon import app as weapon
from ww.docs.export import Docs
from ww.logging import logger_cli

_help = """
The CLI for ZetsuBou
"""

app = Typer(rich_markup_mode="rich", help=_help)

app.add_typer(analyze)
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


@app.command()
def docs(
    version: str = Option(get_version()),
    config_file: str = Option("./build/html/mkdocs.yml"),
    debug_level: int = Option(DEBUG),
):
    logger_cli.setLevel(debug_level)

    t0 = time()
    # Copy the assets
    assets_src_path = "./assets"
    assets_dest_path = "./build/html/docs/assets"
    os.makedirs(assets_dest_path, exist_ok=True)
    shutil.copytree(assets_src_path, assets_dest_path, dirs_exist_ok=True)

    # Copy the docs
    docs_src_path = "./docs/html"
    docs_dest_path = "./build/html/docs"
    shutil.copytree(docs_src_path, docs_dest_path, dirs_exist_ok=True)

    docs = Docs()
    docs.export()

    t1 = time()

    try:
        # Build the mkdocs command
        command = ["mkdocs", "build", "--config-file", config_file]

        # Run the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Print the output
        print("MkDocs Build Output:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error during MkDocs build:")
        print(e.stderr)

    t2 = time()
    t2_0 = t2 - t0
    t1_0 = t1 - t0
    print(f"Create markdown files: {t1_0} (s)")
    print(f"Total: {t2_0} (s)")


@app.command()
def print_docs_settings(version: str = Option(get_version())):
    with open("mkdocs.yml", encoding="utf-8") as stream:
        try:
            settings = yaml.safe_load(stream)
            settings_str = json.dumps(settings, indent=4, ensure_ascii=False)
            print(settings_str)
        except yaml.YAMLError as exc:
            print(exc)


@app.command()
def tmp():
    # from ww.calc.simulated_resonators import Theory1SimulatedResonators
    # from ww.crud.template import get_template
    # from ww.locale import ZhTwEnum, _
    # from ww.utils.pd import save_df

    from ww.calc.simulated_echoes import SimulatedEchoes
    from ww.crud.template import get_template
    from ww.locale import ZhTwEnum, _
    from ww.utils.pd import save_df

    echoes = SimulatedEchoes()
    df = echoes.get_df()
    save_df("tmp.tsv", df, echoes.echoes_table_column_names)


if __name__ == "__main__":
    app()
