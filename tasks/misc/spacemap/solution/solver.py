#!/usr/bin/env python3

import pandas
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np
import matplotlib.pyplot as plt

coords = []
ra = []
dec = []
ngc = pandas.read_csv('NGC.csv', sep=';')

file = open("flag.txt", "r")


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
ax.set_theta_zero_location('S') # East by default
ax.set_xticklabels(['$0^h$', '$1^h$', '$2^h$', '$3^h$', '$4^h$', '$5^h$', '$6^h$', '$7^h$', '$8^h$', '$9^h$', '$10^h$',
                    '$11^h$', '$12^h$', '$13^h$', '$14^h$', '$15^h$', '$16^h$', '$17^h$', '$18^h$', '$19^h$', '$20^h$',
                    '$21^h$', '$22^h$', '$23^h$'], fontsize=10)



previous_point = None

for line in file.readlines():

  if len(line) != 1 and line.replace("\n", "") in ngc.Name.values:
    row = ngc.loc[ngc['Name'] == line.replace("\n", "")]
    c = SkyCoord(row['RA'], row['Dec'], unit=(u.hourangle, u.deg))
    curr_point = (c.ra.degree / 180.0 * 3.141593, c.dec.degree)

    if previous_point is not None:
      ax.plot([previous_point[0], curr_point[0]], [previous_point[1], curr_point[1]], color="red")

    previous_point = curr_point
  else:
    previous_point = None


# Output png file.
fig.tight_layout()
plt.savefig('solution.png', dpi=300)


# plt.show()
