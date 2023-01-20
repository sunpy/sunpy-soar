import json
import pathlib

from astroquery.utils.tap.core import TapPlus


def get_all_instruments():
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
    attr_file = pathlib.Path(__file__).parent.parent / 'sunpy_soar' / 'data' / 'instrument_attrs.json'
    descriptors = get_all_instruments()
    with open(attr_file, 'w') as attrs_file:
        json.dump(dict(sorted(descriptors.items())), attrs_file, indent=2)
