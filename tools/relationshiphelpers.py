import json
from itertools import chain
from stix2 import Filter
from tools import stixhelpers


def get_srcs():
    """memory shares without domain getter"""
    ms, srcs = stixhelpers.get_stix_memory_stores()

    return srcs


def query_all(srcs, filters):
    """Return the union of a query across multiple memorystores."""
    return list(chain.from_iterable(src.query(filters) for src in srcs))


def get_related(srcs, src_type, rel_type, target_type, reverse=False):
    """Build relationship mappings.
    params:
        srcs: memorystores for enterprise and mobile in an array
        src_type: source type for the relationships, e.g "attack-pattern"
        rel_type: relationship type for the relationships, e.g "uses"
        target_type: target type for the relationship, e.g "intrusion-set"
        reverse: build reverse mapping of target to source
    """

    relationships = query_all(
        srcs,
        [
            Filter("type", "=", "relationship"),
            Filter("relationship_type", "=", rel_type),
            Filter("revoked", "=", False),
        ],
    )

    # stix_id => [ ids of objects with relationships with stix_id ]
    id_to_related = {}

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
            targets = query_all(srcs, [Filter("type", "=", target_type)])
        else:
            targets = query_all(srcs, [Filter("type", "=", target_type), Filter("revoked", "=", False)])
    else:
        if src_type.startswith("x-mitre"):
            targets = query_all(srcs, [Filter("type", "=", src_type)])
        else:
            targets = query_all(srcs, [Filter("type", "=", src_type), Filter("revoked", "=", False)])

    id_to_target = {}
    # build the dict
    for target in targets:
        if target.get("id"):
            id_to_target[target["id"]] = target

    output = {}
    for stix_id in id_to_related:
        value = []
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


# technique:mitigation
def mitigation_mitigates_techniques(srcs):
    """Return mitigation_id => {technique, relationship} for each technique mitigated by the mitigation.
    srcs should be an array of memorystores for enterprise, mobile, and pre
    """
    return get_related(srcs, "course-of-action", "mitigates", "attack-pattern", reverse=False)
