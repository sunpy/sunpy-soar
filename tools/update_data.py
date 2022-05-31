import json
import pathlib

from astroquery.utils.tap.core import TapPlus


def get_all_descriptors():
    soar = TapPlus('http://soar.esac.esa.int/soar-sl-tap/tap')
    job = soar.launch_job('select * from soar.cdf_dataset')
    res = job.get_results()
    descriptors = {}
    for row in res:
        desc = row['cdf_descriptor'].split('>')[0].upper()
        descriptors[desc] = row['logical_source_description']
    return descriptors


if __name__ == '__main__':
    attr_file = pathlib.Path(__file__).parent.parent / 'sunpy_soar' / 'data' / 'attrs.json'
    descriptors = get_all_descriptors()
    with open(attr_file, 'w') as attrs_file:
        json.dump(dict(sorted(descriptors.items())), attrs_file, indent=2)
