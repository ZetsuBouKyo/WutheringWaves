from ww.model.element import ElementEnum
from ww.model.template.calculated_row import CalculatedTemplateRowModel


def test_init():
    CalculatedTemplateRowModel()


def test():
    data = {"echo_element": ElementEnum.GLACIO.value}
    row = CalculatedTemplateRowModel(**data)
    print(row.echo_element)
