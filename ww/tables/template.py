from pathlib import Path

from ww.utils.pd import get_df

TEMPLATE_HOME_PATH = "./data/自訂/模板"


class TemplateTable:
    def __init__(self, id: str):
        fname = f"{id}.tsv"
        _stat_path = Path(TEMPLATE_HOME_PATH) / fname
        self.df = get_df(_stat_path)
