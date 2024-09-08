from typer import Argument, Option, Typer

app = Typer(name="template")


@app.command()
def damage(
    template_id: str = Argument(...),
    monster_name: str = Argument(...),
    r_id_1: str = Option(default=None, help="Resonator ID 1"),
    r_id_2: str = Option(default=None, help="Resonator ID 2"),
    r_id_3: str = Option(default=None, help="Resonator ID 3"),
): ...


@app.command()
def list(): ...
