import pandas
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pandas.read_csv('NGC.csv', sep=';')
# print(df)


coords = []
ra = []
dec = []

for index, row in df.iterrows():
    c = SkyCoord(row['RA'], row['Dec'], unit=(u.hourangle, u.deg))
    ca = [row['Name'], c.ra.degree, c.dec.degree]
    ra.append(c.ra.degree)
    dec.append(c.dec.degree)
    coords.append(ca)

# Convert RA from decimal degrees to radians.
ra = [x / 180.0 * 3.141593 for x in ra]

# Make plot.
fig = plt.figure(figsize=(20, 20))
ax = plt.axes(polar=True)
# Position plot in figure using gridspec.
# ax = plt.subplot(gs[0], polar=True)

# lims = [-90, 0]
lims = [0, 90]
ax.set_ylim(lims[0], lims[1])
ax.invert_yaxis()

# Set x,y ticks
# angs = np.array([0., 15., 30., 45., 60., 75., 90., 105., 120., 135., 150., 165., 180., 195., 330., 345.])
angs = np.arange(0., 360., 15.)
plt.xticks(angs * np.pi / 180., fontsize=6)
plt.yticks(np.arange(lims[0], lims[1], 10), fontsize=6)
ax.set_rlabel_position(120)
ax.set_xticklabels(['$0^h$', '$1^h$', '$2^h$', '$3^h$', '$4^h$', '$5^h$', '$6^h$', '$7^h$', '$8^h$', '$9^h$', '$10^h$',
                    '$11^h$', '$12^h$', '$13^h$', '$14^h$', '$15^h$', '$16^h$', '$17^h$', '$18^h$', '$19^h$', '$20^h$',
                    '$21^h$', '$22^h$', '$23^h$'], fontsize=10)
# ax.set_yticklabels(['$-80^{\circ}$', '$-70^{\circ}$', '$-60^{\circ}$'],
#     fontsize=10)

# Plot points.
ax.scatter(ra, dec, marker='o', c='k', s=1, lw=0.)

# Output png file.
fig.tight_layout()
plt.savefig('ra_dec_plot.png', dpi=300)
# plt.show()


