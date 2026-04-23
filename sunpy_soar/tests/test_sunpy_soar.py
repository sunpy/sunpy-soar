from pathlib import Path

import astropy.units as u
import pytest
import responses
import sunpy.map
from requests.exceptions import HTTPError
from sunpy.net import Fido
from sunpy.net import attrs as a
from sunpy.util.exceptions import SunpyUserWarning

from sunpy_soar.client import SOARClient

SUNPY_VERSION = (sunpy.version.major, sunpy.version.minor)


@pytest.mark.remote_data
def test_search() -> None:
    instrument = a.Instrument("EUI")
    time = a.Time("2022-02-11", "2022-02-12")
    level = a.Level(1)
    product = a.soar.Product("eui-fsi174-image")

    res = Fido.search(instrument, time, level, product)
    assert len(res) == 1
    assert len(res[0]) == 660
    assert u.allclose(res[0, 0]["Filesize"], 2.439 * u.Mbyte)

    # check passing upper case descriptor
    product = a.soar.Product("EUI-FSI174-IMAGE")
    res = Fido.search(time, level, product)
    assert res.file_num == 660

    files = Fido.fetch(res[0, 0])
    assert len(files) == 1
    fname = files[0]

    assert u.allclose(Path(fname).stat().st_size * u.byte, res[0, 0]["Filesize"], atol=1e-3 * u.Mbyte)

    # Smoke test that we can read this into a map
    sunpy.map.Map(fname)


@pytest.mark.remote_data
def test_search_low_latency() -> None:
    time = a.Time("2020-11-13", "2020-11-14")
    level = a.Level("LL02")
    product = a.soar.Product("epd-het-asun-rates")

    res = Fido.search(time, level, product)
    assert len(res) == 1
    assert len(res[0]) == 1

    files = Fido.fetch(res[0, 0])
    assert len(files) == 1


@pytest.mark.remote_data
def test_insitu_search() -> None:
    instrument = a.Instrument("MAG")
    time = a.Time("2020-04-16", "2020-04-17")
    product = a.soar.Product("mag-rtn-normal-1-minute")

    res = Fido.search(instrument, time, product)
    assert len(res) == 1
    assert len(res[0]) == 2

    files = Fido.fetch(res[0, 0])
    assert len(files) == 1


@pytest.mark.remote_data
def test_no_results() -> None:
    instrument = a.Instrument("EUI")
    time = a.Time("2019-02-01", "2019-02-02")
    query = instrument & time

    res = SOARClient().search(query)
    assert len(res) == 0


@pytest.mark.remote_data
def test_no_instrument() -> None:
    # Check that a time only search returns results
    time = a.Time("2020-04-16", "2020-04-17")
    res = SOARClient().search(time)
    assert len(res) == 63


@pytest.mark.remote_data
def test_download_path(tmp_path) -> None:
    # Check that we can download things to a custom path using
    # the search parameters
    instrument = a.Instrument("EUI")
    time = a.Time("2021-02-01", "2021-02-02")
    level = a.Level(1)
    res = Fido.search(instrument & time & level)
    files = Fido.fetch(res[0, 0], path=tmp_path / "{instrument}")
    assert len(files) == 1
    for f in files:
        assert "EUI" in f


def test_registered_attrs() -> None:
    attr_str = str(a.soar.Product)
    # Check that at least one attr value is registered
    assert "epd_ept_asun_burst_ele_close" in attr_str


def test_registered_instr_attrs() -> None:
    # Check if the Solo instruments are registered in a.Instrument
    instr_attr = a.Instrument
    assert "SOAR" in instr_attr._attr_registry[instr_attr].client
    assert "stix" in instr_attr._attr_registry[instr_attr].name

def test_registered_sensor_attrs() -> None:
    # Check if SolO sensors are registered in a.soar.Sensor
    sensor_attr = a.soar.Sensor
    assert "SOAR" in sensor_attr._attr_registry[sensor_attr].client
    assert "ept" in sensor_attr._attr_registry[sensor_attr].name


def test_registered_soop_names() -> None:
    # Check if the soop names are registered in a.soar.SOOP
    soop_attr = str(a.soar.SOOP)
    assert "\nr_small_mres_mcad_ar_long_term" in soop_attr


@pytest.mark.remote_data
def test_search_soop() -> None:
    instrument = a.Instrument("EUI")
    time = a.Time("2022-04-01 01:00", "2022-04-01 02:00")
    soop_attr = a.soar.SOOP.r_small_mres_mcad_ar_long_term
    res = Fido.search(time, instrument, soop_attr)
    assert "SOOP Name" in res[0].columns
    assert res.file_num == 16

    # test non valid soop name passed
    res = Fido.search(time, instrument, a.soar.SOOP("hello"))
    assert res.file_num == 0


