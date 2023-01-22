import json
import pathlib

from astroquery.utils.tap.core import TapPlus

soar = TapPlus('http://soar.esac.esa.int/soar-sl-tap/tap')


def get_cdf_descriptors():
    # Get data descriptors for CDF files
    print("Updating CDF descriptors...")
    job = soar.launch_job('select * from soar.cdf_dataset')
    res = job.get_results()
    descriptors = {}
    for row in res:
        desc = row['logical_source'].split('_')[-1].upper()
        descriptors[desc] = row['logical_source_description']
    return descriptors


def get_fits_descriptors():
    # Get data descriptors for FITS files
    print("Updating FITS descriptors...")
    soar = TapPlus('http://soar.esac.esa.int/soar-sl-tap/tap')
    job = soar.launch_job('select * from soar.fits_dataset')
    res = job.get_results()
    descriptors = {}
    for row in res:
        desc = row['logical_source'].split('_')[-1].upper()
        # Currently no way to get a description from the FITS table
        descriptors[desc] = ''
    return descriptors


def get_all_descriptors():
    desc = get_cdf_descriptors()
    desc.update(get_fits_descriptors())
    return desc


def get_all_instruments():
    # Get the unique instrument names
    SOAR = TapPlus(url="http://soar.esac.esa.int/soar-sl-tap/tap")
    job = SOAR.launch_job('select * from soar.instrument')
    res = job.get_results()

    instruments = ['EPD', 'EUI', 'MAG', 'METIS', 'PHI', 'RPW',
                   'SOLOHI', 'SPICE', 'STIX', 'SWA']
    instr_desc = {}
    for r in res:
        if r["name"] not in instruments:
            pass
        else:
            instr_desc[r["name"]] = r["long_name"]
    return instr_desc


if __name__ == '__main__':
    attr_file = pathlib.Path(__file__).parent.parent / 'sunpy_soar' / 'data' / 'attrs.json'
    descriptors = get_all_descriptors()
    with open(attr_file, 'w') as attrs_file:
        json.dump(dict(sorted(descriptors.items())), attrs_file, indent=2)

    instr_file = pathlib.Path(__file__).parent.parent / 'sunpy_soar' / 'data' / 'instrument_attrs.json'
    instr_descriptors = get_all_instruments()
    with open(instr_file, 'w') as instrs_file:
        json.dump(dict(sorted(instr_descriptors.items())), instrs_file, indent=2)
