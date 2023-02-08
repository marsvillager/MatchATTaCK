import _io
import yaml


def load_file(filename: str) -> dict:
    """
    function: load yaml
    :param filename: yaml
    :return: file contents
    """
    f: _io.TextIOWrapper = open(filename, 'r', encoding='utf-8')
    file: str = f.read()
    key: dict = yaml.safe_load(file)
    return key
