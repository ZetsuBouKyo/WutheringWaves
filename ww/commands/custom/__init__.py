from typer import Typer

from ww.commands.custom.resonators import app as resonators
from ww.commands.custom.template import app as template

app = Typer(name="custom")
app.add_typer(resonators)
app.add_typer(template)
