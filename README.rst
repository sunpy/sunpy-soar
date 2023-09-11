**************
``sunpy-soar``
**************

|ci-status| |coverage|

.. |ci-status| image:: https://github.com/sunpy/sunpy-soar/actions/workflows/ci.yml/badge.svg
    :alt: CI status

.. |coverage| image:: https://codecov.io/gh/dstansby/sunpy-soar/branch/main/graph/badge.svg?token=5NKZHBX3AW
   :target: https://codecov.io/gh/dstansby/sunpy-soar
   :alt: Code coverage

.. note::

  With the updates to the SOAR, the product names now need to be lowercase.
  This is fixed with the latest release of sunpy-soar, so you will need to update if you are having issues finding data.

A sunpy Fido plugin for accessing data in the Solar Orbiter Archive (SOAR).

Installation
------------

``sunpy-soar`` requires ``python >= 3.9`` and `sunpy >= 5.0`.
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

Getting Help
============

For more information or to ask questions about ``sunpy-soar`` or any other SunPy library, check out:

-  `sunpy-soar documentation <https://docs.sunpy.org/en/stable/>`__
-  `SunPy Chat`_
-  `SunPy mailing list <https://groups.google.com/forum/#!forum/sunpy>`__
-  `SunPy Community forum <https://community.openastronomy.org/c/sunpy/5>`__

Contributing
============

If you would like to get involved, start by joining the `SunPy Chat`_ and check out our `Newcomers' guide <https://docs.sunpy.org/en/latest/dev_guide/contents/newcomers.html>`__.
This will walk you through getting set up for contributing.

Code of Conduct
===============

When you are interacting with the SunPy community you are asked to follow our `Code of Conduct <https://sunpy.org/coc>`__.

.. _SunPy Chat: https://app.element.io/#/room/#sunpy:openastronomy.org
