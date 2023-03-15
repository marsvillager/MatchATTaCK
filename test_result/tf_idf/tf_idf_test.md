分词：`WordPunctTokenizer`

词干提取：

```
PorterStemmer, LancasterStemmer, SnowballStemmer
```

词性提取：`stanford`

注：

```python
description:
    （1）evaluation
        if 'description' not in pairs or pairs['tags'] is None or pairs['tags'] == '':
        # if pairs['tags'] is None or pairs['tags'] == '':
    （2）config
        SECURITY_RULES_PROP: list[str] = ['category', 'name', 'remarks', 'description']

lemma:
    （1）main
format_list: pd.DataFrame = pd.read_csv(Config.OUTPUT_CSV + "mitre_data(LancasterStemmer).csv")
	（2）main
        test_all(Config.SECURITY_RULES_PATH + "/fy22_deliverable/rules/", format_list, 10, True)
    （3）transform
        cut_word.append(LancasterStemmer().stem(word))
```

# LancasterStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

# PorterStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

# SnowballStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

# 对比

## description

|                   |  Regular  | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :---------------: | :-------: | :--------------: | :-----------: | :-------------: |
|   **fy22(53)**    |   0.302   |      0.283       |   **0.321**   |    **0.321**    |
|    **fy23(1)**    |     0     |        0         |       0       |        0        |
| **osa_rules(46)** | **0.326** |      0.261       |     0.261     |      0.261      |

## no description

|                    | Regular | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :----------------: | :-----: | :--------------: | :-----------: | :-------------: |
|    **fy22(53)**    |  0.340  |    **0.340**     |   **0.340**   |    **0.340**    |
|    **fy23(1)**     |    0    |        0         |       0       |        0        |
| **osa_rules(140)** |  0.386  |       0.4        |   **0.407**   |    **0.407**    |

