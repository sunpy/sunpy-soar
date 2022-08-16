from pkg_resources import get_distribution

__version__ = get_distribution(__name__).version


# Import here to register the client with sunpy
from sunpy_soar.attrs import *
from sunpy_soar.client import *
