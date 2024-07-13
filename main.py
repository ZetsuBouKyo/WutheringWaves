from typer import Typer

from ww.commands.custom import app as custom
from ww.commands.resonator import app as resonator
from ww.commands.weapon import app as weapon

_help = """
The CLI for ZetsuBou
"""

app = Typer(rich_markup_mode="rich", help=_help)

app.add_typer(custom)
app.add_typer(resonator)
app.add_typer(weapon)


if __name__ == "__main__":
    app()
