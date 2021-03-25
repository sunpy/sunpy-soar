sunpy-soar
==========

A sunpy plugin for accessing data in the Solar Orbiter Archive (SOAR).

|build-status| |coverage|

.. |build-status| image:: https://github.com/dstansby/sunpy-soar/actions/workflows/python-test.yml/badge.svg
    :alt: build status


.. |coverage| image:: https://codecov.io/gh/dstansby/sunpy-soar/branch/main/graph/badge.svg?token=5NKZHBX3AW
   :target: https://codecov.io/gh/dstansby/sunpy-soar
   :alt: code coverage

Installation
------------

.. code-block:: bash

   pip install sunpy-soar

Example usage
-------------

.. code-block:: python

   # Importing sunpy_soar registers the client with sunpy
   import sunpy_soar
   from sunpy.net import Fido

   from sunpy.net.attrs import Instrument, Level, Time
   from sunpy_soar.attrs import Identifier

   instrument = Instrument('EUI')
   time = Time('2020-02-01', '2021-02-02')
   level = a.Level(1)
   identifier = Identifier('EUI-FSI174-IMAGE')

   res = Fido.search(instrument, time, level, identifier)
   print(res)
