[(118条消息) 对STIX2.0标准12个构件的解读_fufu_good的博客-CSDN博客](https://blog.csdn.net/fufu_good/article/details/104109496/)

[网络威胁情报之 STIX 2.1 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/365563090?utm_id=0)

# STIX 介绍

**STIX 是一种描述网络威胁信息的结构化语言**，STIX 能够以标准化和结构化的方式获取更广泛的网络威胁信息。

STIX（Structured Threat Information Expression）是一种用于交换网络威胁情报（cyber threat intelligence，CTI）的语言和序列化格式。STIX的应用场景包括：**协同威胁分析、自动化威胁情报交换、自动化威胁检测和响应**等。

# STIX 对网络威胁情报的描述方法

![img](https://pic4.zhimg.com/80/v2-c9e59ff49083188d1bf41879c9e1756b_1440w.jpg)

**STIX 是一种<font color=red>基于图</font>的模型，其中 SDO 和 SCO 定义了图的节点，而 STIX relationships 定义了边**。

- **STIX Meta Objects**：用于丰富或扩展 **STIX Core Objects**
- **STIX Bundle Object**：用于打包 STIX 内容

① **STIX Domain Objects**（SDO）：威胁情报主要的分类对象，包含了一些威胁的 behaviors 和 construct，共有 18 种类型：Attack Pattern, Campaign, Course of Action, Grouping, Identity, Indicator, Infrastructure, Intrusion Set, Location, Malware, Malware Analysis, Note, Observed Data, Opinion, Report, Threat Actor, Tool, and Vulnerability.

② **STIX Cyber-observable Objects**（SCO）：威胁情报中具体的可观察对象，用于刻画**基于主机或基于网络的信息**

- SCO 会被多种 SDO 所使用，以提供上下文支持，如 *Observed Data* SDO，表示在特定时间观察到的 raw data；在 STIX2.0 中，SCO 在 SDO 中出现时只会以 Observed Data 的形式出现，在 STIX2.1 则不限于此
- SCO 本身不包括 who，when 和 why 的信息，但是将 SCO 和 SDO 关联起来，可能会得到这些信息以及对威胁更高层面的理解
- SCO 可以捕获的对象包括文件、进程、IP 之间的流量等

③ **STIX Relationship Objects**（SRO）：用于 SDO 之间、SCO 之间、SDO 和 SCO 之间的关系。SRO 的大类包括以下两种：

- **generic SRO（Relationship）**：大多数关系所采用的类型，其 relation_type 字段包括：

- - 内置关系：如 Indicator 到 Malware 之间的关系，可以用 *indicates* 表示，它描述了该 Indicator 可用于检测对应的恶意软件
  - 自定义关系

- **Sighting SRO**：用于捕获实体在 SDO 中出现的案例，如 sighting an indicator。没有明确指明连接哪两个 object。之所以将其作为独立的 SRO，是因为其具有一些独有的属性，如 *count*。

## STIX 通用属性

![img](https://pic3.zhimg.com/80/v2-4502a49dc00fc1bfae5913c20a191a3e_1440w.jpg)

![image-20220907212632894](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20220907212632894.png)

# STIX 1.0 和 2.0

**STIX 1.0 定义了 8 种构件**：可观测数据（Observation）、攻击指标（Indicator）、安全事件（Incident）、攻击活动（Campaign）、威胁主体（Threat Actor）、攻击目标（ExploitTarget）、攻击方法（TTP）、应对措施（CourseOfAction）在内的八个威胁信息构件。

**STIX 2.0 定义了 12 种构件**：Attack Pattern、Campaign、Course of Action、Identity、Indicator、Intrusion Set、Malware、Observed Data、Report、Threat Actor、Tool、and Vulnerability。

2.0 将 1.0 版本中的 

- TTP 进行更细致的描述拆分为 Attack Pattern、Intrusion Set、Tool、Malware
- 从 Exploit Target 拆分出 Vulnerability
- 从威胁主体（Threat Actor）中拆分出 Identity、Intrusion Set
- 删去了 Incident
- 新增了 Report

# STIX 2.0 标准的 12 个构件（不止）

[sdo — stix2 3.0.1 documentation](https://stix2.readthedocs.io/en/latest/api/v20/stix2.v20.sdo.html#)

## 1. Attack Pattern（攻击模式）

描述攻击者试图破坏目标的方式，由原来版本的 TTP 拆分出来的

## 2. Campaign（攻击活动或网络战役）

Campaign 是描述一系列针对特定目标的恶意行为或一段时间内发动的攻击

一次 APT 攻击活动就像军事上针对特定目标的定点打击或间谍渗透，类似一次攻击战役

通常将攻击者或其实施的攻击行动赋予独有的代号进行识别。例如，某攻击者使用一组特定的 TTP（恶意软件和工具）以某个特定目的攻击一个工业部门，那么这就是一次“XXXX活动”。

## 3. Course of Action（处置方法）

**处置方法**是指针对威胁的具体应对方法，包括修复性措施或预防性措施，以及对“安全事件”造成影响的反制或缓解手段。

## 4. Identity（身份）

STIX2.0 里将“攻击目标(受害者)、威胁源、威胁参与者、信息来源”的身份用单独构件进行描述。

身份可以表示实际的个人、组织或团体以及个人、组织或团体的类别（如金融部门）。

## 5. Indicator（威胁指标）

“**威胁指标**”用来识别一个特定“攻击方法”的技术指标，它是多个“可观测数据”的组合，是用来检测“安全事件”的检测规则。

## 6. Intrusion Set（入侵集）

入侵基础设施是一组具有共同属性的行为和资源，属于某单个组织协调的。入侵基础设施可以捕获多个活动或其他活动，这些活动都由共享属性绑定在一起，这些共享属性代表一个常见的已知或未知的威胁参与者。简单说入侵基础设施即指该威胁源所拥有的 IP、域名、社工库等攻击资源。

## 7. Tool（工具）

指威胁源在过往攻击事件中常用的工具，工具其实也涉及到恶意软件，但是恶意软件单独拿了出去，作为一个独立的构件。TOOL 也可以包含防御人员在响应中使用的工具。

## 8. Malware（恶意软件）

恶意软件是一种 TTP 类型，也称为恶意代码和恶意软件，指插入系统中的程序，通常是**秘密插入**，**目的是破坏受害者数据、应用程序或操作系统（OS）的机密性、完整性或可用性**。

## 9. Observed Data（可观测数据）

指该威胁源在攻击时可观测到的一系列行为特征，包括**流量侧和系统侧**两大类，如访问特定的 C&C 节点、特定的扫描行为、在特定时间发送钓鱼邮件、尝试上传某类 Webshell 等。

## 10. Report（报告）

**报告是集中于一个或多个主题的威胁情报的集合**，例如威胁参与者的描述、恶意软件或攻击技术，包括上下文和相关细节。它们用于将相关的威胁情报分组，以便将其作为一个全面的网络威胁故事发布。

## 11. Threat Actor（威胁源）

Threat Actor（即威胁源），在威胁情报中用于描述实施网络攻击威胁的**个人、团伙或组织**以达到其恶意的动机和意图。Threat Actor 结构中捕获各种信息详情，包括**身份、动机、预期效果和复杂程度**。

## 12. Vulnerability（脆弱性）

Vulnerability 属性表示可能被利用的目标漏洞。信息的示例包括漏洞描述（结构化或非结构化的方式）、CVE 标识符、OSVDB 标识符和 CVSS 信息。
