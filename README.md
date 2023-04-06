# Requirement

- 初始更新困难时建议科学上网，更新后不再需要
- 所需软件包在 `requirement.txt` 文件中

# Preparing

- 去除拉取 mitre att&ck 数据时的 VCS root mapping（PyCharm ==> Settings ==> Version Control ==> Directory Mappings）or `./idea/vcs.xml` 中去除不相关的 `<mapping>` 标签
- 需另外在 [Google Drive](https://drive.google.com/drive/folders/1e-rdHZCyjCW1VsrJu8dNkWWFELc7J9g1?usp=sharing) 下载 3 个过大的文件：`./prompt/model/en.model`, `./prompt/data/data_train.json`, `./prompt/data/vec_inuse.json`
- `pip install -r requirement.txt`
- Update: `python main.py -u`

# Usage

## Global ONE

```bash
usage: main.py [-h] [-u] [-l LEMMA] [-a ATTACK] [-s SEARCH_ENGINE] [-sn SEARCH_ENGINE_NUMBER] [-st SEARCH_ENGINE_TEST] [-stn SEARCH_ENGINE_TEST_NUMBER] [-d DOC2VEC]
               [-dn DOC2VEC_NUMBER] [-dt DOC2VEC_TEST] [-dtm DOC2VEC_TEST_MODEL] [-dtn DOC2VEC_TEST_NUMBER] [-p PROMPT]

Match Security Rules to Mitre ATT&CK.

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          Download or Update data source.
  -l LEMMA, --lemma LEMMA
                        Extract lemma of words if True, else please choose False.
  -a ATTACK, --attack ATTACK
                        Tables that store processed data of Mitre ATT&CK. -(full) means use complete words instead of extracting lemma of words -(xxxStemmer) means
                        different tools used to extract lemma of words
  -s SEARCH_ENGINE, --search_engine SEARCH_ENGINE
                        Match single security rule by search_engine.
  -sn SEARCH_ENGINE_NUMBER, --search_engine_number SEARCH_ENGINE_NUMBER
                        Show the first few results ranked depends on search_engine.
  -st SEARCH_ENGINE_TEST, --search_engine_test SEARCH_ENGINE_TEST
                        Test all files in directory of input.
  -stn SEARCH_ENGINE_TEST_NUMBER, --search_engine_test_number SEARCH_ENGINE_TEST_NUMBER
                        The number is used as a baseline to determine whether the Security Rule passes the test,eg. tags in top 10 will be considered PASS the test.
  -d DOC2VEC, --doc2vec DOC2VEC
                        Match single security rule by Doc2Vec.
  -dn DOC2VEC_NUMBER, --doc2vec_number DOC2VEC_NUMBER
                        Show the first few results ranked depends on doc2vec.
  -dt DOC2VEC_TEST, --doc2vec_test DOC2VEC_TEST
                        Test all files in directory of input.
  -dtm DOC2VEC_TEST_MODEL, --doc2vec_test_model DOC2VEC_TEST_MODEL
                        Choose one model to test.
  -dtn DOC2VEC_TEST_NUMBER, --doc2vec_test_number DOC2VEC_TEST_NUMBER
                        The number is used as a baseline to determine whether the Security Rule passes the test,eg. tags in top 10 will be considered PASS the test.
  -p PROMPT, --prompt PROMPT
                        Prompt words to supply more accuracy description.
```

- **Match**
  
  - *search engine*   `python main.py [-s path] [-sn number]` 

    ![image-20230317093758063](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230406093846172.png)
  
  - *Doc2vec*   `python main.py [-d path] [-dn number]` 
  
    ![image-20230317093832954](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230317093832954.png)
  
- **Test**
  - *search engine*  `python main.py [-st directory] [-stn number]`
  
    ![image-20230317093847609](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230406095810451.png)
  - *Doc2vec*   `python main.py [-dt directory] [-dtn number] [-dtm model]`
  
    ![image-20230317093912052](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230317093912052.png))
  
