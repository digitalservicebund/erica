import os
samples_folder = os.path.join(os.path.dirname(__file__), 'erica_legacy/samples')


def read_text_from_sample(sample_name, read_type='r'):
    with open(os.path.join(samples_folder, sample_name), read_type) as sample_xml:
        return sample_xml.read()