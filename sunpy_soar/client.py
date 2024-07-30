import json
import pathlib
import re
from json.decoder import JSONDecodeError

import astropy.table
import astropy.units as u
import requests
import sunpy.net.attrs as a
from sunpy import log
from sunpy.net.attr import and_
from sunpy.net.base_client import BaseClient, QueryResponseTable
from sunpy.time import parse_time

from sunpy_soar.attrs import FOV, SOOP, Product, walker

__all__ = ["SOARClient"]


class SOARClient(BaseClient):
    """
    Client to access the Solar Orbiter Archive (SOAR).
    """

    def search(self, *query, **kwargs):  # NOQA: ARG002
        query = and_(*query)
        queries = walker.create(query)

        results = []
        for query_parameters in queries:
            if "provider='SOAR'" in query_parameters:
                query_parameters.remove("provider='SOAR'")
            results.append(self._do_search(query_parameters))
        table = astropy.table.vstack(results)
        qrt = QueryResponseTable(table, client=self)
        qrt["Filesize"] = (qrt["Filesize"] * u.byte).to(u.Mbyte).round(3)
        qrt.hide_keys = [
            "Data item ID",
            "Filename",
        ]
        return qrt

    @staticmethod
    def determine_fov_table(query):
        """
        Determine the value of 'm' based on the FOV parameter in the query.

        Parameters
        ----------
        query : list[str]
            List of query items.

        Returns
        -------
        str or None
            The value of 'm' ("earth", "solo", or None).
        """
        for q in query:
            match = re.match(r"FOV\s*=\s*'([^']+)'", q)
            if match:
                fov_value = match.group(1).lower()
                if fov_value == "earth":
                    return "earth"
                if fov_value == "solar":
                    return "solo"
        return None

    def fov_join(self, query, instrument_table: str, where_part: str, from_part: str, select_part: str):
        """
        Add FoV (Field of View) join to the query if applicable based on the
        instrument.

        Parameters
        ----------
        instrument_table : str
            Name of the instrument table.
        where_part : str
            The WHERE part of the ADQL query.
        from_part : str
            The FROM part of the ADQL query.
        select_part : str
            The SELECT part of the ADQL query.

        Returns
        -------
        tuple[str, str, str]
            Updated WHERE, FROM, and SELECT parts of the query.
        """
        m = self.determine_fov_table(query)
        if not m:
            return where_part, from_part, select_part

        join_tables = {
            "eui": (
                "v_eui_hri_fov",
                f"fov_{m}_bot_left_arcsec_ty, h3.fov_{m}_bot_left_arcsec_tx, "
                f"h3.fov_{m}_top_right_arcsec_ty, h3.fov_{m}_top_right_arcsec_tx",
            ),
            "spi": (
                "v_spice_fov",
                f"fov_{m}_bot_left_arcsec_ty, h3.fov_{m}_bot_left_arcsec_tx, "
                f"h3.fov_{m}_top_right_arcsec_ty, h3.fov_{m}_top_right_arcsec_tx",
            ),
            "phi": (
                "v_phi_hrt_fov",
                f"fov_{m}_bot_left_arcsec_ty, h3.fov_{m}_bot_left_arcsec_tx, "
                f"h3.fov_{m}_top_right_arcsec_ty, h3.fov_{m}_top_right_arcsec_tx",
            ),
        }
        for instrument, (table, fields) in join_tables.items():
            if instrument in instrument_table:
                from_part += f" LEFT JOIN {table} AS h3 ON h2.filename = h3.filename"
                select_part += f", {fields}"
                break

        return where_part, from_part, select_part

    def add_join_to_query(self, query: list[str], data_table: str, instrument_table: str):
        """
        Construct the WHERE, FROM, and SELECT parts of the ADQL query.

        Parameters
        ----------
        query : list[str]
            List of query items.
        data_table : str
            Name of the data table.
        instrument_table : str
            Name of the instrument table.

        Returns
        -------
        tuple[str, str, str]
            WHERE, FROM, and SELECT parts of the query.
        """
        final_query = ""
        # Extract wavemin and wavemax individually
        wavemin_pattern = re.compile(r"Wavemin='(\d+\.\d+)'")
        wavemax_pattern = re.compile(r"Wavemax='(\d+\.\d+)'")
        for parameter in query:
            if parameter.startswith("FOV"):
                continue
            wavemin_match = wavemin_pattern.search(parameter)
            wavemax_match = wavemax_pattern.search(parameter)
            # If the wavemin and wavemax are the same, that means only one wavelength is given in the query.
            if wavemin_match and wavemax_match and float(wavemin_match.group(1)) == float(wavemax_match.group(1)):
                parameter = f"Wavelength='{wavemin_match.group(1)}'"
            elif wavemin_match and wavemax_match:
                parameter = f"Wavemin='{wavemin_match.group(1)}'+AND+h2.Wavemax='{wavemax_match.group(1)}'"
            prefix = "h2." if parameter.startswith(("Detector", "Wave", "Observation")) else "h1."
            if parameter.startswith("begin_time"):
                time_list = parameter.split("+AND+")
                final_query += f"h1.{time_list[0]}+AND+h1.{time_list[1]}+AND+"
                if "stx" not in instrument_table:
                    final_query += "h2.dimension_index='1'+AND+"
            else:
                final_query += f"{prefix}{parameter}+AND+"

        where_part = final_query[:-5]
        from_part = f"{data_table} AS h1"
        select_part = (
            "h1.instrument, h1.descriptor, h1.level, h1.begin_time, h1.end_time, h1.data_item_id, "
            "h1.filesize, h1.filename, h1.soop_name, h2.wavelength, h2.detector, h2.dimension_index"
        )
        # Add the second join always
        from_part += f" JOIN {instrument_table} AS h2 ON h1.data_item_oid = h2.data_item_oid"

        # Add the third join conditionally based on the instrument and other conditions
        if any(q.startswith("FOV") for q in query):
            where_part, from_part, select_part = self.fov_join(
                query, instrument_table, where_part, from_part, select_part
            )

        return where_part, from_part, select_part

    @staticmethod
    def _construct_payload(query):
        """
        Construct search payload.

        Parameters
        ----------
        query : list[str]
            List of query items.

        Returns
        -------
        dict
            Payload dictionary to be sent with the query.
        """
        # Default data table
        data_table = "v_sc_data_item"
        instrument_table = None
        # Mapping is established between the SOAR instrument names and its corresponding SOAR instrument table alias.
        instrument_mapping = {
            "SOLOHI": "SHI",
            "EUI": "EUI",
            "STIX": "STX",
            "SPICE": "SPI",
            "PHI": "PHI",
            "METIS": "MET",
        }

        instrument_name = None
        for q in query:
            if q.startswith("instrument") or q.startswith("descriptor") and not instrument_name:
                instrument_name = q.split("=")[1][1:-1].split("-")[0].upper()
            elif q.startswith("level") and q.split("=")[1][1:3] == "LL":
                data_table = "v_ll_data_item"

        if instrument_name:
            if instrument_name in instrument_mapping:
                instrument_name = instrument_mapping[instrument_name]
            instrument_table = f"v_{instrument_name.lower()}_sc_fits"
            if data_table == "v_ll_data_item" and instrument_table:
                instrument_table = instrument_table.replace("_sc_", "_ll_")

        # Need to establish join for remote sensing instruments as they have instrument tables in SOAR.
        if instrument_name in ["EUI", "MET", "SPI", "PHI", "SHI"]:
            where_part, from_part, select_part = SOARClient().add_join_to_query(query, data_table, instrument_table)
        else:
            from_part = data_table
            select_part = "*"
            where_part = "+AND+".join(query)

        adql_query = {"SELECT": select_part, "FROM": from_part, "WHERE": where_part}

        adql_query_str = "+".join([f"{key}+{value}" for key, value in adql_query.items()])
        return {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql_query_str}

    @staticmethod
    def _do_search(query):
        """
        Query the SOAR server with a single query.

        Parameters
        ----------
        query : list[str]
            List of query items.

        Returns
        -------
        astropy.table.QTable
            Query results.
        """
        tap_endpoint = "http://soar.esac.esa.int/soar-sl-tap/tap"
        payload = SOARClient._construct_payload(query)
        # Need to force requests to not form-encode the parameters
        payload = "&".join([f"{key}={val}" for key, val in payload.items()])
        r = requests.get(f"{tap_endpoint}/sync", params=payload)
        log.debug(f"Sent query: {r.url}")
        r.raise_for_status()
        try:
            response_json = r.json()
        except JSONDecodeError as err:
            msg = "The SOAR server returned an invalid JSON response. It may be down or not functioning correctly."
            raise RuntimeError(msg) from err

        # Do some list/dict wrangling
        names = [m["name"] for m in response_json["metadata"]]
        info = {name: [] for name in names}

        for entry in response_json["data"]:
            for i, name in enumerate(names):
                info[name].append(entry[i])

        if len(info["begin_time"]):
            info["begin_time"] = parse_time(info["begin_time"]).iso
            info["end_time"] = parse_time(info["end_time"]).iso

        m = SOARClient.determine_fov_table(query)
        contains_fov = any(q.lower().startswith("fov") for q in query)
        if not contains_fov:
            result_table = astropy.table.QTable(
                {
                    "Instrument": info["instrument"],
                    "Data product": info["descriptor"],
                    "Level": info["level"],
                    "Start time": info["begin_time"],
                    "End time": info["end_time"],
                    "Data item ID": info["data_item_id"],
                    "Filename": info["filename"],
                    "Filesize": info["filesize"],
                    "SOOP Name": info["soop_name"],
                },
            )
            if "wavelength" in info:
                result_table["Wavelength"] = info["wavelength"]
            if "detector" in info:
                result_table["Detector"] = info["detector"]
        else:
            result_table = astropy.table.QTable(
                {
                    "Instrument": info["instrument"],
                    "Start time": info["begin_time"],
                    "End time": info["end_time"],
                    "Filesize": info["filesize"],
                    f"fov_{m}_left_arcsec_ty": info[f"fov_{m}_bot_left_arcsec_ty"],
                    f"fov_{m}_left_arcsec_tx": info[f"fov_{m}_bot_left_arcsec_tx"],
                    f"fov_{m}_right_arcsec_ty": info[f"fov_{m}_top_right_arcsec_ty"],
                    f"fov_{m}_right_arcsec_tx": info[f"fov_{m}_top_right_arcsec_tx"],
                },
            )
        result_table.sort("Start time")
        return result_table

    def fetch(self, query_results, *, path, downloader, **kwargs):  # NOQA: ARG002
        """
        Queue a set of results to be downloaded.
        `sunpy.net.base_client.BaseClient` does the actual downloading, so we
        just have to queue up the ``downloader``.

        Parameters
        ----------
        query_results : sunpy.net.fido_factory.UnifiedResponse
            Results from a Fido search.
        path : str
            Path to download files to. Must be a format string with a ``file``
            field for the filename.
        downloader : parfive.Downloader
            Downloader instance used to download data.
        kwargs :
            Keyword arguments aren't used by this client.
        """
        base_url = "http://soar.esac.esa.int/soar-sl-tap/data?" "retrieval_type=LAST_PRODUCT"

        for row in query_results:
            url = base_url
            if row["Level"].startswith("LL"):
                url += "&product_type=LOW_LATENCY"
            else:
                url += "&product_type=SCIENCE"
            data_id = row["Data item ID"]
            url += f"&data_item_id={data_id}"
            filepath = str(path).format(file=row["Filename"], **row.response_block_map)
            log.debug(f"Queuing URL: {url}")
            downloader.enqueue_file(url, filename=filepath)

    @classmethod
    def _can_handle_query(cls, *query):
        """
        Check if this client can handle a given Fido query. Checks to see if a
        SOAR instrument or product is provided in the query.

        Returns
        -------
        bool
            True if this client can handle the given query.
        """
        required = {a.Time}
        optional = {a.Instrument, a.Detector, a.Wavelength, a.Level, a.Provider, Product, SOOP, FOV}
        if not cls.check_attr_types_in_query(query, required, optional):
            return False
        # check to make sure the instrument attr passed is one provided by the SOAR.
        # also check to make sure that the provider passed is the SOAR for which this client can handle.
        instr = [i[0].lower() for i in cls.register_values()[a.Instrument]]
        for x in query:
            if isinstance(x, a.Instrument) and str(x.value).lower() not in instr:
                return False
            if isinstance(x, a.Provider) and str(x.value).lower() != "soar":
                return False
        return True

    @classmethod
    def _attrs_module(cls):
        # Register SOAR specific attributes with Fido
        return "soar", "sunpy_soar.attrs"

    @classmethod
    def register_values(cls):
        return cls.load_dataset_values()

    @staticmethod
    def load_dataset_values():
        # Instrument attrs
        attrs_path = pathlib.Path(__file__).parent / "data" / "attrs.json"
        with attrs_path.open() as attrs_file:
            all_datasets = json.load(attrs_file)
        # Convert from dict to list of tuples
        all_datasets = list(all_datasets.items())

        # Instrument attrs
        instr_path = pathlib.Path(__file__).parent / "data" / "instrument_attrs.json"
        with instr_path.open() as instr_attrs_file:
            all_instr = json.load(instr_attrs_file)
        all_instr = list(all_instr.items())

        soop_path = pathlib.Path(__file__).parent / "data" / "soop_attrs.json"
        with soop_path.open() as soop_path_file:
            all_soops = json.load(soop_path_file)

        all_soops = list(all_soops.items())

        return {
            Product: all_datasets,
            a.Instrument: all_instr,
            SOOP: all_soops,
            a.Provider: [("SOAR", "Solar Orbiter Archive.")],
        }
