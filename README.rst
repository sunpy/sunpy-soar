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

   from sunpy.net.attrs import Instrument, Level, Time
   from sunpy_soar.attrs import Identifier

   # Create search attributes
   instrument = Instrument('EUI')
   time = Time('2021-02-01', '2021-02-02')
   level = Level(1)
   identifier = Identifier('EUI-FSI174-IMAGE')

   # Do search
   result = Fido.search(instrument & time & level & identifier)
   print(result)

   # Download files
   files = Fido.fetch(result)
   print(files)

Available search attributes
---------------------------

When constructing a search, ``sunpy.net.attrs.Time`` must be provided.
Other search attributes can be used too; sunpy-soar recognises the following:

- ``sunpy.net.attrs.Instrument``
- ``sunpy.net.attrs.Level``
- ``sunpy_soar.attrs.Identifier``


Changelog
---------
1.1
~~~
- Fixed download of data where multiple versions of the requested file are
  available. Only the most recent version will be downloaded.
- Added some log messages to the sunpy logger at DEBUG level
