.. _sunpy-soar-dev-guide-tables:

**********************************
Tables supported in ``sunpy-soar``
**********************************

The ``sunpy-soar`` library currently supports data retrieval from both science and low-latency data tables, such as
``v_sc_data_item`` and ``v_ll_data_item``. Additionally, it provides support for join tables associated with remote
instruments, such as ``v_eui_sc_fits``.

In the context of ``sunpy-soar``, data tables contain columns related to scientific measurements, while instrument
tables contain metadata specific to particular instruments. The ``sunpy-soar`` library specifically supports the
wavelength and detector columns within these tables. These columns are linked to the data columns in the instrument
tables through a join operation, using the ``data_item_oid`` as the key.

How can a new column be added?
==============================

If the new column you wish to add is part of an existing data or instrument FITS table, you can extend the
corresponding ADQL query to include this column. For example, if the new column is in the instrument table, it should
be included in the SELECT clause of the query for that table.

Moreover, if filtering by this new column is required, you must consider adding it as an attribute in the ``attrs.py``
file. If the column already exists within `sunpy.net.attrs`, you should add a corresponding walker in the
``attrs.py`` file. The ``_can_handle_query`` method in the ``client.py`` file should also be updated to ensure proper
support for this new column in queries.

How can a new table be added?
=============================

When adding support for a new table in ``sunpy-soar``, it is essential to fully understand the context and requirements.
This includes identifying the key that will be used for join operations and determining what data should be
returned to the user.

For direct joins, the key relationship between the tables should be carefully identified. Once the joins are
established, the necessary columns can be included in the query, following the process outlined for adding columns.

Depending on the use case, you might need to determine the type of join (e.g., inner join, outer join, left join) and what
specific tables or columns should be displayed to the user. In some cases, conditional logic may be required, where
certain attributes in the search query trigger specific join operations or column selections.

Finally, ensure that the ``_do_search`` method is updated to reflect these changes. This method should handle any
additional columns or conditional logic for attribute-specific queries, ensuring that the appropriate data is returned
to the user.

Note
====

Accordingly, test cases for every extreme and usual case must be added, to show full functionality of the added table or column.
