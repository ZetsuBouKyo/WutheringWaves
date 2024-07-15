from typer import Argument, Option, Typer

from ww.commands.custom.template.damage import get_damage

app = Typer(name="template")


@app.command()
def damage(
    template_id: str = Argument(...),
    r1: str = Option(default=None, help="Resonator ID 1"),
    r2: str = Option(default=None, help="Resonator ID 2"),
    r3: str = Option(default=None, help="Resonator ID 3"),
):
    get_damage(template_id, r1, r2, r3)


@app.command()
def list(): ...
