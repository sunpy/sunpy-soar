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

sunpy-soar requires `python >= 3.7` and `sunpy >= 2.1`. Currently it can only be installed from
PyPI using:

.. code-block:: bash

   pip install sunpy-soar

or conda using

.. code-block:: bash

   conda install -c conda-forge sunpy-soar

Example usage
-------------

The code below gives an example of how to search and download Solar Orbiter
data using ``sunpy.net.Fido``:

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
The easiest way to access search attributes is using
``import sunpy.net.attrs as a``. When constructing a search, ``a.Time`` must be
provided. Other search attributes can be used too - sunpy-soar recognises the
following:

- ``a.Instrument``
- ``a.Level``
- ``a.soar.Product``

The third ``near`` argument to ``a.Time`` is not supported - you will have to
manually filter the results if you want to find the one closest to a given
time.

Changelog
=========

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
