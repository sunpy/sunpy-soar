"""
``sunpy-soar``
==============

A sunpy FIDO plugin for accessing data in the Solar Orbiter Archive (SOAR).
"""

from sunpy_soar.client import SOARClient

from .version import version as __version__

__all__ = ["SOARClient", "__version__"]
