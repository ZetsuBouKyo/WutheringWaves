import csv
import os
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


def get_empty_df(column_names: List[str]) -> pd.DataFrame:
    data = {column_name: [""] for column_name in column_names}
    return pd.DataFrame(data)


def save_tsv(
    fpath: Union[str, Path],
    data: List[List[str]],
    columns: List[str],
):
    if type(fpath) is str:
        fpath = Path(fpath)
    os.makedirs(fpath.parent, exist_ok=True)
    with fpath.open(mode="w", encoding="utf-8", newline="") as fp:
        tsv = csv.writer(fp, delimiter="\t")
        tsv.writerow(columns)
        for row in data:
            tsv.writerow(row)


def init_df(fpath: Union[str, Path], column_names: List[str]) -> pd.DataFrame:
    df = get_empty_df(column_names)
    if type(fpath) is str:
        fpath = Path(fpath)
    os.makedirs(fpath.parent, exist_ok=True)
    data = df.values.tolist()
    save_tsv(fpath, data, column_names)
    return df


def safe_get_df(fpath: Union[str, Path], column_names: List[str]) -> pd.DataFrame:
    try:
        df = get_df(fpath)
        if df is not None:
            return df
    except pd.errors.EmptyDataError:
        ...

    df = get_empty_df(column_names)
    return df
