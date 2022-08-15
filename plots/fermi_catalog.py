import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from astropy.table import Table
from astropy.coordinates import SkyCoord
# from astropy.io import fits


# fits_image_filename = './plots/data/fermi_4fgl.fit'

# with fits.open(fits_image_filename) as hdul:
#     print(hdul.info())

table = Table.read('./plots/data/fermi_4fgl.fit', hdu=1)

table.sort('Flux1000')
coords = SkyCoord(table['GLON'], table['GLAT'], frame='galactic')

x_coord = coords.galactic.l.wrap_at('180 deg').rad
y_coord = coords.galactic.b.rad

colors = table['Energy_Flux100'].to('TeV/(cm2 s)')

fig, ax = plt.subplots(1, 1, figsize=(8,4.5), subplot_kw=dict(projection='mollweide'), constrained_layout=True)
sc = ax.scatter(x_coord, y_coord, c=colors, cmap='inferno', norm=LogNorm(), alpha=0.9, s=12, edgecolors='none')

ax.set_facecolor('black')

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(False)

ax.set_title('LAT 10-year Source Catalog (4FGL-DR2)')

cbar = fig.colorbar(sc, ax=ax, pad=0.1, fraction=0.025, label='Flux / \si{\TeV\per\square\centi\meter \per\second}')

plt.savefig('./build/fermi_catalog.pdf', dpi=300, bbox_inches='tight')