from typer import Typer

from ww.commands.analyze.crit import app as crit

app = Typer(name="analyze")

app.add_typer(crit)
