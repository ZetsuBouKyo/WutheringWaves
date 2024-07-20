import csv
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd


def get_df(fpath: Union[str, Path]) -> Optional[pd.DataFrame]:
    if type(fpath) is str:
        fpath = Path(fpath)
    if not fpath.exists():
        return None
    df = pd.read_csv(fpath, sep="\t", dtype="str", keep_default_na=False)
    return df


def save_tsv(
    fpath: Union[str, Path],
    data: List[List[str]],
    columns: List[str],
):
    if type(fpath) is str:
        fpath = Path(fpath)
    with fpath.open(mode="w", encoding="utf-8", newline="") as fp:
        tsv = csv.writer(fp, delimiter="\t")
        tsv.writerow(columns)
        for row in data:
            tsv.writerow(row)
