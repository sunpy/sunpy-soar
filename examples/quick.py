"""
============================================
Quick overview of using sunpy-soar with Fido
============================================

This example demonstrates how to search and download Solar Orbiter data using ``sunpy.net.Fido``.
"""

import sunpy.net.attrs as a
from sunpy.net import Fido

#####################################################
# Importing sunpy_soar registers the client with sunpy
import sunpy_soar  # NOQA: F401

#####################################################
# We shall start with constructing a search query.

instrument = a.Instrument("METIS")
level = a.Level(2)
product = a.soar.Product("metis-vl-pol-angle")
distance = a.soar.Distance(0.45, 0.55)
res = Fido.search(distance & instrument & product & level)
print(res)

#####################################################
# Finally we can download the data.
#
# For this example, we will comment out the download part
# as we want to avoid downloading data in the documentation build

# files = Fido.fetch(result)
# print(files)
