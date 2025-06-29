import enum
from pathlib import Path

import typer
from rich import print
from typing_extensions import Annotated

import sd_utils.advancement_charts as ac
from sd_utils.todo_lists import make_todo

app = typer.Typer()


class PivotDirection(enum.Enum):
    H: str = "H"
    # TODO: Weird errors with V. Can't investigate now...
    # V: str = "V"


@app.command(
    "make-adv-chart",
    help="Convert the downloadable advancement chart from scouts digital into something more aesthetically pleasing. Work in progress, very unpolished.",
    no_args_is_help=True,
)
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


@app.command(
    "make-todo-list",
    help="For each scout, produce a list of un-finished items in the form of a todo list. Requires the downloaded advancement chart.",
    no_args_is_help=True,
)
def cli_make_todo(
    input_file: Annotated[Path, typer.Argument()],
    output_file: Annotated[Path, typer.Argument()],
    full_export: Annotated[bool, typer.Option("--full/--minimal")] = True,
):
    print(f"Reading advancement chart from [bold purple]{input_file}[/bold purple].")
    make_todo(input_file, output_file, full_export)
    print(f"Wrote output to [bold blue]{output_file}[/bold blue].")
    pass


def cli_entrypoint():
    app()


if __name__ == "__main__":
    cli_entrypoint()
