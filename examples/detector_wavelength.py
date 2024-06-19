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
# For instruments EUI, METIS and SOLOHI we get query results in form of wavelength.
#
# When a single wavelength is provided it is interpreted as the wavelength value.

instrument = a.Instrument("METIS")
time = a.Time("2023-02-01 01:00", "2023-02-01 05:00")
level = a.Level(2)
detector = a.Detector("UVD")
wavelength = a.Wavelength(121.6 * u.AA)
#####################################################
# Now do the search.

result = Fido.search(instrument & time & level & detector & wavelength)
result

#####################################################
# When a range of wavelength is provided, it is interpreted as the wavemin and wavemax.

detector = a.Detector("VLD")
wavelength = a.Wavelength(580 * u.AA, 640 * u.AA)
result = Fido.search(instrument & time & level & detector & wavelength)
result
#####################################################
# For instruments PHI and SPICE, we get query results in form of wavemin and wavemax.
#
# When two values are provided, it is interpreted as the wavemin and wavemax.

instrument = a.Instrument("SPICE")
time = a.Time("2023-02-01 2:00", "2023-02-01 2:30")
level = a.Level(2)
detector = a.Detector("SW")
wavelength = a.Wavelength(69.523026 * u.AA, 79.508766 * u.AA)
#####################################################
# Now do the search.

result = Fido.search(instrument & time & level & wavelength & detector)
result
#####################################################
# When a single value given for wavelength is interpreted as the wavemin.


wavelength = a.Wavelength(69.523026 * u.AA)
result = Fido.search(instrument & time & level & wavelength & detector)
result

#####################################################
# Finally we can download the data.
#
# For this example, we will comment out the download part
# as we want to avoid downloading data in the documentation build

# files = Fido.fetch(result)
# print(files)