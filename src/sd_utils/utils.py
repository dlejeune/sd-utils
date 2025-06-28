import numpy as np
import pandas as pd


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

    df[["Temp", "DatePassed", "Scouter"]] = df["Passed"].str.split("\n", 2, expand=True)
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
        "\n", 2, expand=True
    )

    df["Theme"] = df["Theme"].str.replace(" \(", "", regex=True)
    df["Theme"] = df["Theme"].str.replace("\)", "", regex=True)

    df[["Level", "Theme", "Patrol"]] = df[["Level", "Theme", "Patrol"]].astype(
        "category"
    )

    df["Level"] = df["Level"].cat.reorder_categories(
        ["Membership", "Traveller", "Discoverer", "1st Class", "Springbok"]
    )

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
