import enum
from pathlib import Path

import typer
from rich import print
from typing_extensions import Annotated

import sd_utils.advancement_charts as ac
from sd_utils.todo_lists import (
    make_todo,
    read_scout_name_file,
    write_full_scout_namefile,
)

app = typer.Typer(
    add_completion=False, help="Tool to manipulate the output of SD advancement charts."
)


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
            "--full/--minimal",
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
    input_file: Annotated[
        Path, typer.Argument(help="Path to the excel file downloaded from SD.")
    ],
    output_file: Annotated[
        Path,
        typer.Argument(
            help="Path to write the output file. Remember to include the filename, eg /path/to/output.pdf"
        ),
    ],
    full_export: Annotated[
        bool,
        typer.Option(
            "--full/--minimal",
            help="Is this a full export (with dates) or a minimal export (with Xs)",
        ),
    ] = True,
    num_levels: Annotated[
        str, typer.Option(help="How many levels per scout to export.")
    ] = 1,
    name_file: Annotated[
        Path,
        typer.Option(
            help="Optionally supply a plain text file with the names of scouts to make todo lists for. Note these names must match the 'short names'. See the get-names command for help"
        ),
    ] = None,
    names: Annotated[
        str,
        typer.Option(
            help="Provide a string of comma-separated values with the names of scouts to create todo lists for"
        ),
    ] = None,
):
    if name_file and names:
        print("[bold red]Please only supply one of name_file or names[/bold red]")
        exit(1)

    if names:
        names = [n.strip() for n in names.split(",")]

    if name_file:
        names = read_scout_name_file(name_file)
        print(names)

    print(f"Reading advancement chart from [bold purple]{input_file}[/bold purple].")
    make_todo(
        input_file, output_file, full_export, scout_names=names, num_levels=num_levels
    )
    print(f"Wrote output to [bold blue]{output_file}[/bold blue].")
    pass


@app.command("get-names")
def cli_get_scout_names(
    input_file: Annotated[Path, typer.Argument()],
    output_file: Annotated[Path, typer.Option()] = None,
    full_export: Annotated[bool, typer.Option("--full/--minimal")] = True,
):
    write_full_scout_namefile(input_file, output_file, full_export)
    pass


def cli_entrypoint():
    app()


if __name__ == "__main__":
    cli_entrypoint()
