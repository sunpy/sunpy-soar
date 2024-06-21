.. _sunpy-soar-how-to-query-wavelength:

*************************************
How to query using Wavelength in SOAR
*************************************

``sunpy-soar`` provides a convenient methods to query Wavelength for all different instruments available in SOAR.
In this guide, we will demonstrate how we can query for Wavelength for different instruments.
For instruments EUI, METIS and SOLOHI we get query results in form of wavelength,
for instrument PHI we get query results in form of wavemin and wavemax and
for instruments SPICE and STIX we do not get any meaningful data for wavelength.

For instruments EUI, METIS and SOLOHI passing a single Wavelength
=================================================================

When a single wavelength is provided it is interpreted as the wavelength.

.. code-block:: python


    >>> import astropy.units as u
    >>> import sunpy.net.attrs as a
    >>> from sunpy.net import Fido
    >>> import sunpy_soar

    >>> instrument = a.Instrument("METIS")
    >>> time = a.Time("2023-02-01 01:00", "2023-02-01 05:00")
    >>> level = a.Level(2)
    >>> wavelength = a.Wavelength(121.6 * u.AA)
    >>> result = Fido.search(instrument & time & level & wavelength) # doctest: +REMOTE_DATA
    >>> result  # doctest: +REMOTE_DATA
    Results from 1 Provider:
    <BLANKLINE>
    8 Results from the SOARClient:
    <BLANKLINE>
    Instrument  Data product  Level        Start time               End time        Filesize SOOP Name Detector Wavelength
                                                                                    Mbyte
    ---------- -------------- ----- ----------------------- ----------------------- -------- --------- -------- ----------
        METIS metis-uv-image    L2 2023-02-01 01:00:48.690 2023-02-01 01:11:46.866     0.85      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 01:30:48.680 2023-02-01 01:41:45.540     0.85      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 02:00:48.671 2023-02-01 02:11:44.213    12.64      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 02:30:48.661 2023-02-01 02:41:42.887    12.64      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 03:00:48.652 2023-02-01 03:11:41.560    12.64      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 03:30:48.643 2023-02-01 03:41:40.233    12.64      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 04:00:48.633 2023-02-01 04:11:38.907    12.64      none      UVD      121.6
        METIS metis-uv-image    L2 2023-02-01 04:30:38.163 2023-02-01 04:40:37.625    12.64      none      UVD      121.6
    <BLANKLINE>
    <BLANKLINE>

For instruments EUI, METIS and SOLOHI passing a range of Wavelength
===================================================================

When a range of wavelength is provided, it is interpreted as the wavemin and wavemax.

.. code-block:: python


    >>> wavelength = a.Wavelength(580 * u.AA, 640 * u.AA)
    >>> result = Fido.search(instrument & time & level & wavelength) # doctest: +REMOTE_DATA
    >>> result  # doctest: +REMOTE_DATA
    Results from 1 Provider:
    <BLANKLINE>
    64 Results from the SOARClient:
    <BLANKLINE>
    Instrument    Data product    Level        Start time               End time        Filesize SOOP Name Detector Wavelength
                                                                                        Mbyte
    ---------- ------------------ ----- ----------------------- ----------------------- -------- --------- -------- ----------
        METIS        metis-vl-tb    L2 2023-02-01 01:00:00.147 2023-02-01 01:24:37.923    12.64      none      VLD      610.0
        METIS    metis-vl-stokes    L2 2023-02-01 01:00:00.147 2023-02-01 01:24:37.923   21.067      none      VLD      610.0
        METIS        metis-vl-pb    L2 2023-02-01 01:00:00.147 2023-02-01 01:24:37.923    12.64      none      VLD      610.0
        METIS     metis-vl-image    L2 2023-02-01 01:00:00.147 2023-02-01 01:23:05.525   12.643      none      VLD      610.0
        METIS metis-vl-pol-angle    L2 2023-02-01 01:00:00.147 2023-02-01 01:24:37.923    12.64      none      VLD      610.0
        ...                ...   ...                     ...                     ...      ...       ...      ...        ...
        METIS        metis-vl-tb    L2 2023-02-01 04:30:00.201 2023-02-01 04:54:37.981   50.388      none      VLD      610.0
        METIS        metis-vl-pb    L2 2023-02-01 04:30:00.201 2023-02-01 04:54:37.981   50.388      none      VLD      610.0
        METIS     metis-vl-image    L2 2023-02-01 04:30:00.201 2023-02-01 04:53:05.585   50.388      none      VLD      610.0
        METIS     metis-vl-image    L2 2023-02-01 04:30:30.999 2023-02-01 04:53:36.383   50.388      none      VLD      610.0
        METIS     metis-vl-image    L2 2023-02-01 04:31:01.796 2023-02-01 04:54:07.184   50.388      none      VLD      610.0
        METIS     metis-vl-image    L2 2023-02-01 04:31:32.593 2023-02-01 04:54:37.979   50.388      none      VLD      610.0
    Length = 64 rows
    <BLANKLINE>
    <BLANKLINE>

