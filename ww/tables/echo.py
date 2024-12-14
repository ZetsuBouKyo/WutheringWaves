import json
from pathlib import Path
from typing import Any, List, Optional

from ww.model.echo import (
    EchoMainAffixesModel,
    EchoModel,
    EchoSkillTsvColumnEnum,
    EchoSonataEnum,
    EchoSubAffixesModel,
    EchoTsvColumnEnum,
    ResonatorEchoTsvColumnEnum,
)
from ww.tables.crud import search
from ww.utils.pd import get_empty_df, safe_get_df

ECHOES_PATH = "./cache/v1/zh_tw/custom/echo/echoes.tsv"
ECHOES_HTML_PATH = "./cache/v1/zh_tw/output/echoes.html"
ECHOES_PNG_FNAME = "echoes.png"

ECHOES_LIST_PATH = "./data/v1/zh_tw/echo_list.tsv"
ECHO_SKILL_PATH = "./data/v1/zh_tw/echo_skills.tsv"
ECHO_SKILL_DESCRIPTIONS_PATH = "./data/v1/zh_tw/echo_skill_descriptions.json"
ECHO_SONATA_DESCRIPTIONS_PATH = "./data/v1/zh_tw/echo_sonata_descriptions.json"

ECHO_FPATH = "./data/v1/zh_tw/echo.json"
ECHO_MAIN_AFFIXES_FPATH = "./data/v1/zh_tw/echo_main_affixes.json"
ECHO_SUB_AFFIXES_FPATH = "./data/v1/zh_tw/echo_sub_affixes.json"


def get_echo_list_fpath() -> Path:
    return Path(ECHOES_LIST_PATH)


def get_echo_skill_fpath() -> Path:
    return Path(ECHO_SKILL_PATH)


def get_echo_skill_descriptions_fpath() -> Path:
    return Path(ECHO_SKILL_DESCRIPTIONS_PATH)


def get_echo_sonata_descriptions_fpath() -> Path:
    return Path(ECHO_SONATA_DESCRIPTIONS_PATH)


class EchoTable:
    def __init__(self, fpath: str = ECHO_FPATH):
        _fpath = Path(fpath)
        if _fpath.exists():
            with _fpath.open(mode="r", encoding="utf-8") as fp:
                data = json.load(fp)
        else:
            data = []

        self.data: List[EchoModel] = []
        for i in range(len(data)):
            echo = EchoModel(**data[i])
            self.data.append(echo)

    def get_names(self) -> List[str]:
        return [d.name for d in self.data]

    def has_44111(self, sonatas: List[EchoSonataEnum]) -> bool:
        for i in range(len(sonatas)):
            if type(sonatas[i]) is EchoSonataEnum:
                sonatas[i] = sonatas[i].value

        echoes_4c: List[EchoModel] = []
        for echo in self.data:
            if echo.cost == 4:
                echoes_4c.append(echo)

        used_echo_names = set()
        for sonata in sonatas:
            for echo in echoes_4c:
                if sonata in echo.sonatas:
                    used_echo_names.add(echo.name)

        if len(used_echo_names) > 1:
            return True
        return False


class EchoesTable:
    def __init__(self):
        column_names = [e.value for e in ResonatorEchoTsvColumnEnum]
        self.df = safe_get_df(ECHOES_PATH, column_names)

    def search(self, id: str, col: ResonatorEchoTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, ResonatorEchoTsvColumnEnum.ID.value)


class EchoListTable:
    def __init__(self):
        _path = get_echo_list_fpath()
        self.column_names = [e.value for e in EchoTsvColumnEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: EchoTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoTsvColumnEnum.PRIMARY_KEY.value)


class EchoSkillTable:
    def __init__(self):
        _path = get_echo_skill_fpath()
        self.column_names = [e.value for e in EchoSkillTsvColumnEnum]
        if _path is not None:
            self.df = safe_get_df(_path, self.column_names)
        else:
            self.df = get_empty_df(self.column_names)

    def search(self, id: str, col: EchoSkillTsvColumnEnum) -> Optional[Any]:
        return search(self.df, id, col, EchoSkillTsvColumnEnum.PRIMARY_KEY.value)


class EchoMainAffixesTable:

    def __init__(self, fpath: str = ECHO_MAIN_AFFIXES_FPATH):
        _fpath = Path(fpath)
        with _fpath.open(mode="r", encoding="utf-8") as fp:
            data = json.load(fp)

        self.data = EchoMainAffixesModel(**data)

    def get_main_affixes(self) -> EchoMainAffixesModel:
        return self.data


class EchoSubAffixesTable:

    def __init__(self, fpath: str = ECHO_SUB_AFFIXES_FPATH):
        _fpath = Path(fpath)
        with _fpath.open(mode="r", encoding="utf-8") as fp:
            data = json.load(fp)
        self.data = EchoSubAffixesModel(**data)

    def get_sub_affixes(self) -> EchoSubAffixesModel:
        return self.data
