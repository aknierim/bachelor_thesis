import pandas as pd

tables = [
    "efficiency",
    "angular_resolution"
]

def build_dataset_table(df):

    table = ""
    for n, series in df.iterrows():
        v = [str(s) for s in series.values]
        s = " & ".join(v) + "\\\\ "
        table += s

    return table[:-3]


def combined_table(tab_name: str) -> str:
    combined_table = pd.read_csv("./plots/data/combined_table.csv")
    combined_table = combined_table.dropna()

    table = combined_table[
        [f"{tab_name}_tail", f"{tab_name}_mars" , f"{tab_name}_fact", f"{tab_name}_tcc"]
    ].astype(float).applymap('{:,.3f}'.format)

    table.insert(0, "n_lower", combined_table["n_lower"])
    table.insert(1, "n_upper", table["n_lower"] + 0.05)

    table[["n_lower", "n_upper"]] = table[["n_lower", "n_upper"]].astype(float).applymap('{:,.2f}'.format)

    table_out = build_dataset_table(table)

    return table_out



if __name__ == "__main__":

    for name in tables:
        outfile = f'build/{name}.txt'

        if name == "efficiency":
            table_out = combined_table("ratio")
        if name == "angular_resolution":
            table_out = combined_table("angres")

        with open(outfile, "w") as f:
            f.write(table_out)