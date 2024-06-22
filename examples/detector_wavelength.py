"""
================================================
Searching SOAR data with Wavelength and Detector
================================================

This example demonstrates how to search and download Solar Orbiter data using ``sunpy.net.Fido``.
"""

import astropy.units as u
import sunpy.net.attrs as a
from sunpy.net import Fido

#####################################################
# Importing sunpy_soar registers the client with sunpy

import sunpy_soar  # NOQA: F401

#####################################################
# We shall start with constructing a search query with wavelength and detector.

instrument = a.Instrument("METIS")
time = a.Time("2023-02-01 01:00", "2023-02-01 05:00")
level = a.Level(2)
detector = a.Detector("UVD")
wavelength = a.Wavelength(121.6 * u.AA)

#####################################################
# Now do the search.

result = Fido.search(instrument & time & level & detector & wavelength)
print(result)

