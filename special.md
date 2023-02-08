# attack_pattern 没有 description 字段：
    -mobile-attack
        --attack-pattern
            ---attack-pattern--11bd699b-f2c2-4e48-bf46-fb3f8acd9799

```json
{
    "type": "bundle",
    "id": "bundle--b3a3feee-1681-47ba-acb6-b9cd37970e0a",
    "spec_version": "2.0",
    "objects": [
        {
            "x_mitre_domains": [
                "mobile-attack"
            ],
            "id": "attack-pattern--11bd699b-f2c2-4e48-bf46-fb3f8acd9799",
            "type": "attack-pattern",
            "created": "2017-10-25T14:48:30.462Z",
            "revoked": true,
            "external_references": [
                {
                    "source_name": "mitre-mobile-attack",
                    "url": "https://attack.mitre.org/techniques/T1425",
                    "external_id": "T1425"
                }
            ],
            "modified": "2018-10-17T01:05:10.699Z",
            "name": "Insecure Third-Party Libraries",
            "x_mitre_version": "1.0"
        }
    ]
}
```

# course_of_action(mitigation) 没有相关的 attack_pattern(technique)

enterprise:

```
course-of-action--fe0aeb41-1a51-4152-8467-628256ea6adf
```

# course_of_action(mitigation) 相关的 attack_pattern(technique)没有 use(description)

enterprise:

```
course-of-action--af093bc8-7b59-4e2a-9da8-8e839b4c50c6
```

混进了 technique:

```
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/mitigations/T1219",
                    "external_id": "T1219"
                }
            ],
```