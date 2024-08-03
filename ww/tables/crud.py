from enum import Enum
from typing import Any, Dict, List, Optional

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


def get_col(df: pd.DataFrame, col_name: str, ignore_empty: bool = True) -> List[str]:
    if ignore_empty:
        return [cell for cell in df[col_name].to_list() if cell]
    return [cell for cell in df[col_name].to_list()]


def get_row(df: pd.DataFrame, id: str, id_col_name: str) -> Optional[pd.DataFrame]:
    if not id or df is None:
        return None

    rows = df.loc[df[id_col_name] == id]
    assert len(rows.values) <= 1, f"ID: {id} must be unique"
    if len(rows.values) == 0:
        # print(f"ID: {id} not found")
        return None

    return rows


def get_rows(df: pd.DataFrame, id: str, id_col_name: str) -> Optional[pd.DataFrame]:
    if not id or df is None:
        return None

    rows = df.loc[df[id_col_name] == id]
    if len(rows.values) == 0:
        # print(f"ID: {id} not found")
        return None

    return rows


def get_cell_by_row(df: pd.DataFrame, col_name: str) -> Optional[Any]:
    cells = df[df.columns.get_loc(col_name)].values
    assert len(cells) <= 1, f"Column name: {col_name} must be unique"
    if len(cells) == 0:
        # print(f"ID: {id} with column: {col} not found")
        return None

    return cells[0]


def df_to_list(df: Optional[pd.DataFrame]) -> List[Dict[str, str]]:
    if df is None:
        return []
    return [r for r in df.to_dict(orient="records")]
