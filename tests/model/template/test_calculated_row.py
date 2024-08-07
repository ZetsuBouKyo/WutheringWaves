from ww.model.template.calculated_row import CalculatedTemplateRowModel


def test_init():
    CalculatedTemplateRowModel()


def test():
    data = {"echo_element": ""}
    row = CalculatedTemplateRowModel(**data)
    print(row.echo_element)
