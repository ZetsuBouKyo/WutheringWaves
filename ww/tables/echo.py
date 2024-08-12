from pathlib import Path
from typing import Any, Optional

from ww.model.echo import EchoesEnum, EchoListEnum, EchoSkillEnum
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

ECHOES_PATH = "./cache/v1/zh_tw/custom/echo/echoes.tsv"
ECHOES_HTML_PATH = "./cache/v1/zh_tw/output/echoes.html"
ECHOES_PNG_FNAME = "echoes.png"

ECHOES_LIST_PATH = "./data/v1/zh_tw/echo_list.tsv"
ECHO_SKILL_PATH = "./data/v1/zh_tw/echo_skills.tsv"
ECHO_SKILL_DESCRIPTIONS_PATH = "./data/v1/zh_tw/echo_skill_descriptions.json"
ECHO_SONATA_DESCRIPTIONS_PATH = "./data/v1/zh_tw/echo_sonata_descriptions.json"


def get_echo_list_fpath() -> Path:
    return Path(ECHOES_LIST_PATH)


def get_echo_skill_fpath() -> Path:
    return Path(ECHO_SKILL_PATH)


def get_echo_skill_descriptions_fpath() -> Path:
    return Path(ECHO_SKILL_DESCRIPTIONS_PATH)


def get_echo_sonata_descriptions_fpath() -> Path:
    return Path(ECHO_SONATA_DESCRIPTIONS_PATH)


class EchoesTable:
    def __init__(self):
        column_names = [e.value for e in EchoesEnum]
        self.df = safe_get_df(ECHOES_PATH, column_names)

    def search(self, id: str, col: EchoesEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoesEnum.ID.value)


class EchoListTable:
    def __init__(self):
        _path = get_echo_list_fpath()
        self.column_names = [e.value for e in EchoListEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: EchoListEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoListEnum.PRIMARY_KEY.value)


class EchoSkillTable:
    def __init__(self):
        _path = get_echo_skill_fpath()
        self.column_names = [e.value for e in EchoSkillEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: EchoSkillEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoSkillEnum.PRIMARY_KEY.value)
