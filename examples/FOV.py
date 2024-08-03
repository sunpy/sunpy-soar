"""
========================================
Retrieve and Plot Field of View on a map
========================================

This example demonstrates how to fetch Solar Orbiter's Field of View (FOV) for each instrument values and Solar Orbiter data using `sunpy.net.Fido` and plot them on a `sunpy.map.Map`.
"""

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import sunpy.map
import sunpy.net.attrs as a
from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames
from sunpy.net import Fido

#####################################################
# Importing sunpy_soar registers the client with sunpy
import sunpy_soar  # NOQA: F401

#####################################################
# We shall start with constructing a search query.

instrument = a.Instrument("EUI")
time = a.Time("2022-10-13 12:06:00", "2022-10-13 12:06:10")
level = a.Level(2)
detector = a.Detector("HRI_EUV")
product = a.soar.Product("eui-hrieuv174-image")
fov = a.soar.FOV("earth")

#####################################################
# Now we will do the search.

result = Fido.search(instrument & time & level & detector & product & fov)

#####################################################
# To plot the FOV, we need a map to overlay them on to.
# For this we will create a blank map as the base.

data = np.full((10, 10), np.nan)
skycoord = SkyCoord(0 * u.arcsec, 0 * u.arcsec, obstime="2013-10-28", observer="earth", frame=frames.Helioprojective)
header = sunpy.map.make_fitswcs_header(data, skycoord, scale=[220, 220] * u.arcsec / u.pixel)
blank_map = sunpy.map.Map(data, header)

#####################################################
# Now we need to  extract the FOV coordinates from search results.

fov_earth_bot_left_tx = result[0]["fov_earth_left_arcsec_tx"][0] * u.arcsec
fov_earth_bot_left_ty = result[0]["fov_earth_left_arcsec_ty"][0] * u.arcsec
fov_earth_top_right_tx = result[0]["fov_earth_right_arcsec_tx"][0] * u.arcsec
fov_earth_top_right_ty = result[0]["fov_earth_right_arcsec_ty"][0] * u.arcsec

#####################################################
# To plot the corners of the corners of the FOVs, we need turn them into a `~astropy.coordinates.SkyCoord`. 

earth_fov_corners = SkyCoord(
    [
        fov_earth_bot_left_tx,
        fov_earth_top_right_tx,
        fov_earth_top_right_tx,
        fov_earth_bot_left_tx,
        fov_earth_bot_left_tx,
    ],
    [
        fov_earth_bot_left_ty,
        fov_earth_bot_left_ty,
        fov_earth_top_right_ty,
        fov_earth_top_right_ty,
        fov_earth_bot_left_ty,
    ],
    frame=blank_map.coordinate_frame,
)

#####################################################
# Finally we will plot the blank map and overlay the FOV from Solar Orbiter.

fig = plt.figure()
ax = fig.add_subplot(projection=blank_map)
blank_map.plot(axes=ax)
blank_map.draw_limb(axes=ax, color="k")
blank_map.draw_grid(axes=ax, color="k")

# Plot the FOVs
ax.plot_coord(earth_fov_corners, color="blue", linestyle="-", label="Earth FOV")

# Mark the corners
ax.plot_coord(earth_fov_corners, "bo")

# Set title and show legend
ax.set_title("Fields of View on Blank Map")
ax.legend()

plt.show()
