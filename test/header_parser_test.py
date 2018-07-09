from resources.config_provider import get_config_default
from generate_trainset.extract_header_values import parse_xml_header
import os


def test_header_parser():
    config_training = get_config_default()
    xml_path = config_training["xml_unittest_file"]
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/" + xml_path
    print(dir_path)
    header_content = parse_xml_header(path=xml_path)
    assert len(header_content) == 1
    assert header_content['CA-aix-en-provence-20130208-1022871-jurica']['defendeur_fullname'] == ['Catherine ***REMOVED***']