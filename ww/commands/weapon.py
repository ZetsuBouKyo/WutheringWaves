from pathlib import Path

import pandas as pd
from typer import Typer

from ww.utils.table import print_table

BASE_PATH = "./data/v1/zh_tw/武器"
STAT = "屬性"
RANK = "諧振"

base_path = Path(BASE_PATH)

app = Typer(name="weapon")


@app.command()
def stat(name: str):
    resonator_stat_fpath = base_path / name / STAT
    df = pd.read_csv(resonator_stat_fpath, sep="\t")

    table_title = f"{name} {STAT}"
    print_table(table_title, df)


@app.command()
def rank(name: str):
    resonator_stat_fpath = base_path / name / RANK
    df = pd.read_csv(resonator_stat_fpath, sep="\t")

    table_title = f"{name} {RANK}"
    print_table(table_title, df)