@pytest.mark.remote_data
def test_when_soar_provider_passed() -> None:
    # Tests when a.Provider.soar is passed that only SOARClient results are returned
    instrument = a.Instrument("EUI")
    time = a.Time("2022-04-01 00:00", "2022-04-01 01:00")
    provider = a.Provider.soar
    res = Fido.search(time & instrument & provider)
    assert len(res) == 1
    assert res["soar"]


@pytest.mark.xfail(reason="Something is wrong, work it out")
def test_when_sdac_provider_passed() -> None:
    # tests that only VSO EUI results are returned when explicitly setting the provider to SDAC
    instrument = a.Instrument("EUI")
    time = a.Time("2022-04-01 00:00", "2022-04-01 01:00")
    provider = a.Provider.sdac
    res = Fido.search(time & instrument & provider)
    assert len(res) == 1
    assert res["vso"]


@pytest.mark.remote_data
def test_when_wrong_provider_passed() -> None:
    # Tests that no results are returned when a provider is passed which does not provide EUI data.
    # This is different from the above test because the SDAC and the SOAR both provide EUI data while
    # NOAA has no overlap with the data provided by the SOAR.
    instrument = a.Instrument("EUI")
    time = a.Time("2022-04-01 00:00", "2022-04-01 01:00")
    provider = a.Provider.noaa
    res = Fido.search(time & instrument & provider)
    assert len(res) == 0


@pytest.mark.remote_data
def test_search_wavelength_detector_column() -> None:
    instrument = a.Instrument("EUI")
    time = a.Time("2021-02-01", "2021-02-02")
    level = a.Level(1)
    product = a.soar.Product("EUI-FSI174-IMAGE")
    res = Fido.search(instrument & time & level & product)
    assert "Wavelength" in res[0].columns
    assert "Detector" in res[0].columns


@pytest.mark.remote_data
def test_search_detector_instrument_dimension_2() -> None:
    # Instruments "EUI", "METIS", "PHI" and "SOLOHI" have two dimensions in the SOAR data.
    # Selecting no dimension index in the query results in two identical output rows.
    # To avoid repeating data, we have methods to take dimension index=1, which avoids any repetition.
    instrument = a.Instrument("EUI")
    time = a.Time("2020-03-03", "2020-03-04")
    level = a.Level(1)
    detector = a.Detector("HRI_EUV")
    res = Fido.search(instrument & time & level & detector)
    assert "Detector" in res[0].columns
    assert res.file_num == 266


@pytest.mark.remote_data
def test_search_detector_instrument_dimension_4() -> None:
    # The "SPICE" instrument has four dimensions in the SOAR data. As a result,
    # selecting no dimension index in the query results in four identical output rows.
    # To avoid repeating data, we have methods to take dimension index=1, which avoids any repetition.
    instrument = a.Instrument("SPICE")
    time = a.Time("2023-03-03 15:00", "2023-03-03 16:00")
    level = a.Level(1)
    detector = a.Detector("SW")
    res = Fido.search(instrument & time & level & detector)
    assert "Detector" in res[0].columns
    assert res.file_num == 11


@pytest.mark.remote_data
def test_invalid_detector() -> None:
    instrument = a.Instrument("SPICE")
    time = a.Time("2023-03-03 15:00", "2023-03-03 16:00")
    level = a.Level(1)
    detector = a.Detector("hello")
    res = Fido.search(instrument & time & level & detector)
    assert "Detector" in res[0].columns
    assert res.file_num == 0


@pytest.mark.remote_data
def test_wavelength_column_wavelength_exists() -> None:
    # For instruments EUI, METIS and SOLOHI "wavelength" column is available.
    # Test to check if the "Wavelength" column exists in the search results.
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-03 15:00", "2023-04-03 16:00")
    level = a.Level(1)
    wavelength = a.Wavelength(304 * u.AA)
    res = Fido.search(instrument & time & level & wavelength)
    assert "Wavelength" in res[0].columns
    assert res.file_num == 12


@pytest.mark.remote_data
def test_wavelength_single() -> None:
    # Test to check if the wavelength value is filtered for a single value provided.
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-03 15:00", "2023-04-03 16:00")
    level = a.Level(1)
    wavelength = a.Wavelength(304 * u.AA)
    res = Fido.search(instrument & time & level & wavelength)
    for table in res:
        assert all(table["Wavelength"] == 304)


