Changelog
=========

1.2
---
- Allow time-only searches to be made.
- Registered the ``Identifier`` attribute in the ``sunpy.net.attrs.soar``
  namespace. With ``import sunpy.net.attrs as a``, the attribute can now be
  accessed using ``a.soar.Identifier``.
- The ``"Filesize"`` column in returned results now has units of
  ``astropy.units.Mbyte`` (previously it had no units).

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
