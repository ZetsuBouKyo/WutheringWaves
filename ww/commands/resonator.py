from pathlib import Path

import pandas as pd
from typer import Typer

from ww.utils.table import print_table

BASE_PATH = "./data/角色"
STAT = "屬性"
SKILL = "技能"

base_path = Path(BASE_PATH)

app = Typer(name="resonator")


@app.command()
def stat(name: str):
    resonator_stat_fpath = base_path / name / STAT
    df = pd.read_csv(resonator_stat_fpath, sep="\t")

    table_title = f"{name} {STAT}"
    print_table(table_title, df)


@app.command()
def skill(name: str):
    resonator_stat_fpath = base_path / name / SKILL
    df = pd.read_csv(resonator_stat_fpath, sep="\t")

    table_title = f"{name} {SKILL}"
    print_table(table_title, df)