@pytest.mark.remote_data
def test_wavelength_range() -> None:
    # Test to check if the wavelength value is filtered for wavemin and wavemax provided.
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-03 15:00", "2023-04-03 16:00")
    level = a.Level(1)
    wavelength = a.Wavelength(171 * u.AA, 185 * u.AA)
    res = Fido.search(instrument & time & level & wavelength)
    for table in res:
        assert all(table["Wavelength"] == 174)


def test_join_science_query() -> None:
    result = SOARClient._construct_payload(
        [
            "instrument='EUI'",
            "begin_time>='2021-02-01 00:00:00' AND begin_time<='2021-02-02 00:00:00'",
            "level='L1'",
            "descriptor='eui-fsi174-image'",
        ]
    )

    assert result["QUERY"] == (
        "SELECT h1.instrument, h1.descriptor, h1.level, h1.begin_time, h1.end_time, "
        "h1.data_item_id, h1.filesize, h1.filename, h1.soop_name, h2.detector, h2.wavelength, "
        "h2.dimension_index FROM v_sc_data_item AS h1 JOIN v_eui_sc_fits AS h2 USING (data_item_oid)"
        " WHERE h1.instrument='EUI' AND h1.begin_time>='2021-02-01 00:00:00' AND h1.begin_time<='2021-02-02 00:00:00'"
        " AND h2.dimension_index='1' AND h1.level='L1' AND h1.descriptor='eui-fsi174-image'"
    )


def test_join_low_latency_query() -> None:
    result = SOARClient._construct_payload(
        [
            "instrument='EUI'",
            "begin_time>='2021-02-01 00:00:00' AND begin_time<='2021-02-02 00:00:00'",
            "level='LL01'",
            "descriptor='eui-fsi174-image'",
        ]
    )

    assert result["QUERY"] == (
        "SELECT h1.instrument, h1.descriptor, h1.level, h1.begin_time, h1.end_time, "
        "h1.data_item_id, h1.filesize, h1.filename, h1.soop_name, h2.detector, h2.wavelength, "
        "h2.dimension_index FROM v_ll_data_item AS h1 JOIN v_eui_ll_fits AS h2 USING (data_item_oid)"
        " WHERE h1.instrument='EUI' AND h1.begin_time>='2021-02-01 00:00:00' AND h1.begin_time<='2021-02-02 00:00:00'"
        " AND h2.dimension_index='1' AND h1.level='LL01' AND h1.descriptor='eui-fsi174-image'"
    )


def test_distance_query():
    result = SOARClient._construct_payload(
        [
            "instrument='RPW'",
            "DISTANCE(0.28,0.30)",
            "level='L2'",
        ]
    )

    assert result["QUERY"] == ("SELECT * FROM v_sc_data_item WHERE instrument='RPW' AND level='L2'&DISTANCE(0.28,0.30)")


def test_distance_join_query():
    result = SOARClient._construct_payload(
        [
            "instrument='EUI'",
            "DISTANCE(0.28,0.30)",
            "level='L2'",
            "descriptor='eui-fsi174-image'",
        ]
    )

    assert result["QUERY"] == (
        "SELECT h1.instrument, h1.descriptor, h1.level, h1.begin_time, h1.end_time, "
        "h1.data_item_id, h1.filesize, h1.filename, h1.soop_name, h2.detector, h2.wavelength, "
        "h2.dimension_index FROM v_sc_data_item AS h1 JOIN v_eui_sc_fits AS h2 USING (data_item_oid)"
        " WHERE h1.instrument='EUI' AND h1.level='L2' AND h1.descriptor='eui-fsi174-image'&DISTANCE(0.28,0.30)"
    )


def test_construct_payload_insitu_no_join():
    """In-situ instruments (e.g. MAG) should produce SELECT * with no JOIN."""
    result = SOARClient._construct_payload(
        [
            "instrument='MAG'",
            "begin_time>='2020-04-16 00:00:00' AND begin_time<='2020-04-17 00:00:00'",
            "descriptor='mag-rtn-normal-1-minute'",
        ]
    )
    assert result["REQUEST"] == "doQuery"
    assert "SELECT *" in result["QUERY"]
    assert "JOIN" not in result["QUERY"]
    assert "FROM v_sc_data_item" in result["QUERY"]


def test_construct_payload_descriptor_infers_instrument():
    """When no instrument= is given, instrument should be inferred from the descriptor."""
    result = SOARClient._construct_payload(
        [
            "begin_time>='2021-02-01 00:00:00' AND begin_time<='2021-02-02 00:00:00'",
            "level='L1'",
            "descriptor='eui-fsi174-image'",
        ]
    )
    # EUI is inferred from 'eui-fsi174-image' and should trigger the join path
    assert "JOIN v_eui_sc_fits" in result["QUERY"]
    assert "h1.descriptor='eui-fsi174-image'" in result["QUERY"]


