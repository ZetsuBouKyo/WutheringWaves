from pathlib import Path
from typing import Optional, Union

import pandas as pd


def get_df(fpath: Union[str, Path]) -> Optional[pd.DataFrame]:
    if type(fpath) is str:
        fpath = Path(fpath)
    if not fpath.exists():
        return None
    df = pd.read_csv(fpath, sep="\t", dtype="str", keep_default_na=False)
    return df
