import json
import pandas as pd
import stix2

from stix2 import FileSystemSource, CompositeDataSource, Filter
from tools.config import Config
from tools.transform import is_lemma


def get_data(filter_list: list[stix2.Filter]) -> list:
    """
    Extract data depends on stix2.

    :param filter_list: filter by classification
    :return: techniques of stix2
    """
    enterprise_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH +
                                                                     "enterprise-attack")
    mobile_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH + "mobile-attack")
    ics_attack_src: stix2.FileSystemSource = FileSystemSource(Config.MITRE_ATTACK_DATA_PATH + "ics-attack")

    src = CompositeDataSource()
    src.add_data_sources([enterprise_attack_src, mobile_attack_src, ics_attack_src])

    return src.query(filter_list)


def format_data(lemma: bool) -> pd.DataFrame:
    """
    Extract technique data which is key to process then match.

    :return: key data
    """
    techniques: list = get_data(Filter("type", "=", "attack-pattern"))
    techniques_map_datacomponent_dict: dict = datacomponents_detecting_technique()

    format_list: list = []
    for technique in techniques:
        name: set[str] = is_lemma(technique["name"], lemma)

        description: str = ''
        if 'description' in technique:
            description: set[str] = is_lemma(technique["description"], lemma)

        detects: str = ''
        if 'x_mitre_data_sources' in technique:
            detect_list: list = techniques_map_datacomponent_dict[technique["id"]]
            for item in detect_list:
                detects = detects + ' ' + item['relationship']['description']
            detects: set[str] = is_lemma(detects, lemma)

        format_dict: dict[str, str] = {"id": technique["external_references"][0]["external_id"],
                                       "name": ' '.join(name),
                                       "description": ' '.join(description),
                                       "detects": ' '.join(detects)}

        format_list.append(format_dict)

    # show all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('expand_frame_repr', False)

    return pd.DataFrame(format_list)


def get_related(src_type: str, rel_type: str, target_type: str, reverse=False) -> dict:
    """
    Build relationship mappings.

    :param src_type: source type for the relationships, e.g "attack-pattern"
    :param rel_type: relationship type for the relationships, e.g "uses"
    :param target_type: target type for the relationship, e.g "intrusion-set"
    :param reverse: build reverse mapping of target to source
    """

    relationships = get_data([
            Filter("type", "=", "relationship"),
            Filter("relationship_type", "=", rel_type),
            Filter("revoked", "=", False)
    ])

    # stix_id => [ ids of objects with relationships with stix_id ]
    id_to_related: dict = {}

    # build the dict
    for relationship in relationships:
        if relationship.get("x_mitre_deprecated"):
            continue

        if src_type in relationship.source_ref and target_type in relationship.target_ref:
            if (relationship.source_ref in id_to_related and not reverse) or (
                relationship.target_ref in id_to_related and reverse
            ):
                if not reverse:
                    id_to_related[relationship.source_ref].append(
                        {"relationship": relationship, "id": relationship.target_ref}
                    )
                else:
                    id_to_related[relationship.target_ref].append(
                        {"relationship": relationship, "id": relationship.source_ref}
                    )
            else:
                if not reverse:
                    id_to_related[relationship.source_ref] = [
                        {"relationship": relationship, "id": relationship.target_ref}
                    ]
                else:
                    id_to_related[relationship.target_ref] = [
                        {"relationship": relationship, "id": relationship.source_ref}
                    ]
    # all objects of target type
    if not reverse:
        if target_type.startswith("x-mitre"):
            targets = get_data([Filter("type", "=", target_type)])
        else:
            targets = get_data([Filter("type", "=", target_type), Filter("revoked", "=", False)])
    else:
        if src_type.startswith("x-mitre"):
            targets = get_data([Filter("type", "=", src_type)])
        else:
            targets = get_data([Filter("type", "=", src_type), Filter("revoked", "=", False)])

    id_to_target: dict = {}
    # build the dict
    for target in targets:
        if target.get("id"):
            id_to_target[target["id"]] = target

    output: dict = {}
    for stix_id in id_to_related:
        value: list = []
        for related in id_to_related[stix_id]:
            if not related["id"] in id_to_target:
                continue  # targetting a revoked object

            if related["id"].startswith("x-mitre"):
                value.append(
                    {
                        "object": id_to_target[related["id"]],
                        "relationship": json.loads(related["relationship"].serialize()),
                    }
                )
            else:
                value.append(
                    {
                        "object": json.loads(id_to_target[related["id"]].serialize()),
                        "relationship": json.loads(related["relationship"].serialize()),
                    }
                )
        output[stix_id] = value
    return output


def datacomponents_detecting_technique():
    """
    Return technique => {data component, relationship} for each data component decting a technique.
    """
    return get_related("x-mitre-data-component", "detects", "attack-pattern", reverse=True)
