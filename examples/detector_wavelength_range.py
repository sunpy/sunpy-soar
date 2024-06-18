"""
=======================================================
Searching SOAR data with Wavelength(Range) and Detector
=======================================================

This example demonstrates how to search and download Solar Orbiter data using ``sunpy.net.Fido``.
"""

import astropy.units as u
import sunpy.net.attrs as a
from sunpy.net import Fido

#####################################################
# Importing sunpy_soar registers the client with sunpy
import sunpy_soar  # NOQA: F401

#####################################################
# We shall start with constructing a search query involving wavelength and detector.
# For instruments PHI and SPICE, we get query results in inform of wavemin and wavemax.
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
