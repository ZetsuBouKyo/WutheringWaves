from typing import List

from ww.locale import ZhTwEnum, _
from ww.model.echo import EchoSonataEnum, EchoTsvColumnEnum, ResonatorEchoTsvColumnEnum
from ww.tables.echo import EchoesTable, EchoListTable, EchoTsvColumnEnum


def get_echo_names() -> List[str]:
    echo_list_table = EchoListTable()
    echo_list = [
        row[EchoTsvColumnEnum.PRIMARY_KEY] for _, row in echo_list_table.df.iterrows()
    ]
    return echo_list


def get_echo_costs() -> List[str]:
    return ["4", "3", "1"]


def get_echo_affixes() -> List[str]:
    return [
        _(ZhTwEnum.ABBR_HP),
        _(ZhTwEnum.ABBR_ATK),
        _(ZhTwEnum.ABBR_DEF),
        _(ZhTwEnum.ABBR_CRIT_RATE),
        _(ZhTwEnum.ABBR_CRIT_DMG),
        _(ZhTwEnum.ABBR_ENERGY_REGEN),
        _(ZhTwEnum.ABBR_RESONANCE_SKILL),
        _(ZhTwEnum.ABBR_BASIC_ATTACK),
        _(ZhTwEnum.ABBR_HEAVY_ATTACK),
        _(ZhTwEnum.ABBR_RESONANCE_LIBERATION),
        _(ZhTwEnum.ABBR_HEALING),
        _(ZhTwEnum.GLACIO),
        _(ZhTwEnum.FUSION),
        _(ZhTwEnum.ELECTRO),
        _(ZhTwEnum.AERO),
        _(ZhTwEnum.SPECTRO),
        _(ZhTwEnum.HAVOC),
    ]


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


def get_echoes() -> List[str]:
    echoes_table = EchoesTable()
    echoes = echoes_table.df[ResonatorEchoTsvColumnEnum.ID]
    return echoes.to_list()
