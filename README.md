# Requirement

- 初始更新困难时建议科学上网，更新后不再需要
- `requirement.txt`

# Preparing

- 另外在 [Google Drive](https://drive.google.com/drive/folders/1e-rdHZCyjCW1VsrJu8dNkWWFELc7J9g1?usp=sharing) 下载 3 个过大的文件：`./prompt/model/en.model`, `./prompt/data/data_train.json`, `./prompt/data/vec_inuse.json`
- `pip install -r requirement.txt`
- Update: `python main.py -u`

# Usage

## Global ONE

```bash
usage: main.py [-h] [-u UPDATE] [-l LEMMA] [-a ATTACK] [-f FILE] [-t TEST] [-n NUMBER] [-p PROMPT]

Match Security Rules to Mitre ATT&CK.

optional arguments:
  -h, --help            show this help message and exit
  -u UPDATE, --update UPDATE
                        Download or Update data source.
  -l LEMMA, --lemma LEMMA
                        Extract lemma of words if True, else please choose False.
  -a ATTACK, --attack ATTACK
                        Tables that store processed data of Mitre ATT&CK. -(full) means use complete words instead of extracting lemma of words -(xxxStemmer) means
                        different tools used to extract lemma of words
  -f FILE, --file FILE  Match single security rule.
  -t TEST, --test TEST  Test all files in directory of input.
  -n NUMBER, --number NUMBER
                        The number is used as a baseline to determine whether the Security Rule passes the test,eg. tags in top 10 will be considered PASS the test.
  -p PROMPT, --prompt PROMPT
                        Prompt words to supply more accuracy description.
```

- Match: `python main.py [-f path]`
- Test: `python main.py [-t directory] [-n number]`
- Prompt: `python main.py [-p description]`

## Global TWO

`./tools/config.py`

```python
class Config:
    """
    Variables.
    """
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    URL: str = "https://github.com/mitre/cti.git"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/mitre_attack/data/cti/"

    SECURITY_RULES_PATH: str = BASE_DIR + "/security_rules/data/"

    EXTEND_STOP_WORD: list[str] = ["citation", "may", "e.g", "e.g.", "'s", "att", "ck", 'like', 'particular']

    # SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks']
    SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks', 'description']

    FILTER_PUNCTUATIONS: list[str] = [r"\\", r"//", r"~/", r"\~/", r"/\/", r"\\\\.\\", r"\\\\"]

    OUTPUT_CSV: str = BASE_DIR + "/mitre_attack/data/"

    STANFORD_POSTAGGER: str = BASE_DIR + "/tools/stanford-postagger-full-2020-11-17"

    STANFORD_POSTAGGER_JAR_PATH: str = STANFORD_POSTAGGER + "/stanford-postagger.jar"

    POS_TAGGER_PATH: str = STANFORD_POSTAGGER + "/models/english-bidirectional-distsim.tagger"

    MODE_en = "rsl" # Multi-channel Reverse Dictionary Model, four channels: basic, root-affix, sememe, lexname

    NUM_RESPONSE = 500

    GET_NUM = 500

    PROMPT_RESOURCE_PATH = BASE_DIR + "/prompt/resources/"
```

> *Note*
>
> - *SECURITY_RULES_PROP: match properties of Security Rules*
> - *GET_NUM: return number of prompt words*