from typer import Argument, Option, Typer

from ww.commands.custom.template.damage import get_damage

app = Typer(name="template")


@app.command()
def damage(
    template_id: str = Argument(...),
    monster_name: str = Argument(...),
    r_id_1: str = Option(default=None, help="Resonator ID 1"),
    r_id_2: str = Option(default=None, help="Resonator ID 2"),
    r_id_3: str = Option(default=None, help="Resonator ID 3"),
):
    get_damage(template_id, monster_name, r_id_1, r_id_2, r_id_3)


@app.command()
def list(): ...
