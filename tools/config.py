import os


class Config:
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    SECURITY_RULES_PATH: str = BASE_DIR + "/data/security_rules/"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/data/mitre_attack/cti/"

    VECTOR_SIZE = 100

    OUTPUT_CLASSIFICATION_CSV: str = BASE_DIR + "/data/mitre_attack/processed_data/classification_data/"

    OUTPUT_TRANSFORM_TXT: str = BASE_DIR + "/data/mitre_attack/processed_data/transform_data/"

    OUTPUT_WORD_FREQ: str = BASE_DIR + "/data/mitre_attack/processed_data/others/word_freq.txt"

    OUTPUT_WORD_CLOUD_PIC = BASE_DIR + "/data/mitre_attack/processed_data/others/word_cloud.png"

    OUTPUT_WORD2VEC_MODULE: str = BASE_DIR + "/data/mitre_attack/processed_data/others/word2vec.w2v"

    URL: str = "https://github.com/mitre/cti.git"

    SCENE: dict = {"enterprise": "enterprise-attack",
                   "ics": "ics-attack",
                   "mobile": "mobile-attack"}

    COMPARISON_TABLE: dict = {"attack-pattern": "technique",
                              "course-of-action": "mitigation",
                              "intrusion-set": "group",
                              "malware": "software",
                              "tool": "software",
                              "x-mitre-matrix": "matrix",
                              "x-mitre-tactic": "tactic",
                              "x-mitre-data-source": "data_source"}

    EXTEND_STOP_WORD: list[str] = ["citation", "may", "e.g.", "'s", "att", "ck", 'like']

    SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks']
    # SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks', 'description']

    FILTER_PUNCTUATIONS: list[str] = [',', '.', ':', ';', '?', '(', ')', '[', ']', '!', '*', '@', '#', '$', '%', '`',
                                      '&', '``', "''", '{', '}', '“', '”', '-', '’', '‘', "'", '/', '<', '>', '--',
                                      '~/', '|', '_', '..', '\\', '\\\\', '=', '+', '-']
