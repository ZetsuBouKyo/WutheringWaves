from pathlib import Path
from typing import List, Optional

from ww.utils.pd import get_empty_df, safe_get_df


class BaseTable:
    def __init__(self, fpath: Optional[Path], column_names: List[str]):
        self.column_names = column_names
        if fpath is not None:
            self.df = safe_get_df(fpath, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)