def test_construct_payload_solohi_mapping():
    """SOLOHI should be mapped to SHI for the instrument table."""
    result = SOARClient._construct_payload(
        [
            "instrument='SOLOHI'",
            "begin_time>='2021-02-01 00:00:00' AND begin_time<='2021-02-02 00:00:00'",
            "level='L1'",
        ]
    )
    assert "JOIN v_shi_sc_fits" in result["QUERY"]


def test_construct_payload_stix_mapping():
    """STIX should be mapped to STX but should not trigger a join (not a remote sensing join instrument)."""
    result = SOARClient._construct_payload(
        [
            "instrument='STIX'",
            "begin_time>='2021-02-01 00:00:00' AND begin_time<='2021-02-02 00:00:00'",
            "level='L1'",
        ]
    )
    # STIX (STX) is not in the remote sensing join list
    assert "SELECT *" in result["QUERY"]
    assert "JOIN" not in result["QUERY"]


def test_construct_payload_distance_with_time():
    """When both distance and time are present, the query method should be doQueryFilteredByDistance
    and the DISTANCE parameter should be appended with '&' rather than ' AND '."""
    result = SOARClient._construct_payload(
        [
            "instrument='RPW'",
            "begin_time>='2023-04-27 00:00:00' AND begin_time<='2023-04-28 00:00:00'",
            "level='L2'",
            "DISTANCE(0.45,0.46)",
        ]
    )
    assert result["REQUEST"] == "doQueryFilteredByDistance"
    assert "begin_time>='2023-04-27 00:00:00'" in result["QUERY"]
    assert "&DISTANCE(0.45,0.46)" in result["QUERY"]
    # DISTANCE should not appear with ' AND ' prefix
    assert " AND DISTANCE" not in result["QUERY"]


@pytest.mark.remote_data
def test_distance_search_remote_sensing():
    instrument = a.Instrument("RPW")
    product = a.soar.Product("rpw-tnr-surv")
    level = a.Level(2)
    distance = a.soar.Distance(0.28 * u.AU, 0.30 * u.AU)
    res = Fido.search(distance & instrument & product & level)
    assert res.file_num > 40


@pytest.mark.remote_data
def test_distance_search_insitu():
    instrument = a.Instrument("METIS")
    level = a.Level(2)
    product = a.soar.Product("metis-vl-pol-angle")
    distance = a.soar.Distance(0.45 * u.AU, 0.46 * u.AU)
    res = Fido.search(distance & instrument & product & level)
    assert res.file_num == 310


@pytest.mark.remote_data
def test_distance_time_search():
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-27", "2023-04-28")
    level = a.Level(2)
    product = a.soar.Product("eui-fsi174-image")
    distance = a.soar.Distance(0.45 * u.AU, 0.46 * u.AU)
    res = Fido.search(instrument & product & level & time)
    assert res.file_num == 96
    # To check if we get different value when distance parameter is added in search.
    res = Fido.search(distance & instrument & product & level & time)
    assert res.file_num == 48


# Remove this test and the mark from below once min sunpy dep >=7.1
@pytest.mark.skipif(SUNPY_VERSION >= (7, 1), reason="Skip post sunpy 7.1")
@pytest.mark.remote_data
def test_distance_out_of_bounds_warning(recwarn):
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-27", "2023-04-28")
    level = a.Level(2)
    product = a.soar.Product("eui-fsi174-image")
    distance = a.soar.Distance(0.45 * u.AU, 1.2 * u.AU)
    # Run the search and ensure it raises an HTTPError
    with pytest.raises(HTTPError):
        Fido.search(distance & instrument & product & level & time)
    # Check if the warning was raised
    warnings_list = recwarn.list
    assert any(
        warning.message.args[0] == "Distance values must be within the range 0.28 AU to 1.0 AU."
        and issubclass(warning.category, SunpyUserWarning)
        for warning in warnings_list
    )


