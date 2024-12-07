****************************
``sunpy-soar`` Documentation
****************************

A sunpy Fido plugin for accessing data in the Solar Orbiter Archive (SOAR).

Installation
============

``sunpy-soar`` requires ``python >= 3.10`` and ``sunpy >= 5.0``.
Currently it can be installed from PyPI using:

.. code-block:: bash

   pip install sunpy-soar

or conda using

.. code-block:: bash

   conda install -c conda-forge sunpy-soar

``sunpy-soar`` and the VSO
==========================

``sunpy-soar`` queries the official repository of Solar Orbiter data, the SOAR.
The Virtual Solar Observatory (VSO) as of writing (September 2022) mirrors a subset of the Solar Orbiter archive alongside many other solar physics data sources.
The VSO allows data from multiple missions/observatories to be easily queried in one go, but users should be aware that the VSO is not the official repository for Solar Orbiter data and does not currently (as of September 2022) provide a comprehensive listing of all available Solar Orbiter data.

Getting Help
============

For more information or to ask questions about ``sunpy-soar`` or any other SunPy Project library, check out:

-  `sunpy-soar documentation <https://docs.sunpy.org/projects/soar/>`__
-  `SunPy chat`_
-  `SunPy mailing list <https://groups.google.com/forum/#!forum/sunpy>`__
-  `SunPy community forum <https://community.openastronomy.org/c/sunpy/5>`__

Contributing
============

If you would like to get involved, start by joining the `SunPy Chat`_ and check out our `Newcomers' guide <https://docs.sunpy.org/en/latest/dev_guide/contents/newcomers.html>`__.
This will walk you through getting set up for contributing.

.. _SunPy Chat: https://app.element.io/#/room/#sunpy:openastronomy.org

.. toctree::
   :hidden:

   generated/gallery/index
   how_to/index
   api
   whatsnew/index
   coc
