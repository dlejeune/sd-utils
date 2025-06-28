import subprocess
from pathlib import Path

import jinja2
import numpy as np
import pandas as pd
from rich import print

TEMPLATE_DIR = Path(
    "/home/dlejeune/Documents/scouts/dashboard/src/dashboard/todo_templates/"
)


def make_todo(raw_adv_chart: Path, output_location: Path):
    adv_chart_df = parse_advancement_chart(raw_adv_chart)

    todo_dict = build_todo_dict(adv_chart_df, "all")
    print(__name__)

    hydrate_templates(output_location, todo_dict)
    pass


def hydrate_templates(output_file: Path, data: dict, keep_tex: bool = False):
    latex_jinja_env = jinja2.Environment(
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.PackageLoader("sd_utils.todo_lists"),
    )

    template = latex_jinja_env.get_template("todo_template.tex")

    with output_file.with_suffix(".tex").open("w") as file:
        file.write(template.render(data=data))

    result = subprocess.call(
        f"latexmk -xelatex -interaction=batchmode {output_file}",
        shell=True,
        cwd=output_file.parent,
    )

    if result != 0:
        exit(result)

    subprocess.call(
        "latexmk -c",
        shell=True,
        cwd=output_file.parent,
    )


def trim_name(name_str):
    name_arr = name_str.split(" ")
    initial = name_arr[1][0:1]

    return "{} {}".format(name_arr[0], initial)


def parse_advancement_chart(file):
    df = pd.read_excel(file)
    df = df.drop(["Age", "Invested", "End"], axis=1)
    df = pd.melt(
        df, id_vars=["Patrol", "Name"], var_name="Requirement", value_name="Passed"
    )
    df.fillna(value=False, inplace=True)

    df[["Temp", "DatePassed", "Scouter"]] = df["Passed"].str.split(
        "\n", n=2, expand=True
    )
    df = df.drop(["Temp"], axis=1)
    df.loc[df["Passed"] != False, "Passed"] = True
    df = df.replace({np.nan: None})

    df[df["DatePassed"] != None]
    df["DatePassed"] = df["DatePassed"].str.extract(
        r"(\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$)", expand=False
    )[0]
    df["DatePassed"] = pd.to_datetime(df["DatePassed"])
    df["Scouter"] = df["Scouter"].str.slice(start=3)

    df[["Name", "id"]] = df["Name"].str.split("\n", expand=True)

    df["Name"] = df["Name"].apply(trim_name)
    df[["Level", "Requirement", "Theme"]] = df["Requirement"].str.split(
        "\n", n=2, expand=True
    )

    df["Theme"] = df["Theme"].str.replace(" \\(", "", regex=True)
    df["Theme"] = df["Theme"].str.replace("\\)", "", regex=True)

    df[["Theme", "Patrol"]] = df[["Theme", "Patrol"]].astype("category")

    cat_type = pd.CategoricalDtype(
        categories=["Membership", "Traveller", "Discoverer", "1st Class", "Springbok"],
        ordered=True,
    )

    df["Level"] = df["Level"].astype(cat_type)

    df["Theme"] = df["Theme"].cat.rename_categories(
        {
            "Safety Awareness Theme": "Safety",
            "Living Outdoors Theme": "Living Outdoors",
            "Adventure Theme": "Adventure",
            "Skills Theme": "Scout Skills",
            "Service Theme": "Service",
            "Personal Development Theme": "Personal Dev",
        }
    )

    df["Theme"] = df["Theme"].cat.reorder_categories(
        [
            "Safety",
            "Living Outdoors",
            "Adventure",
            "Scout Skills",
            "Service",
            "Personal Dev",
            "",
        ]
    )
    df = df.replace({np.nan: None})

    adv_df = df.copy()

    return adv_df


def build_todo_dict(df, scouts):
    # cat_type = pd.CategoricalDtype(
    #     categories=["Membership", "Traveller", "Discoverer", "1st Class", "Springbok"],
    #     ordered=True,
    # )
    df = df.loc[df["Passed"] == False, :]

    if scouts != "all":
        df = df[df["Name"] == scouts]

    # print(df.loc[df.groupby(["Patrol", "Name"], observed=True)["Level"].idxmin()])
    df = df.merge(
        df.loc[df.groupby(["Patrol", "Name"], observed=True)["Level"].idxmin()][
            ["Patrol", "Name", "Level"]
        ],
        on=["Patrol", "Name", "Level"],
    )

    out = {}

    df = df.sort_values(["Patrol", "Name", "Level", "Theme", "Requirement"])

    for patrol in df.groupby("Patrol", observed=True).groups:
        out[patrol] = {}

        for person in df[df["Patrol"] == patrol].groupby("Name").groups:
            out[patrol][person] = {
                "Level": df[(df["Patrol"] == patrol) & (df["Name"] == person)].iloc[0][
                    "Level"
                ],
                "tasks": [],
            }

            for row in df[(df["Patrol"] == patrol) & (df["Name"] == person)].iterrows():
                theme = row[1]["Theme"]
                if theme == "":
                    theme = "Membership"
                out[patrol][person]["tasks"].append(
                    (theme, row[1]["Requirement"].replace("&", "\\&"))
                )
    return out
