from typing import List

from ww.model.echoes import EchoListEnum, EchoSonataEnum
from ww.tables.echoes import EchoListEnum, EchoListTable


def get_echo_names() -> List[str]:
    echo_list_table = EchoListTable()
    echo_list = [row[EchoListEnum.ID] for _, row in echo_list_table.df.iterrows()]
    return echo_list


def get_echo_sonatas() -> List[str]:
    return [e.value for e in EchoSonataEnum]