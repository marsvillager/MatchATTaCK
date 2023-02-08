import os
import pandas as pd
import stix2
from stix2 import Filter, MemoryStore
from itertools import chain
from tools.relationshiphelpers import mitigation_mitigates_techniques


def format_data(srcs: list[MemoryStore], mitigation_dict: dict) -> pd.DataFrame:
    """
    function: format mitigation_mitigates_techniques
    :param srcs: stix2 data
    :param mitigation_dict: mitigation_mitigates_techniques
    :return: list of properties for matching
    """
    # course-of-action(mitigation) id, mitigation_id, mitigation_name, mitigation_description, attack_type,
    # attack id, relationship(, attack name, attack description)
    dict_all: list = []

    for mitigation in mitigation_dict:
        mitigation_list: list = mitigation_dict[mitigation]
        for item in mitigation_list:
            mitigation_list = get_mitigation_id(srcs, mitigation)
            dict_map: dict = {
                'id': mitigation,
                'mitigation_id': mitigation_list['external_references'][0]['external_id'],
                'mitigation_name': mitigation_list['name'],
                'mitigation_description': mitigation_list['description']
            }
            attack_object: dict = item['object']
            dict_map['attack_id'] = attack_object['external_references'][0]['external_id']
            dict_map['attack_type'] = attack_object['x_mitre_domains']

            relationship: dict = item['relationship']
            if 'description' in relationship:
                dict_map['relationship'] = relationship['description']
            else:
                dict_map['relationship'] = ''

            print(dict_map)
            dict_all.append(dict_map)

    df: pd.DataFrame = pd.DataFrame(dict_all)
    df.dropna(inplace=True)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    # show all columns
    # pd.set_option('display.max_rows', None)

    return df


def get_mitigation_id(srcs: list[MemoryStore], course_of_action: str) -> list:
    """
    function: get mitigation_id by id
    :param srcs: stix2 data
    :param course_of_action: id of course_of_action(mitigation)
    :return: mitigation_id
    """
    filter_objects: stix2.Filter = Filter('id', '=', course_of_action)

    return list(chain.from_iterable(src.query(filter_objects) for src in srcs))[0]


def mitigation_map_technique_list_out(srcs: list[MemoryStore]) -> None:
    """
    function: output classification of mitigation and relationship between mitigation and attack-pattern source data
    in the form of cvs
    :param srcs: stix2 data
    """
    mitigation_map_technique_dict: dict = mitigation_mitigates_techniques(srcs)
    mitigation_map_technique_list: pd.DataFrame = format_data(srcs, mitigation_map_technique_dict)

    if not os.path.exists('../csv_out'):
        os.mkdir('../csv_out')
    mitigation_map_technique_list.to_csv("../csv_out/mitigation_map_technique_list.csv", sep=',', index=False,
                                         header=True)
