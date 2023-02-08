from classification import attack_classification, mitigation_classification
import match
import pandas as pd
from stix2 import MemoryStore, Filter, CompositeDataSource

from classification.attack_classification import get_all_src
from tools.load_yml import load_file
from tools.relationshiphelpers import mitigation_mitigates_techniques, get_srcs

if __name__ == '__main__':
    # 0. update
    update = False
    # print("Update data or not?Please input yes or no")
    # if input() == 'yes':
    #     update = True

    """
    1. classification and format mitre att&ck source data
    """
    # ranges: pre/enterprise/mobile/ics
    techniques: list = attack_classification.classify_by_level1('enterprise')
    # column: id, type, attack_id, attack_name, attack_description
    attack_list: pd.DataFrame = attack_classification.format_by_level3(techniques)
    # print(attack_list)

    if update:
        srcs: list[MemoryStore] = get_srcs()
        mitigation_map_technique_dict: dict = mitigation_mitigates_techniques(srcs)
    #   column: id, mitigation_id, mitigation_name, mitigation_description, attack_id, attack_type, relationship(,
    #   attack name, attack description)
        mitigation_map_technique_list: pd.DataFrame = \
            mitigation_classification.format_data(srcs, mitigation_map_technique_dict)
    #   print(mitigation_map_technique_list)

    #   output data
        mitigation_classification.mitigation_map_technique_list_out(srcs)

    # read directly
    mitigation_list: pd.DataFrame = pd.read_csv("./csv_out/mitigation_map_technique_list.csv")
    # print(mitigation_list)
    # print(mitigation_list['relationship'])

    """
    2. read security rules
    """
    # key: dict = load_file("./security_rules/" + "00927_Account_Disabled_on_Windows.yml")
    # key: dict = load_file("./security_rules/" + "00928_Account_Enabled_on_Windows.yml")
    # key: dict = load_file("./security_rules/" + "00929_Privilege_Assigned_on_Windows.yml")
    # key: dict = load_file("./security_rules/" + "00930_Privilege_Removed_on_Windows.yml")
    # key: dict = load_file("./security_rules/" + "00931_Privilege_Use_on_Windows.yml")
    key: dict = load_file("./security_rules/" + "15022_LoginLogoutAtUnusualTime.yml")
    # print(key['category'])
    # print(key['description'])
    # print(key['name'])
    # print(key['remarks'])

    """
    3. match
    """
    # strategy(a) key2key and rank

    # additional stop words
    filer_list: list = ["(e.g.,"]
    stop_words_list: list[str] = match.get_stop_words("./resources/stop_en_words.txt") + filer_list

    default_list: list[str] = ['category', 'name', 'remarks', 'description']  # fields of security rules
    attack_match_list: list = match.attack_key2key(attack_list, key, default_list, stop_words_list)
    mitigation_match_list: list = match.mitigation_key2key(mitigation_list, key, default_list, stop_words_list)
    print(match.rank(attack_match_list))
    print(match.rank(mitigation_match_list))

    """
    4. assess
    """
    src: CompositeDataSource = get_all_src('./mitre_attack_data/cti')
    info: list = src.query([Filter("external_references.external_id", "=", "T1534")])[0]
    print(info['name'])
    print(info['description'])
