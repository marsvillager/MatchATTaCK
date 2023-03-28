# 预处理

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
				parser.add_argument('-a', '--attack', action='store', default=Config.OUTPUT_CSV + "mitre_data(PorterStemmer).csv", help='Tables that store processed data of Mitre ATT&CK. \n'
'-(full) means use complete words instead of extracting lemma of words \n'
'-(xxxStemmer) means different tools used to extract lemma of words')
	  （2）main
        parser.add_argument('-l', '--lemma', action='store', default=True, help='Extract lemma of words if True, else please choose False.')
    （3）transform
        cut_word.append(LancasterStemmer().stem(word))
```

## LancasterStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

## PorterStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

## SnowballStemmer

|           | no description | description |
| :-------: | :------------: | :---------: |
| osa_rules |       √        |      √      |
|   fy22    |       √        |      √      |
|   fy23    |       √        |      √      |

# 算法

![image-20230321100215064](https://github.com/marsvillager/pictures_for_markdown/raw/main/tf_idf.png)

# 调参

## before

![image-20230317093758063](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230317093758063.png)

## 分析

各攻击手段之间的总词数差距过大

![image-20230321095803795](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230321095803795.png)

## 词数分布

![image-20230322111455640](https://github.com/marsvillager/pictures_for_markdown/raw/main/image-20230322111455640.png)

# 对比

## origin(top10)

### description

|                   |  Regular  | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :---------------: | :-------: | :--------------: | :-----------: | :-------------: |
|   **fy22(53)**    |   0.302   |      0.283       |   **0.321**   |    **0.321**    |
|    **fy23(1)**    |     0     |        0         |       0       |        0        |
| **osa_rules(46)** | **0.326** |      0.261       |     0.261     |      0.261      |

### no description

|                    | Regular | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :----------------: | :-----: | :--------------: | :-----------: | :-------------: |
|    **fy22(53)**    |  0.340  |    **0.340**     |   **0.340**   |    **0.340**    |
|    **fy23(1)**     |    0    |        0         |       0       |        0        |
| **osa_rules(140)** |  0.386  |       0.4        |   **0.407**   |    **0.407**    |

## fix(top10)

### description

|                   |  Regular  | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :---------------: | :-------: | :--------------: | :-----------: | :-------------: |
|   **fy22(53)**    |   0.283   |      0.283       |   **0.321**   |    **0.321**    |
|    **fy23(1)**    |     0     |        0         |       0       |        0        |
| **osa_rules(46)** | **0.283** |      0.239       |     0.261     |      0.261      |

### no description

|                    | Regular | LancasterStemmer | PorterStemmer | SnowballStemmer |
| :----------------: | :-----: | :--------------: | :-----------: | :-------------: |
|    **fy22(53)**    |  0.340  |      0.321       |   **0.340**   |    **0.340**    |
|    **fy23(1)**     |    0    |        0         |       0       |        0        |
| **osa_rules(140)** |  0.364  |      0.379       |    **0.4**    |     **0.4**     |

## filter

PorterStemmer

|  lemma with desc  | no filter | filter < 10 | filter < 20 | filter < 30 | filter < 40 | filter < 50 | filter < 60 | filter < 70 | filter < 80 | remove |
| :---------------: | :-------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :----: |
|   **fy22(53)**    |   0.321   |    0.321    |    0.358    |    0.358    |  **0.377**  |  **0.377**  |    0.358    |  **0.377**  |    0.358    | 0.283  |
|    **fy23(1)**    |     0     |      0      |      0      |      0      |      0      |             |             |             |             |        |
| **osa_rules(46)** |   0.261   |    0.326    |    0.348    |    0.391    |    0.457    |    0.457    |  **0.522**  |    0.478    |    0.478    | 0.348  |

PorterStemmer

|  lemma & no desc   | no filter | filter < 10 | filter < 20 | filter < 30 | filter < 40 | filter < 50 | filter < 60 | filter < 70 | filter < 80 |  remove   |
| :----------------: | :-------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | ----------- | :-------: |
|    **fy22(53)**    |   0.340   |    0.340    |    0.340    |     0.4     |    0.434    |    0.472    |    0.472    |    0.453    | 0.453       | **0.491** |
|    **fy23(1)**     |           |             |             |             |             |             |             |             |             |           |
| **osa_rules(140)** |    0.4    |     0.4     |    0.414    |    0.429    |    0.471    |     0.5     |    0.507    |  **0.536**  | 0.514       |   0.514   |

# Results(top20)

PorterStemmer

|  lemma with desc  | no filter | filter < 10 | filter < 20 | filter < 30 | filter < 40 | filter < 50 | filter < 60 | filter < 70 | filter < 80 | remove |
| :---------------: | :-------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :----: |
|   **fy22(53)**    |   0.377   |    0.377    |    0.377    |    0.377    |    0.415    |    0.509    |  **0.528**  |    0.509    |    0.453    | 0.472  |
|    **fy23(1)**    |           |             |             |             |             |             |             |             |             |        |
| **osa_rules(46)** |   0.522   |    0.522    |    0.543    |    0.565    |    0.609    |    0.609    |  **0.630**  |    0.609    |    0.543    | 0.457  |

PorterStemmer

|  lemma & no desc   | no filter | filter < 10 | filter < 20 | filter < 30 | filter < 40 | filter < 50 | filter < 60 | filter < 70 | filter < 80 |  remove   |
| :----------------: | :-------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | ----------- | :-------: |
|    **fy22(53)**    |   0.453   |    0.453    |    0.491    |    0.509    |    0.566    |    0.566    |    0.566    |  **0.642**  | **0.642**   |   0.623   |
|    **fy23(1)**     |           |             |             |             |             |             |             |             |             |           |
| **osa_rules(140)** |   0.529   |    0.529    |    0.543    |    0.550    |    0.579    |    0.579    |    0.586    |    0.621    | 0.614       | **0.643** |

# 增加权重操作

以 `./security_rules/data/fy23_deliverable/rules/15694_ApplicationInstallationLinuxRedHat.yml` 为例

标记为 `tags: [attack.enterprise.T1543]`

实际排名 `T1546.016`  以 `[linux, instal, applic]` 位列第一，而这一条中直接引用了 `T1543`，因此考虑<font color=red>**为引用到的攻击项增加权重**</font>

```
T1546.016,
package installer,
leverage component requirement check execution launch command org download instal daemon http event installation application run trouton developer mitre maintainer applejeus post grant installer permission root complete version resource user dalton attack msi prebuild t1543 persistence adversary update well technique file prerm build manipulation linux script content package service system dependency bundle distribution specific privilege process brandon preinst environment window end microsoft use trigger,
abuse package associate installer monitor execution process command file installation argument application creation trigger
```

## Reference

[外链权重公式](https://wenku.baidu.com/view/64820136f46527d3240ce0b4.html?_wkts_=1679994987154&bdQuery=外链权重计算公式)

外部（链）权重：外部权重是指从其他网站引用到该网站的链接数。也就是说，如果一个网站被很多其他网站所引用，它就具有较高的外部权重。
$$
\begin{align*}
& score = weight * (\frac{n}{m}) * r \\
& - 相关系数 \ r \in (1, 10)  \\
& - 链点数 \ n \\
& - 链出数 \ m \\
\end{align*}
$$
[PageRank](https://zhuanlan.zhihu.com/p/137561088)（link analysis）

在有向图上定义一个随机游走模型，即一阶马尔可夫链，描述随机游走者沿着有向图随机访问各个结点的行为。

直观上，一个网页，如果指向该网页的超链接越多，随机跳转到该网页的概率也就越高，该网页的 PageRank 值就越高，这个网页也就越重要；一个网页，如果指向该网页的 PageRank 值越高，随机跳转到该网页的概率也就越高，该网页的 PageRank 值就越高，这个网页也就越重要。

PageRank 值依赖于网络的拓扑结构，一旦网络的拓扑(连接关系)确定，PageRank 值就确定。

PageRank 的计算可以在互联网的有向图上进行，通常是一个迭代过程。先假设一 个初始分布，通过迭代，不断计算所有网页的PageRank值，直到收敛为止。

[综合评分](https://zhuanlan.zhihu.com/p/396332074)

如今搜索引擎是按照这个方法进行计算页面得分的：score(页面得分) = TF-IDF分 * x + 链接分 * y + 用户体验分 * z（其中 x+y+z=100%）

2G左右谷歌搜索资料中，相关技术大咖做了相关预测，预测 TF-IDF 分值百度占比约为 40% 左右，谷歌 TF-IDF 分值占比约 50% 左右，通过做黑帽 SEO 的朋友介绍，TF-IDF 分值的权重值百度约占有 20%。
用户体验得分可以通过刷快排提高，百度占 40% 左右，Google无相关公示文档。
所以说在国内做 SEO：排名得分= 40% 内容质量（TF-IDF）+ 40% 用户体验分（快排）+ 20% 的链接分（域名+外链）

## 应用

$$
\begin{align*}
& score = x \times (TF(a, w) \times IDF(a)) + y \times link, \  \  x + y = 1 \\ \\
& TF(a,w)=\frac{count(a,w)}{limit(count(a,*))} \\
& - count(a, w)：单词w在攻击手段a中出现的次数 \\
& - count(a, *)：攻击手段a的总词数 \\
& - limit：总词数小于某阈值时将强制调节为该阈值 \\
& IDF(a)=log\frac{N+1}{N(a)+1} + 1 \\
& - N：语料库中的文档总数 \\
& - N(a)：单词w出现在多少种攻击手段中 \\ \\

& link = ?
\end{align*}
$$
