import warnings

import astropy.units as u
import sunpy.net.attrs as a
from sunpy.net.attr import AttrAnd, AttrOr, AttrWalker, DataAttr, Range, SimpleAttr
from sunpy.util.exceptions import SunpyUserWarning
from astropy.utils.decorators import quantity_input

__all__ = ["Product", "SOOP"]


class Product(SimpleAttr):
    """
    The data product descriptor to search for.

    Makes the value passed lower so that it is case insensitive as all
    descriptors on the SOAR are now lowercase.
    """

    def __init__(self, value):
        self.value = value.lower()


class SOOP(SimpleAttr):
    """
    The SOOP name to search for.
    """

@quantity_input(dist_min=u.m, dist_max=u.m)
class Distance(Range):
    type_name = "distance"

    def __init__(self, dist_min, dist_max=None):
        """
        Specifies the distance range.

        Parameters
        ----------
        dist_min : `~astropy.units.Quantity`
            The lower bound of the range.
        dist_max : `~astropy.units.Quantity`, optional
            The upper bound of the range, if not specified it will default to
            the lower bound.

        Notes
        -----
        The valid units for distance are AU, km, and mm. Any unit directly
        convertible to these units is valid input. This class filters the query
        by solar distance without relying on a specific distance column.
        """
        if dist_max is None:
            dist_max = dist_min

        # Ensure both dist_min and dist_max are astropy Quantity instances
        if not all(isinstance(var, u.Quantity) for var in [dist_min, dist_max]):
            msg = "Distance inputs must be astropy Quantities"
            raise TypeError(msg)

        # Ensure both dist_min and dist_max are scalar values
        if not all([dist_min.isscalar, dist_max.isscalar]):
            msg = "Both dist_min and dist_max must be scalar values"
            raise ValueError(msg)

        # Supported units for distance
        supported_units = [u.AU, u.km, u.mm]
        for unit in supported_units:
            if dist_min.unit.is_equivalent(unit):
                break
        else:
            msg = f"This unit is not convertible to any of {supported_units}"
            raise u.UnitsError(msg)

        # Convert to the chosen unit and sort the values
        dist_min, dist_max = sorted([dist_min.to(unit), dist_max.to(unit)])
        self.unit = unit

        # Initialize the parent class with the sorted distances
        super().__init__(dist_min, dist_max)

    def collides(self, other):
        return isinstance(other, self.__class__)


walker = AttrWalker()


@walker.add_creator(AttrOr)
def create_or(wlk, tree):
    """
    Creator for OR.

    Loops through the next level down in the tree and appends the
    individual results to a list.
    """
    return [wlk.create(sub) for sub in tree.attrs]


@walker.add_creator(AttrAnd, DataAttr)
def create_and(wlk, tree):
    """
    Creator for And and other simple attributes.

    No walking needs to be done, so simply call the applier function.
    """
    result = []
    wlk.apply(tree, result)
    return [result]


@walker.add_applier(AttrAnd)
def apply_and(wlk, and_attr, params):
    """
    Applier for And.

    Parameters
    ----------
    wlk : AttrWalker
    and_attr : AttrAnd
        The AND attribute being applied. The individual attributes being
        AND'ed together are accessible with ``and_attr.attrs``.
    params : list[str]
        List of search parameters.
    """
    for iattr in and_attr.attrs:
        wlk.apply(iattr, params)


"""
Below are appliers for individual attributes.

The all convert the attribute object into a query string, that will eventually
be passed as a query to the SOAR server. They all have the signature:

Parameters
----------
wlk : AttrWalker
    The attribute walker.
attr :
    The attribute being applied.
params : list[str]
    List of search parameters.
"""


@walker.add_applier(a.Time)
def _(wlk, attr, params):  # NOQA: ARG001
    start = attr.start.strftime("%Y-%m-%d+%H:%M:%S")
    end = attr.end.strftime("%Y-%m-%d+%H:%M:%S")
    params.append(f"begin_time>='{start}'+AND+begin_time<='{end}'")


@walker.add_applier(a.Level)
def _(wlk, attr, params):  # NOQA: ARG001
    level = attr.value
    if isinstance(level, int):
        level = f"L{level}"

    level = level.upper()
    allowed_levels = ("L0", "L1", "L2", "L3", "LL01", "LL02", "LL03")
    if level not in allowed_levels:
        warnings.warn(
            f"level not in list of allowed levels for SOAR: {allowed_levels}",
            SunpyUserWarning,
            stacklevel=2,
        )

    params.append(f"level='{level}'")


@walker.add_applier(a.Instrument)
def _(wlk, attr, params):  # NOQA: ARG001
    params.append(f"instrument='{attr.value}'")


@walker.add_applier(Product)
def _(wlk, attr, params):  # NOQA: ARG001
    params.append(f"descriptor='{attr.value}'")


@walker.add_applier(a.Provider)
def _(wlk, attr, params):  # NOQA: ARG001
    params.append(f"provider='{attr.value}'")


@walker.add_applier(SOOP)
def _(wlk, attr, params):  # NOQA: ARG001
    params.append(f"soop_name='{attr.value}'")


@walker.add_applier(a.Detector)
def _(wlk, attr, params):  # NOQA: ARG001
    params.append(f"Detector='{attr.value}'")


@walker.add_applier(a.Wavelength)
def _(wlk, attr, params):  # NOQA: ARG001
    wavemin = attr.min.value
    wavemax = attr.max.value
    params.append(f"Wavemin='{wavemin}'+AND+Wavemax='{wavemax}'")


@walker.add_applier(Distance)
def _(wlk, attr, params):  # NOQA: ARG001
    # The `Distance` attribute is used to filter the query by solar distance
    # without relying on a specific distance column. It is commonly used
    # to filter the query without time consideration.
    dmin = attr.min.value
    dmax = attr.max.value
    params.append(f"DISTANCE({dmin},{dmax})")
    if not (0.28 <= dmin <= 1.0) or not (0.28 <= dmax <= 1.0):
        warnings.warn(
            "Distance values must be within the range 0.28 AU to 1.0 AU.",
            SunpyUserWarning,
            stacklevel=2,
        )
    params.append(f"DISTANCE({dmin},{dmax})")
