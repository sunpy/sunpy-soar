1.8
===

- Added ability to query with SOOP name.

1.7
===

- Added STIX data products to the list of valid data product identifiers.

1.6
===

- Registered a list of instruments available from the SOAR, with the ``a.Instrument`` attribute.
- Registered the SOAR in the ``a.Provider`` attribute, meaning that a user can specify to the Fido search to only query the SOAR by use of ``a.Provider.soar``.
- The ``_can_handle_query`` function within the SOARClient now checks to make sure if the SOAR supplies the queried data which fixes a bug which searched the SOAR for any data (e.g. AIA data).

1.5
===

- Registered a list of valid data product identifiers with the ``a.soar.Product`` attribute.
  To see these use ``print(a.soar.Product)``.

1.4
===

- Added support for searching for and fetching low latency data.

1.3
===

- Added support for path string interpolation, which allows you to do (for example)
  ``Fido.fetch(query, path=tmp_path / '{instrument}')`` and the name of the instrument will be used in the save path.
  This works for all supported Fido attrs.

1.2
===

- The ``Identifier`` attribute is deprecated - use ``Product`` instead, which is a direct replacement (with a better name!).
- Allow time-only searches to be made.
- Registered the ``Product`` attribute in the ``sunpy.net.attrs.soar`` namespace.
  After running ``import sunpy.net.attrs as a``, the attribute can now be accessed using ``a.soar.Product``.
- The ``"Filesize"`` column in returned results now has units of ``astropy.units.Mbyte`` (previously it had no units).
- Removed a validation check on ``a.Level``.
  If an level that SOAR doesn't understand is passed, zero results will now be returned instead of an error
  being raised.

1.1
===

- Fixed download of data where multiple versions of the requested file are available.
  Only the most recent version will be downloaded.
- Added some log messages to the sunpy logger at DEBUG level

1.0
===

- Fixed searches where there are no results.
- Added filesize to the result table
- Raise an error if the SOAR server can't be reached
