from typing import List

from ww.model.echo import EchoesEnum, EchoListEnum, EchoSonataEnum
from ww.tables.echo import EchoesTable, EchoListEnum, EchoListTable


def get_echo_names() -> List[str]:
    echo_list_table = EchoListTable()
    echo_list = [
        row[EchoListEnum.PRIMARY_KEY] for _, row in echo_list_table.df.iterrows()
    ]
    return echo_list


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]


def get_echoes() -> List[str]:
    echoes_table = EchoesTable()
    echoes = echoes_table.df[EchoesEnum.ID]
    return echoes.to_list()
