from pathlib import Path
from typing import Union

import pandas as pd


def get_df(fpath: Union[str, Path]) -> pd.DataFrame:
    if type(fpath) is str:
        fpath = Path(fpath)
    df = pd.read_csv(fpath, sep="\t")
    return df
