"""
================================================
Searching SOAR data with Wavelength and Detector
================================================

This example demonstrates how to search and download Solar Orbiter data using ``sunpy.net.Fido``.
"""

import sunpy.net.attrs as a
from sunpy.net import Fido
import astropy.units as u

#####################################################
# Importing sunpy_soar registers the client with sunpy
import sunpy_soar  # NOQA: F401

#####################################################
# We shall start with constructing a search query with wavelength and detector.
# For instruments EUI, METIS and SOLOHI we get query results in form of wavelength.
#
# When a single wavelength is provided it is interpreted as the wavelength value.

instrument = a.Instrument("METIS")
time = a.Time("2023-02-01 01:00", "2023-02-01 05:00")
level = a.Level(2)
detector=a.Detector("UVD")
wavelength=a.Wavelength(121.6*u.AA)
#####################################################
# Now do the search.

result = Fido.search(instrument & time & level & detector & wavelength)
result

#####################################################
# When a range of wavelength is provided, it is interpreted as the wavemin and wavemax.

detector=a.Detector("VLD")
wavelength=a.Wavelength(580*u.AA, 640*u.AA)
result = Fido.search(instrument & time & level & detector & wavelength)
result
#####################################################
# Finally we can download the data.
#
# For this example, we will comment out the download part
# as we want to avoid downloading data in the documentation build

# files = Fido.fetch(result)
# print(files)