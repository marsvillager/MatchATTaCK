import glob
import sys

from stix2 import Filter
from package import get_data, datacomponents_detecting_technique
from security_rules.process.process_data import load_file
from tools.config import Config


def test_deprecated_id(filedir: str) -> None:
    """
    Test if deprecated id in security rules.

    :param filedir: directory of security rules
    :return: warning
    """
    with open(Config.DEPRECATED_LIST) as f:
        deprecated_list: str = f.read()

    id_file: str = filedir + '*.yml'
    for file in glob.glob(id_file):
        print(file)

        pairs: dict = load_file(file)

        if pairs['tags'] is None or pairs['tags'] == '':
            print("未打标\n")
            continue

        tag_list: list = [".".join(tag.split('.')[2:]) for tag in pairs['tags'] if 'attack' in tag and 'T' in tag]
        if len(tag_list) == 0:
            print("未打标\n")
            continue

        print("tags of security rules: " + ", ".join(tag_list) + "\n")

        for tag in tag_list:
            if tag in deprecated_list:
                sys.exit('Error: Use deprecated attack-pattern ' + tag + '.')


if __name__ == '__main__':
    # test_deprecated_id(Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/")
    # test_deprecated_id(Config.SECURITY_RULES_PATH + "/fy23_deliverable/rules/")
    # test_deprecated_id(Config.SECURITY_RULES_PATH + "/osa_rules/")

    techniques: list = get_data(Filter("type", "=", "attack-pattern"))
    techniques_map_datacomponent_dict: dict = datacomponents_detecting_technique()

    search_id: str = 'T1546.016'  # 根据 id 查询单条 mitre att&ck

    for technique in techniques:
        # if 'x_mitre_deprecated' in technique and technique['x_mitre_deprecated'] is True:
        #     print(technique["external_references"][0]["external_id"])

        if technique["external_references"][0]["external_id"] == search_id:
            print("name: \n" + technique["name"] + "\n")

            if 'description' in technique:
                print("description: \n" + technique["description"] + "\n")

            print("detects: ")
            if 'x_mitre_data_sources' in technique:
                detect_list: list = techniques_map_datacomponent_dict[technique["id"]]
                for item in detect_list:
                    print(item['relationship']['description'])

