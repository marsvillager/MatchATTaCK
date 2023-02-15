import os


class Config:
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    URL: str = "https://github.com/mitre/cti.git"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/mitre_attack/data/cti/"

    SECURITY_RULES_PATH: str = BASE_DIR + "/security_rules/data/"

    EXTEND_STOP_WORD: list[str] = ["citation", "may", "e.g", "e.g.", "'s", "att", "ck", 'like', 'particular']

    SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks']
    # SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks', 'description']

    FILTER_PUNCTUATIONS: list[str] = [r"\\", r"//", r"~/", r"\~/", r"/\/", r"\\\\.\\", r"\\\\"]

    OUTPUT_CSV: str = BASE_DIR + "/mitre_attack/data/"

    STANFORD_POSTAGGER: str = BASE_DIR + "/tools/stanford-postagger-full-2020-11-17"

    STANFORD_POSTAGGER_JAR_PATH: str = STANFORD_POSTAGGER + "/stanford-postagger.jar"

    POS_TAGGER_PATH: str = STANFORD_POSTAGGER + "/models/english-bidirectional-distsim.tagger"
