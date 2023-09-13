# Import here to register the client with sunpy
from sunpy_soar.attrs import SOOP, Product
from sunpy_soar.client import SOARClient

from .version import version as __version__

__all__ = ["__version__", "SOARClient", "Product", "SOOP"]
