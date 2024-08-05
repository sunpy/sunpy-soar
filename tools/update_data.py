import json
import pathlib

from astroquery.utils.tap.core import TapPlus

soar = TapPlus(url="http://soar.esac.esa.int/soar-sl-tap/tap")


def get_cdf_descriptors():
    # Get data descriptors for CDF files
    print("Updating CDF descriptors...")
    job = soar.launch_job("select * from soar.cdf_dataset")
    res = job.get_results()
    descriptors = {}
    for row in res:
        desc = row["logical_source"].split("_")[-1]
        descriptors[desc] = row["logical_source_description"]
    return descriptors


def get_fits_descriptors():
    # Get data descriptors for FITS files
    print("Updating FITS descriptors...")
    soar = TapPlus(url="http://soar.esac.esa.int/soar-sl-tap/tap")
    job = soar.launch_job("select * from soar.fits_dataset")
    res = job.get_results()
    descriptors = {}
    for row in res:
        desc = row["logical_source"].split("_")[-1]
        # Currently no way to get a description from the FITS table
        descriptors[desc] = ""
    return descriptors


def get_all_descriptors():
    desc = get_cdf_descriptors()
    desc.update(get_fits_descriptors())
    return desc


def get_all_instruments():
    # Get the unique instrument names
    SOAR = TapPlus(url="http://soar.esac.esa.int/soar-sl-tap/tap")
    job = SOAR.launch_job("select * from soar.instrument")
    res = job.get_results()

    instruments = [
        "EPD",
        "EUI",
        "MAG",
        "METIS",
        "PHI",
        "RPW",
        "SOLOHI",
        "SPICE",
        "STIX",
        "SWA",
    ]
    instr_desc = {}
    for r in res:
        if r["name"] not in instruments:
            pass
        else:
            instr_desc[r["name"]] = r["long_name"]
    return instr_desc


def get_all_soops():
    # Get the unique soop names
    print("Updating SOOP descriptors...")
    SOAR = TapPlus(url="http://soar.esac.esa.int/soar-sl-tap/tap")
    job = SOAR.launch_job("select * from soar.soop")
    res = job.get_results()

    soop_names = {}
    for row in res:
        soop_names[row["soop_name"]] = ""

    return soop_names


def get_observation_modes():
    # Fetch observation modes for all instruments combined
    print("Updating observation modes...")
    obs_modes = {}
    instruments = [
        "eui", "phi", "shi", "spi", "met"
    ]

    # Set to hold unique observation modes
    unique_modes = set()

    for instrument in instruments:
        query = f"SELECT DISTINCT observation_mode FROM v_{instrument}_sc_fits"
        job = soar.launch_job(query)
        res = job.get_results()
        for row in res:
            mode = row['observation_mode'].strip()  # Strip leading and trailing whitespace
            if mode:  # Ensure mode is not an empty string
                unique_modes.add(mode)

    # Convert the set to a sorted list and create a dictionary
    obs_modes = {mode: "" for mode in sorted(unique_modes)}

    return obs_modes

if __name__ == "__main__":
    attr_file = (
        pathlib.Path(__file__).parent.parent / "sunpy_soar" / "data" / "attrs.json"
    )
    descriptors = get_all_descriptors()
    with attr_file.open("w") as attrs_file:
        json.dump(dict(sorted(descriptors.items())), attrs_file, indent=2)

    instr_file = (
        pathlib.Path(__file__).parent.parent
        / "sunpy_soar"
        / "data"
        / "instrument_attrs.json"
    )
    instr_descriptors = get_all_instruments()
    with instr_file.open("w") as instrs_file:
        json.dump(dict(sorted(instr_descriptors.items())), instrs_file, indent=2)

    soop_file = (
        pathlib.Path(__file__).parent.parent / "sunpy_soar" / "data" / "soop_attrs.json"
    )
    soop_descriptors = get_all_soops()
    with soop_file.open("w") as soops_file:
        json.dump(dict(sorted(soop_descriptors.items())), soops_file, indent=2)

    obs_modes_file = (
        pathlib.Path(__file__).parent.parent / "sunpy_soar" / "data" / "observation_attrs.json"
    )
    observation_modes = get_observation_modes()
    with obs_modes_file.open("w") as obs_file:
        json.dump(observation_modes, obs_file, indent=2)