@pytest.mark.skipif(SUNPY_VERSION < (7, 1), reason="Skip pre sunpy 7.1")
@pytest.mark.remote_data
def test_distance_out_of_bounds_warning_post71(recwarn):
    instrument = a.Instrument("EUI")
    time = a.Time("2023-04-27", "2023-04-28")
    level = a.Level(2)
    product = a.soar.Product("eui-fsi174-image")
    distance = a.soar.Distance(0.45 * u.AU, 1.2 * u.AU)
    # Run the search and ensure it raises an HTTPError
    query = Fido.search(distance & instrument & product & level & time)
    # Check if the warning was raised
    assert query['soar'].errors
    # Check if the warning was raised
    warnings_list = recwarn.list
    assert any(
        warning.message.args[0] == "Distance values must be within the range 0.28 AU to 1.0 AU."
        and issubclass(warning.category, SunpyUserWarning)
        for warning in warnings_list
    )


# Remove this test and the mark from below once min sunpy dep >=7.1
@pytest.mark.skipif(SUNPY_VERSION >= (7, 1), reason="Skip post sunpy 7.1")
@responses.activate
def test_soar_server_down() -> None:
    # As the SOAR server is expected to be down in this test, a JSONDecodeError is expected
    # to be raised due to the absence of a valid JSON response.
    tap_endpoint = (
        "http://soar.esac.esa.int/soar-sl-tap/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=SELECT"
        " * FROM v_ll_data_item WHERE begin_time%3E='2020-11-13 00:00:00' AND "
        "begin_time%3C='2020-11-14 00:00:00' AND level='LL02' AND descriptor='mag'"
    )
    # We do not give any json data similar to the condition when the server is down.
    responses.add(responses.GET, tap_endpoint, body="Invalid JSON response", status=200)

    time = a.Time("2020-11-13", "2020-11-14")
    level = a.Level("LL02")
    product = a.soar.Product("mag")

    with pytest.raises(
        RuntimeError,
        match=r"The SOAR server returned an invalid JSON response. It may be down or not functioning correctly.",
    ):
        Fido.search(time, level, product)


@pytest.mark.skipif(SUNPY_VERSION < (7, 1), reason="Skip pre sunpy 7.1")
@responses.activate
def test_soar_server_down_post71() -> None:
    # As the SOAR server is expected to be down in this test, a JSONDecodeError is expected
    # to be raised due to the absence of a valid JSON response.
    tap_endpoint = (
        "http://soar.esac.esa.int/soar-sl-tap/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=SELECT"
        " * FROM v_ll_data_item WHERE begin_time%3E='2020-11-13 00:00:00' AND "
        "begin_time%3C='2020-11-14 00:00:00' AND level='LL02' AND descriptor='mag'"
    )
    # We do not give any json data similar to the condition when the server is down.
    responses.add(responses.GET, tap_endpoint, body="Invalid JSON response", status=200)

    time = a.Time("2020-11-13", "2020-11-14")
    level = a.Level("LL02")
    product = a.soar.Product("mag")

    query =  Fido.search(time, level, product)
    assert isinstance(query['soar'].errors, RuntimeError)
    assert ("The SOAR server returned an invalid JSON response. It may be down or not functioning correctly."
            == str(query['soar'].errors))


def test_can_handle_with_time_and_instrument():
    """Time + a known SOAR instrument should be handleable."""
    assert SOARClient._can_handle_query(a.Time("2023-01-01", "2023-01-02"), a.Instrument("EUI")) is True


def test_can_handle_with_distance_no_time():
    """Distance alone (no Time) should be handleable since Distance replaces Time as required."""
    assert SOARClient._can_handle_query(a.soar.Distance(0.3 * u.AU, 0.5 * u.AU)) is True


def test_can_handle_with_distance_and_time():
    """Distance + Time together should be handleable."""
    assert SOARClient._can_handle_query(
        a.soar.Distance(0.3 * u.AU, 0.5 * u.AU),
        a.Time("2023-01-01", "2023-01-02"),
    ) is True


def test_can_handle_wrong_provider():
    """A non-SOAR provider should be rejected."""
    assert SOARClient._can_handle_query(
        a.Time("2023-01-01", "2023-01-02"),
        a.Provider("SDAC"),
    ) is False


def test_can_handle_unknown_instrument():
    """An instrument not in the SOAR registry should be rejected."""
    assert SOARClient._can_handle_query(
        a.Time("2023-01-01", "2023-01-02"),
        a.Instrument("AIA"),
    ) is False


def test_can_handle_unsupported_attr():
    """An attr type not in the required/optional sets should be rejected."""
    assert SOARClient._can_handle_query(
        a.Time("2023-01-01", "2023-01-02"),
        a.Physobs("intensity"),
    ) is False


def test_can_handle_time_only():
    """Time with no instrument should be handleable (the no-instrument search path)."""
    assert SOARClient._can_handle_query(a.Time("2023-01-01", "2023-01-02")) is True
