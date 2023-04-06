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

https://blog.csdn.net/qq_41427834/article/details/110262036

**一阶马尔可夫**：系统转移到下一时刻的任一给定状态的概率仅依赖于当前(1 阶)状态

https://blog.csdn.net/A13526_/article/details/124769112

**全概率公式**：		时刻 $T_0, T_1, T_2, ……$		状态 $S_1, S_2, ……, S_n$
$$
S_1 \ \ \ \ \ \ \ \ \ \ S_2 \ \ \ \ \ \ \ \ \ \ S_3 \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ S_n \ \ \ \\
\begin{bmatrix} 
p_{11} & p_{12} & p_{13} & 	…… & p_{1n} \\ 
p_{21} & p_{22} & p_{23} & 	…… & p_{2n} \\ 
p_{31} & p_{32} & p_{33} & 	…… & p_{3n} \\ 
…… 		 & …… 		& …… 		 &  …… & …… \\
p_{n1} & p_{n2} & p_{n3} & 	…… & p_{nn}
\end{bmatrix}\quad
$$
$Pr(T_1 = S_i | T_0 = S_j) = p_{ij}$

$Pr(T_2) = Pr(T_1 = S_1 | T_0 = S_1)$

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
& - N：攻击手段总数 \\
& - N(a)：单词w出现在多少种攻击手段中 \\ \\

& link = ?
\end{align*}
$$

### link: PageRank

$$
\begin{align*}
& PR(a)_{i+1} = \sum_{i=0}^n \frac{PR(T_i)}{L(T_i)} \\
& - i：循环次数 \\
& - n：节点总数 \\
& - PR(T_i)：其它指向 a 节点的 PR 值 \\
& - L(T_i)：其它指向 a 节点的出链数 \\ \\

& 矩阵化表达：PR(a) = M * V \\
& - M：固定，出链矩阵，转移概率矩阵，每个元素 \in [0, 1]，n \times n \\
& - V：转移前的 PR 值，n \times 1 \\ \\

& Q1：Dead \ Ends \\
& M 为幂零矩阵，即 \ \exists \ k \in N, 使得 M^k = 0, 则 \ PR \ 值最终均变为 \ 0 \\
& e.g. A -> B, C -> B, B \ 没有出链 \\
& \ \ A \ \ \ B \ \ \ C \\
& \begin{bmatrix} 
0 & 0 & 0 \\ 
1 & 0 & 1 \\ 
0 & 0 & 0 \\ 
\end{bmatrix}\quad \\
& A：修正 \ M \\
& M' = M + a^T(\frac{e}{n}) \\
& -a：无出链节点所在列（全为 \ 0） \\
& -e：[1, 1, 1, ……, 1]^T\\
& -n：总节点数 \\ \\

& Q2：Spider \ Traps \\
& 某节点只有指向自己的出链，其它节点指向它，这会导致权重向该节点偏移，\\ 
& 即 \ PR \ 值在更新过程中，含有自指节点的 \ PR \ 值会逐渐归于 \ 1，其它节点归于 \ 0 \\
& A：修正 \ M \\
& M = \beta M + (1 - \beta)\frac{ee^T}{n} \\
& - \beta：跟随出链到达某节点的概率 \\
& - 1 - \beta：随机跳到其它节点的概率 \\
& - ee^T：由 \ 1 \ 填满的 \ n \times n \ 矩阵 \\
& -n：总节点数 \\ \\

& 最终修正公式 \\ \\
& PR(a) = M * V \Rightarrow \\
& PR(a) = [\beta (M + a^T(\frac{e}{n})) + (1 - \beta)\frac{ee^T}{n}] * V
\end{align*}
$$


$$
\begin{align*}
& 注：adj\_matrix \ is \ directed, \ where \ adj\_matrix[i][j] \ is \ 1 \ if \ there \ is \ a \ hyperlink \\ & from \ webpage \ i \ to \ webpage \ j, \ and \ 0 \ otherwise \\
& 若要根据邻接矩阵计算某网页出链，则需要对邻接矩阵的该行求和 \\ 
&    out\_degree: np.ndarray = np.sum(adj\_matrix, axis=1) \\
& score[i] = \sum_{j=0}^N\frac{score[j]}{out\_degree[j]} \\
& Q1: Dead \ Ends \ 出链即 \ out\_degree[j] \ 为 \ 0 \\
& A: 若无出链，则分母加一平滑 \\
& score[i] = \sum_{j=0}^N\frac{score[j]}{out\_degree[j]}, out\_degree[out\_degree == 0] \ += \ 1 \\
& Q2: Spider \ Traps \ 某节点只有指向自己的出链 \\
& A: 增加指向其它节点的概率 \\
& score[i] = \frac{(1 - d)}{N} + d * \sum_{j=0}^N\frac{score[j]}{out\_degree[j]}, out\_degree[out\_degree == 0] \ += \ 1 \\
& Q3: 迭代与收敛 \\
& A: 指定最大迭代次数 \ max\_iter \ 和迭代算法的认为收敛的数值 \ tol \\
& for \ k \ in \ max\_iter: \\
& \ \ \ \ new\_score[i] = \frac{(1 - d)}{N} + d * \sum_{j=0}^N\frac{score[j]}{out\_degree[j]}, out\_degree[out\_degree == 0] \ += \ 1 \\
& \ \ \ \ if \ new\_score[i] - score[i]  < tol: \\
& \ \ \ \ \ \ \ \ break \\
& \ \ \ \ score[i] = new\_score[i]
\end{align*}
$$


```python
def pagerank(adj_matrix: np.ndarray, d=0.85, max_iter=100, tol=1e-6):
    """
    Consider the issue of hyperlink by ranking the importance of webpages in a directed graph.

    :param adj_matrix: directed, where adj_matrix[i][j] is 1 if there is a hyperlink from webpage i to webpage j,
                       and 0 otherwise.
    :param d: damping factor, usually set to 0.85
    :param max_iter: maximum number of iterations
    :param tol: tolerance level convergence of the PageRank algorithm, 1e-6 is a common default value for many
                iterative algorithms
    :return: score of pagerank
    """
    N: int = adj_matrix.shape[0]

    # 若要根据邻接矩阵计算某网页出链, 则需要对邻接矩阵的该行求, 注意无出链情况下为了防止分母为 0 也为了防止 Dead Ends 问题, 需要将分母加一平滑
    out_degree: np.ndarray = np.sum(adj_matrix, axis=1)
    out_degree[out_degree == 0] += 1

    score = np.ones(N) / N
    for i in range(max_iter):
        # Pr = M * V, M = adj_matrix, V 转置前 = score / out_degree
        new_score = (1 - d) / N + d * adj_matrix.T.dot(score / out_degree)
        if np.linalg.norm(new_score - score) < tol:
            break
        score = new_score
    return score
```

# 最终公式

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

