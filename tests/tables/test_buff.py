from ww.model.buff import ResonatorBuffTsvColumnEnum
from ww.tables.buff import ResonatorBuffTable
from ww.tables.crud import get_cell_by_row


def test_resonator_buff_table():
    table = ResonatorBuffTable()
    name = "維里奈"
    rows = table.get_rows(name)
    print(rows)
