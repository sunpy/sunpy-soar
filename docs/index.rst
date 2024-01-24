****************************
``sunpy-soar`` Documentation
****************************

A sunpy Fido plugin for accessing data in the Solar Orbiter Archive (SOAR).

.. toctree::
   :maxdepth: 1

   changelog
   generated/gallery/index

Installation
============

``sunpy-soar`` requires ``python >= 3.9`` and ``sunpy >= 5.0``.
Currently it can only be installed from PyPI using:

.. code-block:: bash

   pip install sunpy_soar

or conda using

.. code-block:: bash

   conda install -c conda-forge sunpy_soar

Example
=======

The code below gives an example of how to search and download Solar Orbiter data using ``sunpy.net.Fido``:

.. code-block:: python

   # Importing sunpy_soar registers the client with sunpy
   >>> import sunpy_soar
   >>> from sunpy.net import Fido
   >>> import sunpy.net.attrs as a

   # Create search attributes
   >>> instrument = a.Instrument('EUI')
   >>> time = a.Time('2021-02-01', '2021-02-02')
   >>> level = a.Level(1)
   >>> product = a.soar.Product('EUI-FSI174-IMAGE')

   # Do search
   >>> result = Fido.search(instrument & time & level & product)
   >>> print(result)
   Results from 1 Provider:
   <BLANKLINE>
   43 Results from the SOARClient:
   <BLANKLINE>
   Instrument   Data product   Level        Start time               End time        Filesize SOOP Name
                                                                                    Mbyte
   ---------- ---------------- ----- ----------------------- ----------------------- -------- ---------
         EUI eui-fsi174-image    L1 2021-02-01 00:45:12.228 2021-02-01 00:45:22.228    3.393      none
         EUI eui-fsi174-image    L1 2021-02-01 01:15:12.232 2021-02-01 01:15:22.232    0.418      none
         EUI eui-fsi174-image    L1 2021-02-01 01:45:12.237 2021-02-01 01:45:22.237    0.406      none
         EUI eui-fsi174-image    L1 2021-02-01 02:15:12.238 2021-02-01 02:15:22.238    3.352      none
         EUI eui-fsi174-image    L1 2021-02-01 02:45:12.241 2021-02-01 02:45:22.241    0.406      none
         EUI eui-fsi174-image    L1 2021-02-01 03:15:12.244 2021-02-01 03:15:22.244    0.406      none
         ...              ...   ...                     ...                     ...      ...       ...
         EUI eui-fsi174-image    L1 2021-02-01 20:44:52.224 2021-02-01 20:45:02.224    0.409      none
         EUI eui-fsi174-image    L1 2021-02-01 21:15:12.227 2021-02-01 21:15:22.227    3.387      none
         EUI eui-fsi174-image    L1 2021-02-01 21:45:12.230 2021-02-01 21:45:22.230    0.412      none
         EUI eui-fsi174-image    L1 2021-02-01 22:15:12.233 2021-02-01 22:15:22.233    0.415      none
         EUI eui-fsi174-image    L1 2021-02-01 22:44:52.236 2021-02-01 22:45:02.236    0.423      none
         EUI eui-fsi174-image    L1 2021-02-01 23:15:12.239 2021-02-01 23:15:22.239    3.459      none
         EUI eui-fsi174-image    L1 2021-02-01 23:45:12.242 2021-02-01 23:45:22.242    0.415      none
   Length = 43 rows
   <BLANKLINE>
   <BLANKLINE>

   # Download files
   >>> files = Fido.fetch(result)  # doctest: +SKIP
   >>> print(files)  # doctest: +SKIP

Available search attributes
===========================

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

For more information or to ask questions about ``sunpy-soar`` or any other SunPy Project library, check out:

-  `sunpy-soar documentation <https://docs.sunpy.org/en/stable/>`__
-  `SunPy chat`_
-  `SunPy mailing list <https://groups.google.com/forum/#!forum/sunpy>`__
-  `SunPy community forum <https://community.openastronomy.org/c/sunpy/5>`__

Contributing
============

If you would like to get involved, start by joining the `SunPy Chat`_ and check out our `Newcomers' guide <https://docs.sunpy.org/en/latest/dev_guide/contents/newcomers.html>`__.
This will walk you through getting set up for contributing.

Code of Conduct
===============

When you are interacting with the SunPy community you are asked to follow our `Code of Conduct <https://sunpy.org/coc>`__.

.. _SunPy Chat: https://app.element.io/#/room/#sunpy:openastronomy.org

Reference/API
=============

.. automodapi:: sunpy_soar
