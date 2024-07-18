from enum import Enum
from typing import Any, Optional

import pandas as pd


def search(df: pd.DataFrame, id: str, col: Enum, id_col_name: str) -> Optional[Any]:
    if not id or df is None or col not in df.columns:
        return None

    rows = df.loc[df[id_col_name] == id]
    assert len(rows.values) <= 1, f"ID: {id} must be unique"
    if len(rows.values) == 0:
        # print(f"ID: {id} not found")
        return None

    cells = rows[col].values
    assert len(cells) <= 1, f"Column name: {col} must be unique"
    if len(cells) == 0:
        # print(f"ID: {id} with column: {col} not found")
        return None

    return cells[0]
