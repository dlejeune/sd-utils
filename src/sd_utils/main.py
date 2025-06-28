import enum
from pathlib import Path

import advancement_charts as ac
import typer
from rich import print
from typing_extensions import Annotated

app = typer.Typer()


class PivotDirection(enum.Enum):
    H: str = "H"
    # TODO: Weird errors with V. Can't investigate now...
    # V: str = "V"


@app.command()
def cli_make_adv_chart(
    input_file: Annotated[Path, typer.Argument()],
    output_file: Annotated[Path, typer.Argument()],
    is_input_full_export: Annotated[
        bool,
        typer.Option(
            "--full",
            "-f",
            help="Is the input file provided a full export or a minimal export",
        ),
    ] = True,
    pivot_direction: Annotated[
        PivotDirection, typer.Option("--direction", "-d")
    ] = PivotDirection.H,
):
    chart_maker = ac.AdvancementUtils()

    chart_maker.create_advancement_sheets(
        input_file, output_file, is_input_full_export, pivot_direction.value
    )
    print(f"Wrote output to [bold blue]{output_file}[/bold blue].")
    pass


def cli_entrypoint():
    app()


if __name__ == "__main__":
    cli_entrypoint()
