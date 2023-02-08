# 杀伤链模型

![img](https://inews.gtimg.com/newsapp_bt/0/14910170155/641)

**（1）侦察**

**（2）武器化**

**（3）交付**

**（4）利用**

**（5）安装**

**（6）命令与控制**

**（7）行动**

# Mitre ATT&CK 介绍

[(118条消息) MITRE ATT&CK超详细学习笔记-01（背景，术语，案例）_Zichel77的博客-CSDN博客](https://blog.csdn.net/weixin_43965597/article/details/125926620)

MITRE 防守方面临的困境，基于现实中发生的真实攻击事件，创建了一个对抗战术和技术知识库，即 **Adversarial Tactics，Techniques，and Common Knowledge**，简称 ATT&CK。

ATT&CK 模型正是在**杀伤链模型**的基础上，构建了一套更细粒度、更易共享的知识模型和框架。

最开始 ATT&CK 模型分为三部分，分别是：

- PRE-ATT&CK
- ATT&CK for Enterprise
- ATT&CK for Mobile

现在删减变为：

- Enterprise：传统企业网络和云技术
- Mobile：移动通信设备
- ICS：工业控制系统

这三个我们称之为技术域 Domain，在官网上每次的 ATT&CK 矩阵可以对三个技术域进行分开的选择，一般我们研究的都注重于 Enterprise 即可。

它与杀伤链有所不同的是，ATT&CK 的战术没有遵循任何线性顺序。相反，攻击者可以随意切换来实现最终目标。

## 相关术语

### （1）Matrix

横轴就是战术，核心研究攻击目标，战术的整体阶段大概是怎样的，只是大的行动纲领，具体怎么做取决于纵轴也就是我们的技术以及子技术，也就是 how 和 what

![image-20220907200642689](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907200642689.png)

### （2）TTPs

![在这里插入图片描述](https://img-blog.csdnimg.cn/0fc3899f57ad4f7cbfeedba1cb09809a.png)

ATT&CK 观察的主要目标是攻击者的TTPs，并将观察结果记录进行总结分类，从而形成知识库。

- 对于攻击方，TTPs 反映了攻击者的行为，调整 TTPs 所需付出的时间和金钱成本也最为昂贵
- 对于防守方，基于 TTPs 的检测和响应可能给对手造成更多的痛苦

简单点说，ATT&CK 是基于现实的、已经发生的 TTPs 的观察、总结形成的知识库，这不是学术理论的结果，意味着 ATT&CK 是具有很强的实战性和可落地性

### （3）痛苦金字塔

![在这里插入图片描述](https://img-blog.csdnimg.cn/7bbca944cfb443f59f87f979722bb0cf.png)

对抗一定是由下至上的，最后发展到最高层面，代表本质的行为

### （4）五大对象

![在这里插入图片描述](https://img-blog.csdnimg.cn/91e928cecdf14d1d9f30de61ee01b3b1.png)

![img](https://pic3.zhimg.com/80/v2-cb1eb7074feb01931ed043bf034fb1e2_1440w.jpg)

以一个特定的 APT 组织—— APT28 为例：

![在这里插入图片描述](https://img-blog.csdnimg.cn/71093ce5566146ec864894dbe3cd0196.png)

## ATT&CK 战术

![在这里插入图片描述](https://img-blog.csdnimg.cn/ad287dc5c2c1432b96f9b6d8d412bbd1.png)

ATT&CK 战术有 14 个，包括**侦察、资源开发、初始访问、执行、持久化、权限提升、防御绕过、发现、横向移动、搜集、命令控制、数据渗出、影响**。

战术仅为作战行动提供目标纲领,具体行动由战术中的技术与子技术实现。

# ATT&CK 数据

[mitre/cti: Cyber Threat Intelligence Repository expressed in STIX 2.0 (github.com)](https://github.com/mitre/cti)

[mitre-attack/attack-stix-data: STIX data representing MITRE ATT&CK (github.com)](https://github.com/mitre-attack/attack-stix-data)

# ATT&CK 数据使用官方文档

[cti/USAGE.md at master · mitre/cti (github.com)](https://github.com/mitre/cti/blob/master/USAGE.md)

## （1）The ATT&CK data model

| ATT&CK concept                                               | STIX object type                                             | Custom type? |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------ |
| [Matrix](https://github.com/mitre/cti/blob/master/USAGE.md#matrices) | `x-mitre-matrix`                                             | yes          |
| [Tactic](https://github.com/mitre/cti/blob/master/USAGE.md#tactics) | `x-mitre-tactic`                                             | yes          |
| [Technique](https://github.com/mitre/cti/blob/master/USAGE.md#techniques) | [attack-pattern](http://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230921) | no           |
| [Sub-technique](https://github.com/mitre/cti/blob/master/USAGE.md#sub-techniques) | [attack-pattern](http://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230921) where `x_mitre_is_subtechnique = true` | no           |
| [Procedure](https://github.com/mitre/cti/blob/master/USAGE.md#procedures) | [relationship](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230970) where `relationship_type = "uses"` and `target_ref` is an `attack-pattern` | no           |
| [Mitigation](https://github.com/mitre/cti/blob/master/USAGE.md#mitigations) | [course-of-action](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230929) | no           |
| [Group](https://github.com/mitre/cti/blob/master/USAGE.md#groups) | [intrusion-set](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230941) | no           |
| [Software](https://github.com/mitre/cti/blob/master/USAGE.md#software) | [malware](http://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230945) or [tool](http://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230961) | no           |
| [Data Source](https://github.com/mitre/cti/blob/master/USAGE.md#data-source) | `x-mitre-data-source`                                        | yes          |

增加的两种：

| STIX object type                                             | About                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [identity](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part2-stix-objects/stix-v2.0-csprd01-part2-stix-objects.html#_Toc476230933) | Referenced in the `created_by_ref` of all objects to state that the MITRE Corporation created the object |
| [marking-definition](https://docs.oasis-open.org/cti/stix/v2.0/csprd01/part1-stix-core/stix-v2.0-csprd01-part1-stix-core.html#_Toc476227338) | Referenced in the `object_marking_refs` of all objects to express the MITRE Corporation copyright |

### ① Extensions of the STIX spec（标准格式的推展）

| Field                  | Type     | Description                                                  |
| ---------------------- | -------- | ------------------------------------------------------------ |
| `x_mitre_version`      | string   | The version of the object in format where and are integers. ATT&CK increments this version number when the object content is updated.`major.minor``major``minor` |
| `x_mitre_contributors` | string[] | People and organizations who have contributed to the object. |
| `x_mitre_deprecated`   | boolean  | See [Working with deprecated and revoked objects](https://github.com/mitre/cti/blob/master/USAGE.md#Working-with-deprecated-and-revoked-objects). |

### ② IDs in ATT&CK

#### a.ATT&CK IDs

| ATT&CK concept                                               | ID format   |
| ------------------------------------------------------------ | ----------- |
| [Matrix](https://github.com/mitre/cti/blob/master/USAGE.md#matrices) | `MAxxxx`    |
| [Tactic](https://github.com/mitre/cti/blob/master/USAGE.md#tactics) | `TAxxxx`    |
| [Technique](https://github.com/mitre/cti/blob/master/USAGE.md#techniques) | `Txxxx`     |
| [Sub-Technique](https://github.com/mitre/cti/blob/master/USAGE.md#sub-techniques) | `Txxxx.yyy` |
| [Mitigation](https://github.com/mitre/cti/blob/master/USAGE.md#mitigations) | `Mxxxx`     |
| [Group](https://github.com/mitre/cti/blob/master/USAGE.md#groups) | `Gxxxx`     |
| [Software](https://github.com/mitre/cti/blob/master/USAGE.md#software) | `Sxxxx`     |
| [Data Source](https://github.com/mitre/cti/blob/master/USAGE.md#data-source) | `DSxxxx`    |

#### b.STIX IDs

ATT&CK 中所有对象都有 STIX IDs，且唯一

STIX ID 是以编程方式检索和引用对象的最佳方法

#### c.Other IDs

- NIST Mobile Threat Catalogue IDs（NIST 移动威胁目录 ID）
- CAPEC IDs

### ③ ATT&CK Types

#### a.Matrices（矩阵）

ATT&CK 矩阵总体布局存储在 x-mitre-matrix 中

对应的 ATT&CK 的 14 个战术：

![matrix, tactic and technique data model](https://raw.githubusercontent.com/mitre-attack/attack-website/master/modules/resources/docs/visualizations/data-model/stix-tactics-techniques.png)

#### b.Tactics（战术）

ATT&CK 中的战术由 x-mitre-tactic 定义

#### c.Techniques（技术）

ATT&CK 中的技术被定义为 attack-pattern 对象

##### **Sub-Techniques**

格式与 Techniques 相同，使用 `x_mitre_is_subtechnique=True` 来表示子技术

#### d.Procedures（过程）

ATT&CK 中的过程被表示为 relationship_type = "uses" 且 target_ref为 attack-pattern 的关系

过程可以源于组（intrusion-set）和软件（malware, tool）的使用

过程的内容在 description 中描述

#### e.Mitigations（预防）

ATT&CK 中的缓解措施被定义为 course-of-action 对象，与 STIX 中的 course-of-action 相同

#### f.Groups（攻击组织）

ATT&CK 中的组被定义为 intrusion-set 对象，与 STIX 中的 intrusion-set 相同

#### g.Software（软件）

ATT&CK 中的软件是 malware 和 tool 对象的结合

#### h.Data Sources and Data Components

**数据源**和**数据组件**表示可用于检测技术的数据。数据组件嵌套在数据源中，但具有自己的 STIX 对象。

- 一个数据组件只能有一个父数据源。
- 数据源可以具有任意数量的数据组件。
- 数据组件可以映射到任意数量的技术。

数据源和数据组件的一般结构如下：

<img src="C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907213716410.png" alt="image-20220907213716410" style="zoom:50%;" />

#### i.Relationships（关联）

ATT&CK 中的对象通过 relationship 对象相互关联

![img](https://raw.githubusercontent.com/mitre-attack/attack-website/master/modules/resources/docs/visualizations/data-model/stix-relationships.png)

## （2）Accessing ATT&CK data in python

[通过Python STIX2使用ATT&CK数据 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/311145611)

**① 创建虚拟环境**

```bash
python -m venv env
```

**② 启动虚拟环境**

```bash
cd xxx/env/Scripts/activate(.ps1)
```

**③ 安装 STIX**

```bash
pip install stix2
```

**④ 导入**

```python
from stix2 import Filter
…………
```

**⑤ 访问本地内容**

a.通过 FileSystemSource 加载

```python
from stix2 import FileSystemSource

src = FileSystemSource('./cti/enterprise-attack')
```

b.通过 bundle 加载

```python
from stix2 import MemoryStore

src = MemoryStore()
src.load_from_file("enterprise-attack.json")
```

**⑥ 访问在线内容**

[cti/USAGE.md at master · mitre/cti (github.com)](https://github.com/mitre/cti/blob/master/USAGE.md)

TAXII 服务器：

```python
server = Server("https://cti-taxii.mitre.org/taxii/")
```

**⑦ 同时访问多个域**

```python
from stix2 import CompositeDataSource

src = CompositeDataSource()
src.add_data_sources([enterprise_attack_src, mobile_attack_src, ics_attack_src])
```

## （3）Python recipes

[通过Python STIX2使用ATT&CK数据 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/311145611)

**① 获取单个对象**

通过

- STIX ID（构件开头）

  - ```python
    src.get("intrusion-set--f40eb8ce-2a74-4e56-89a1-227021410142")
    ```

- ATT&CK ID（见 ② a）

  - ```python
    from stix2 import Filter
    
    g0075 = src.query([ Filter("external_references.external_id", "=", "G0075") ])[0]
    ```

  - ![image-20220907220045900](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907220045900.png)

  - 从 STIX Bundle Object 文件的 object 字段中比对，找到 external_references

- name

  - ```python
    from stix2 import Filter
    
    def get_technique_by_name(thesrc, name):
        filt = [
            Filter('type', '=', 'attack-pattern'),
            Filter('name', '=', name)
        ]
        return thesrc.query(filt)
    # get the technique titled "System Information Discovery"
    get_technique_by_name(src, 'System Information Discovery')
    ```

  - ![image-20220907220311276](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907220311276.png)

  - 从 STIX Bundle Object 文件的 object 字段中比对，找到 name

- alias，同理，通过字段过滤

**② 获取多个对象**

最典型的按类型获取对象，不同于 ① 的是，搜索条件较为模糊，有可能有多个匹配项

```python
from stix2 import Filter

groups = src.query([ Filter("type", "=", "intrusion-set") ])
```

![image-20220907220532999](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907220532999.png)
