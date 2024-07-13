from typer import Typer

from ww.commands.custom.resonator import app as resonator

app = Typer(name="custom")
app.add_typer(resonator)
