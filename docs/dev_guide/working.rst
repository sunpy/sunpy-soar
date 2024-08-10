.. _sunpy-soar-dev-guide-working:

*****************************
How does ``sunpy-soar`` work?
*****************************

``sunpy-soar`` is a Python library developed to interact with the SOAR (Solar Orbiter Archive) data
hosted by ESA (European Space Agency). It provides tools and utilities to access, search, download and
analyze data collected by the Solar Orbiter mission.

How data is retrived from SOAR
==============================
 
To retrieve data from SOAR, you first use the ``Fido`` object from SunPy
and specify the desired attributes using `sunpy.net.attrs`. These
attributes define the criteria for the data you want to retrieve, such as the
time range, instrument, or wavelength. Here is an example of how to specify
the time range for the data you want to retrieve:

.. code-block:: python

    import sunpy.net.attrs as a
    from sunpy.net import Fido
    import sunpy_soar

    instrument = a.Instrument("EUI")
    time = a.Time("2021-02-01", "2021-02-02")
    level = a.Level(1)
    product = a.soar.Product("EUI-FSI174-IMAGE")

    result = Fido.search(instrument & time & level & product)


``sunpy-soar`` constructs the query based on the specified criteria, then generates a URL to interact with the SOAR API.
This is done by using the Table Access Protocol (TAP), a widely adopted standard in the astronomical community for accessing large datasets.
The results are returned in the form of an Astropy table, providing a structured and efficient format for further analysis and visualization within the Python environment.

