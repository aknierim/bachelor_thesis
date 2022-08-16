from enum import unique
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from astropy.table import unique, Table
from astropy.coordinates import SkyCoord
from astropy.io import fits

import itertools
markers = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X', ))

source_classes = {
    "agn": "AGN",
    "bcu": "AGN of uncertain type",
    "bin": "Binary",
    "bll": "BL Lac",
    "css": "Compact Steep Spectrum quasar",
    "fsrq": "FSRQ",
    "gal": "Galaxy",
    "glc": "Globular Cluster",
    "hmb": "High-mass Binary",
    "mc": "Molecular Cloud",
    "nlsy1": "Narrow Line Seyfert 1",
    "nov": "Nova",
    "PSR": "Pulsar",
    "psr": "Pulsar, no pulsations seen in LAT yet",
    "pwn": "Pulsar Wind Nebula",
    "rdg": "Radio Galaxy",
    "sbg": "Starburst Galaxy",
    "sey": "Seyfert Galaxy",
    "sfr": "Star-forming Region",
    "snr": "SNR",
    "spp": "Potential association with SNR or PWN",
    "ssrq": "Soft-spectrum Radio Quasar",
    "unk": "Unknown"
}


fits_image_filename = './plots/data/fermi_4fgl_dr3.fit'

table = Table.read(fits_image_filename, hdu=1)


# col = "CLASS1"
# grouped = table.group_by(col)

# fig, ax = plt.subplots(1, 1, figsize=(8,4.5), subplot_kw=dict(projection='mollweide'), constrained_layout=True)

# for idx, key in enumerate(grouped.groups.keys[1:18]):
#     # print(key, grouped.groups[idx])

#     tab = grouped.groups[idx]
#     tab.sort('Flux1000')

#     coords = SkyCoord(tab["GLON"], tab["GLAT"], frame="galactic")

#     x_coord = coords.galactic.l.wrap_at('180 deg').rad
#     y_coord = coords.galactic.b.rad

#     colors = grouped.groups[idx]

#     ax.scatter(x_coord, y_coord, marker=next(markers), label=key, c=colors, cmap='inferno', norm=LogNorm(), alpha=0.9, s=12, edgecolors='none')

# # cbar = fig.colorbar(sc, ax=ax, pad=0.1, fraction=0.025, label='Flux / \si{\TeV\per\square\centi\meter \per\second}')
# ax.set_facecolor('black')
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
#           fancybox=True, shadow=True, ncol=5)

# plt.savefig('./build/fermi_test.pdf', dpi=300, bbox_inches='tight')

# grouped = grouped[grouped.groups == 0]
# print(table.colnames)
# unique = unique(table[["DataRelease", "Extended_Source_Name"]], "Extended_Source_Name")
# print(unique)
# print(table["Extended_Source_Name"][table["Extended_Source_Name"] == "Crab IC"])
# crab = table[table["Extended_Source_Name"] == "gal"]


table.sort('Flux1000')
coords = SkyCoord(table['GLON'], table['GLAT'], frame='galactic')

x_coord = coords.galactic.l.wrap_at('180 deg').rad
y_coord = coords.galactic.b.rad

colors = table['Energy_Flux100'].to('TeV/(cm2 s)')

fig, ax = plt.subplots(1, 1, figsize=(8,4.5), subplot_kw=dict(projection='mollweide'), constrained_layout=True)
sc = ax.scatter(x_coord, y_coord, c=colors, cmap='inferno', norm=LogNorm(), alpha=0.9, s=8, edgecolors='none')

ax.set_facecolor('black')

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(False)

ax.set_title('LAT 12-year Source Catalog (4FGL-DR3)')

cbar = fig.colorbar(sc, ax=ax, pad=0.1, fraction=0.025, label='Flux / \si{\TeV\per\square\centi\meter \per\second}')

plt.savefig('./build/fermi_catalog.pdf', dpi=300, bbox_inches='tight')
