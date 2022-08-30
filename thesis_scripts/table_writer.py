import pandas as pd
import numpy as np

tables = [
    "efficiency",
    "angular_resolution",
    "metrics_tail",
    "metrics_mars",
    "metrics_fact",
    "metrics_tcc",
]

def build_dataset_table(df):

    table = ""
    for n, series in df.iterrows():
        v = [str(s) for s in series.values]
        s = " & ".join(v) + r" \\ "
        table += s

    return table


def combined_table(tab_name: str) -> str:
    combined_table = pd.read_csv("./plots/data/combined_table.csv")
    # combined_table = combined_table.dropna()

    table = combined_table[
        [f"{tab_name}_tail", f"{tab_name}_mars" , f"{tab_name}_fact", f"{tab_name}_tcc"]
    ]

    first_valid_index = table.first_valid_index()
    last_valid_index = table.last_valid_index()
    table = table.loc[first_valid_index:last_valid_index]

    table = table.astype(float).applymap('{:,.3f}'.format)
    table = table.replace("nan", '', regex=True)

    table.insert(0, "n_lower", combined_table["n_lower"])
    table.insert(1, "n_upper", table["n_lower"] + 0.05)

    table[["n_lower", "n_upper"]] = table[["n_lower", "n_upper"]].astype(float).applymap('{:,.2f}'.format)

    table_out = build_dataset_table(table)

    return table_out


def metrics_table(tab_name):
    cleaner = tab_name.split("_")[1]
    if cleaner == "tail":
        cleaner = "tailcuts"

    table = pd.read_csv(f"./plots/data/metrics/metrics_{cleaner}_MST_MST_NectarCam.csv")
    ids = table["unique_file_id"]

    table = table.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn"])
    table = table.astype(float).applymap('{:,.4f}'.format)
    table.insert(loc=0, column="unique_file_id", value=ids)

    table_out = build_dataset_table(table)

    return table_out



if __name__ == "__main__":

    for name in tables:
        outfile = f'build/{name}.txt'

        if name == "efficiency":
            table_out = combined_table("ratio")

        elif name == "angular_resolution":
            table_out = combined_table("angres")

        elif "metrics" in name:
            table_out = metrics_table(name)

        with open(outfile, "w") as f:
            f.write(table_out)