For instrument PHI passing a range of Wavelength
================================================

When a range of wavelength is provided, it is interpreted as the wavemin and wavemax.

.. code-block:: python


    >>> instrument = a.Instrument("PHI")
    >>> time = a.Time("2023-02-01", "2023-02-02")
    >>> level = a.Level(2)
    >>> wavelength=a.Wavelength(6173.065*u.AA, 6173.501*u.AA)
    >>> result = Fido.search(instrument & time & level) # doctest: +REMOTE_DATA
    >>> result  # doctest: +REMOTE_DATA
    Results from 1 Provider:
    <BLANKLINE>
    2 Results from the SOARClient:
    <BLANKLINE>
    Instrument Data product Level        Start time               End time        Filesize SOOP Name Detector Wavemin  Wavemax
                                                                                Mbyte
    ---------- ------------ ----- ----------------------- ----------------------- -------- --------- -------- -------- --------
        PHI phi-fdt-blos    L2 2023-02-01 21:00:09.414 2023-02-01 21:01:09.262    2.586      None      FDT 6173.065 6173.501
        PHI phi-fdt-icnt    L2 2023-02-01 21:00:09.414 2023-02-01 21:01:09.262    2.586      None      FDT 6173.065 6173.501
    <BLANKLINE>
    <BLANKLINE>

For instrument PHI passing a single of Wavelength
=================================================

When a single value given for wavelength is interpreted as the wavemin.

.. code-block:: python


    >>> wavelength=a.Wavelength(6173.065*u.AA)
    >>> result = Fido.search(instrument & time & level) # doctest: +REMOTE_DATA
    >>> result  # doctest: +REMOTE_DATA
    Results from 1 Provider:
    <BLANKLINE>
    4 Results from the SOARClient:
    <BLANKLINE>
    Instrument Data product Level        Start time               End time        Filesize SOOP Name Detector Wavemin  Wavemax
                                                                                Mbyte
    ---------- ------------ ----- ----------------------- ----------------------- -------- --------- -------- -------- --------
        PHI phi-fdt-blos    L2 2023-02-01 15:00:09.367 2023-02-01 15:01:09.241     2.58      None      FDT 6173.065 6173.502
        PHI phi-fdt-icnt    L2 2023-02-01 15:00:09.367 2023-02-01 15:01:09.241     2.58      None      FDT 6173.065 6173.502
        PHI phi-fdt-blos    L2 2023-02-01 21:00:09.414 2023-02-01 21:01:09.262    2.586      None      FDT 6173.065 6173.501
        PHI phi-fdt-icnt    L2 2023-02-01 21:00:09.414 2023-02-01 21:01:09.262    2.586      None      FDT 6173.065 6173.501
    <BLANKLINE>
    <BLANKLINE>
