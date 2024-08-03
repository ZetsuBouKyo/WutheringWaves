from ww.model.buff import ResonatorBuffEnum
from ww.tables.buff import ResonatorBuffTable
from ww.tables.crud import get_cell_by_row


def test_resonator_buff_table():
    table = ResonatorBuffTable()
    name = "維里奈"
    rows = table.get_rows(name)
    for i in range(rows.shape[0]):
        print(rows.loc[i, ResonatorBuffEnum.VALUE.value])