- **Prompt**  `python main.py [-p description]`

  ![image-20230317093944986](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230317093944986.png)

## Global TWO

`./tools/config.py`

```python
import os


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

    MODE_en = "rsl"  # Multi-channel Reverse Dictionary Model, four channels: basic, root-affix, sememe, lexname

    NUM_RESPONSE = 500

    GET_NUM = 500

    ADJUST_TF = 70

    PROMPT_RESOURCE_PATH = BASE_DIR + "/prompt/resources/"

    # score = x * (TF(a, w) \ IDF(a)) + y * link, x + y = 1
    SCORE = 0.95
```

> *Note*
>
> - *SECURITY_RULES_PROP: match properties of Security Rules*
> - *GET_NUM: return number of prompt words*
> - *ADJUST_TF: limit total words of a certain attack pattern*
> - *SCORE: proportion of tf-idf in search engine formular*

# Theory

## Search Engine

$$
\begin{align*}
& score_i = x \times \sum_{j=0}^N (TF(a_i, w_j) \times IDF(w_j)) + y \times link[i], \  \  x + y = 1 \\ \\
& TF(a_i,w_j)=\frac{count(a_i,w_j)}{limit(count(a_i,*))} \\
& - count(a_i, w_j)：单词 \ w_j \ 在攻击手段 \ a_i \ 中出现的次数 \\
& - count(a_i, *)：攻击手段 \ a_i \ 的总词数 \\
& - limit：总词数小于某阈值时将强制调节为该阈值 \\
& IDF(a_i)=log\frac{N+1}{N(w_j)+1} + 1 \\
& - N：攻击手段总数 \\
& - N(w_j)：单词 \ w_j \ 出现在多少种攻击手段中 \\
& ⚠️ \ limit \ 经测试阈值定在 \ 60 ～ 80 \ 之间 \\ \\

& for \ k \ in \ max\_iter: \\
& \ \ \ \ new\_link[i] = \frac{(1 - d)}{N} + d * \sum_{j=0}^N\frac{link[j]}{out\_degree[j]}, out\_degree[out\_degree == 0] \ += \ 1 \\
& \ \ \ \ if \ new\_link[i] - link[i]  < tol: \\
& \ \ \ \ \ \ \ \ break \\
& \ \ \ \ link[i] = new\_link[i] \\
& - out\_degree[j]：攻击手段 \ a_j \ 的出链, 当出链为 \ 0 \ 时对分母进行加一平滑 \\
& - d：增加指向其它节点的概率, 作为阻尼系统，通常被设置为 \ 0.85 \\
& - max\_iter：最大迭代次数 \\
& - tol：tolerance, 迭代算法的认为收敛的数值, 通常被设置为 \ 1e-6

\end{align*}
$$

# Process Mitre Data(optional)

**Processed cvs files locate in `./mitre_attack/data/`**:

- no lemma
  - mitre_data(full).csv
- lemma
  - mitre_data(LancasterStemmer).csv
  - mitre_data(PorterStemmer).csv
  - mitre_data(SnowballStemmer).csv

If you want to use this code to archieve self-defined data, more preparatory work will be necessary:

- **java** environment

- **postagger tools** 

  - usage: [nltk和stanford nlp](https://blog.csdn.net/lizzy05/article/details/88148097)
  - download from website [The Stanford Natural Language Processing Group](https://nlp.stanford.edu/software/tagger.html)
  - or `wget https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip`

- **memory** problem

  - warning: `Exception in thread "main" java.lang.OutOfMemoryError: Java heap space`

    - ```python
          # \nltk\tag\stanford.py
          def __init__(
              self,
              model_filename,
              path_to_jar=None,
              encoding="utf8",
              verbose=False,
              java_options="-mx1000m",
          ):
      ```

  - change java_options in the way of pass arument

    - ```python
      st = StanfordPOSTagger(Config.POS_TAGGER_PATH, path_to_jar=Config.STANFORD_POSTAGGER_JAR_PATH, java_options="-Xmx8G")
      ```

