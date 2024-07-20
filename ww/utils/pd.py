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
    index: bool = False,
):
    if type(fpath) is str:
        fpath = Path(fpath)
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(fpath, sep="\t", index=index)
