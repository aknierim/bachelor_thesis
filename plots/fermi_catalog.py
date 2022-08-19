import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from astropy.table import Table
from astropy.coordinates import SkyCoord

from collections import Counter

from thesis_scripts.custom_cmap import custom_cmap


cmap = custom_cmap(['#1a2bad', "#32a852", "#fffc5e", "#f7d200"])

# not used, but nice to have for lookups etc
"""
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
"""

fits_image_filename = './plots/data/fermi_4fgl_dr3.fit'
table = Table.read(fits_image_filename, hdu=1)

table.sort('Flux1000')
coords = SkyCoord(table['GLON'], table['GLAT'], frame='galactic')

# # just to get all unique extended source names
# for idx, item in enumerate(table["Extended_Source_Name"]):
#     if not item == 18*" ":
#         print(f"{idx}: {item}")

agn = []
snr = []
pwn = []
psr = []
grb = []

# classes = []

# for item in table["CLASS1"]:
#     if item != 5*" ":
#         classes.append(item)

# print(Counter(classes).keys())
# print(Counter(classes).values())

# agn_classes = ["agn", "bcu", "bll", "css", "fsrq", "nlsy1", "sey", "ssrq"
#                "AGN", "BCU", "BLL", "CSS", "FSRQ", "NLSY1", "SEY", "SSRQ"]

agn_classes = ["agn", "AGN"]

for idx, item in enumerate(table["CLASS2"]):
    if item.strip() in agn_classes:
        agn.append(idx)

for idx, item in enumerate(table["CLASS1"]):
    if "snr" in item:
        snr.append(idx)
    if "SNR" in item:
        snr.append(idx)

for idx, item in enumerate(table["CLASS1"]):
    if "pwn" in item:
        pwn.append(idx)
    if "PWN" in item:
        pwn.append(idx)

for idx, item in enumerate(table["CLASS1"]):
    if "psr" in item:
        psr.append(idx)
    if "PSR" in item:
        psr.append(idx)

for idx, item in enumerate(table["CLASS1"]):
    if "grb" in item:
        grb.append(idx)
    if "GRB" in item:
        grb.append(idx)




x_coord = -coords.galactic.l.wrap_at('180 deg').rad
y_coord = coords.galactic.b.rad

colors = table['Energy_Flux100'].to('TeV/(cm2 s)')


fig, ax = plt.subplots(1, 1, figsize=(8,4.5), subplot_kw=dict(projection='mollweide'), constrained_layout=True)

sc = ax.scatter(x_coord, y_coord, c=colors, cmap="inferno", norm=LogNorm(), alpha=0.9, s=8, edgecolors='none')
ax.scatter(x_coord[6630], y_coord[6630], marker='o', s=20, facecolors='none', edgecolors='#fc0000', label='Crab Nebula') #'#fc0000'
ax.scatter(x_coord[agn], y_coord[agn], marker='o', s=20, facecolors='none', edgecolors='#2ab5fa', label='AGN')
ax.scatter(x_coord[snr], y_coord[snr], marker='o', s=20, facecolors='none', edgecolors='#32a852', label='SNR')
# ax.scatter(x_coord[grb], y_coord[grb], marker='o', s=20, facecolors='none', edgecolors='#fc0000', label='GRB')
# ax.scatter(x_coord[pwn], y_coord[pwn], marker='o', s=20, facecolors='none', edgecolors='#2ab5fa', label='PWN')
# ax.scatter(x_coord[psr], y_coord[psr], marker='o', s=20, facecolors='none', edgecolors='#2ab5fa', label='Pulsar')

ax.set_facecolor('black')

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(False)
ax.legend()
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.025), ncol=3)

ax.set_title('LAT 12-year Source Catalog (4FGL-DR3)')

cbar = fig.colorbar(sc, ax=ax, pad=0.1, fraction=0.025, label='Flux / \si{\TeV\per\square\centi\meter \per\second}')

plt.savefig('./build/fermi_catalog.pdf', dpi=300, bbox_inches='tight')
