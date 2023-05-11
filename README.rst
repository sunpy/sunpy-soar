sunpy-soar
==========

A sunpy plugin for accessing data in the Solar Orbiter Archive (SOAR).

|build-status| |coverage|

.. |build-status| image:: https://github.com/dstansby/sunpy-soar/actions/workflows/python-test.yml/badge.svg
    :alt: build status


.. |coverage| image:: https://codecov.io/gh/dstansby/sunpy-soar/branch/main/graph/badge.svg?token=5NKZHBX3AW
   :target: https://codecov.io/gh/dstansby/sunpy-soar
   :alt: code coverage


When interacting with the sunpy-soar project you are asked to follow the `SunPy Code of Conduct <https://sunpy.org/coc>`_ .

Installation
------------

sunpy-soar requires `python >= 3.7` and `sunpy >= 2.1`.
Currently it can only be installed from PyPI using:

.. code-block:: bash

   pip install sunpy-soar

or conda using

.. code-block:: bash

   conda install -c conda-forge sunpy-soar

Example usage
-------------

The code below gives an example of how to search and download Solar Orbiter data using ``sunpy.net.Fido``:

.. code-block:: python

   # Importing sunpy_soar registers the client with sunpy
   import sunpy_soar
   from sunpy.net import Fido
   import sunpy.net.attrs as a

   # Create search attributes
   instrument = a.Instrument('EUI')
   time = a.Time('2021-02-01', '2021-02-02')
   level = a.Level(1)
   product = a.soar.Product('EUI-FSI174-IMAGE')

   # Do search
   result = Fido.search(instrument & time & level & product)
   print(result)

   # Download files
   files = Fido.fetch(result)
   print(files)

Available search attributes
---------------------------
The easiest way to access search attributes is using ``import sunpy.net.attrs as a``.
When constructing a search for SOAR ``a.Time`` must be provided.
Other search attributes can be used too - ``sunpy-soar`` recognises the following:

- ``a.Instrument``
- ``a.Level`` - one of ``L0, L1, L2, L3, LL01, LL02, LL03``
- ``a.soar.Product``

The third ``near`` argument to ``a.Time`` is not currently supported - you will have to manually filter the results if you want to find the one closest to a given time.

``sunpy-soar`` and the VSO
==========================
``sunpy-soar`` queries the official repository of Solar Orbiter data, the SOAR.
The Virtual Solar Observatory (VSO) as of writing (September 2022) mirrors a subset of the Solar Orbiter archive alongside many other solar physics data sources.
The VSO allows data from multiple missions/observatories to be easily queried in one go, but users should be aware that the VSO is not the official repository for Solar Orbiter data and does not currently (as of September 2022) provide a comprehensive listing of all available Solar Orbiter data.

Development
===========
The SunPy developers maintain this package.
Contributions for new features and bug fixes are welcome.

Changelog
=========

1.8
---
- Added ability to query with SOOP name.

1.7
---
- Added STIX data products to the list of valid data product identifiers.

1.6
---
- Registered a list of instruments available from the SOAR, with the ``a.Instrument`` attribute.
- Registered the SOAR in the ``a.Provider`` attribute, meaning that a user can specifiy to the Fido search to only query the SOAR by use of ``a.Provider.soar``.
- The ``_can_handle_query`` function within the SOARClient now checks to make sure if the SOAR supplies the queried data which fixes a bug which searched the SOAR for any data (e.g. AIA data).

1.5
---
- Registered a list of valid data product identifiers with the ``a.soar.Product`` attribute. To see these use ``print(a.soar.Product)``.

1.4
---
- Added support for searching for and fetching low latency data.

1.3
---

- Added support for path string interpolation, which allows you to do (for example)
  ``Fido.fetch(query, path=tmp_path / '{instrument}')`` and the name of the intrument will be used in the save path.
  This works for all supported Fido attrs.

1.2
---
- The ``Identifier`` attribute is deprecated - use ``Product`` instead, which
  is a direct replacement (with a better name!).
- Allow time-only searches to be made.
- Registered the ``Product`` attribute in the ``sunpy.net.attrs.soar``
  namespace. After running ``import sunpy.net.attrs as a``, the attribute can
  now be accessed using ``a.soar.Product``.
- The ``"Filesize"`` column in returned results now has units of
  ``astropy.units.Mbyte`` (previously it had no units).
- Removed a validation check on ``a.Level``. If an level that SOAR doesn't
  understand is passed, zero results will now be returned instead of an error
  being raised.

1.1
---
- Fixed download of data where multiple versions of the requested file are
  available. Only the most recent version will be downloaded.
- Added some log messages to the sunpy logger at DEBUG level

1.0
---
First stable sunpy-soar release.

- Fixed searches where there are no results.
- Added filesize to the result table
- Raise an error if the SOAR server can't be reached

1.0b1
-----
First sunpy-soar release.
