from typer import Typer

from ww.commands.custom.resonators import app as resonators

app = Typer(name="custom")
app.add_typer(resonators)
