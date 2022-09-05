import matplotlib.pyplot as plt
import pandas as pd

df_angres = pd.read_csv('plots/data/combined_table.csv')

# df_angres = df_angres.iloc[4:9]

size = plt.gcf().get_size_inches()
fig, ax = plt.subplots(1,1, figsize=(size[0], size[1]), constrained_layout=True, dpi=300)

ax.plot(df_angres["ratio_tail"].dropna(), df_angres["angres_tail"].dropna(), "x:", label="Tailcuts")
ax.plot(df_angres["ratio_mars"].dropna(), df_angres["angres_mars"].dropna(), "o:", label="MARS")
ax.plot(df_angres["ratio_fact"].dropna(), df_angres["angres_fact"].dropna(), "^:", label="FACT")
ax.plot(df_angres["ratio_tcc"].dropna(), df_angres["angres_tcc"].dropna(), "v:", label="TCC")

# axins = ax.inset_axes([0.33, 0.40, 0.5, 0.5])
# axins.plot(df_angres["ratio_tail"].dropna(), df_angres["angres_tail"].dropna(), "x:", label="Tailcuts")
# axins.plot(df_angres["ratio_mars"].dropna(), df_angres["angres_mars"].dropna(), "o:", label="MARS")
# axins.plot(df_angres["ratio_fact"].dropna(), df_angres["angres_fact"].dropna(), "^:", label="FACT")
# axins.plot(df_angres["ratio_tcc"].dropna(), df_angres["angres_tcc"].dropna(), "v:", label="TCC")

# x1, x2, y1, y2 = 0.2, 0.48, 0.2, 0.5
# axins.set_xlim(x1, x2)
# axins.set_ylim(y1, y2)

# ax.indicate_inset_zoom(axins)

ax.grid(ls="dotted")

ax.set_xlabel(r"Efficiency $n_\mathrm{reco} \; / \; n_\mathrm{total}$")
ax.set_ylabel(r"Mean Angular Resolution$\,\, / \,\, \mathrm{deg}$")

ax.legend()

plt.savefig("build/ar_vs_eff.pdf")