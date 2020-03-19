# Finite State Transducer in Morphology Analysis
> 2020 Spring: Principles of Compilers, exercise about NFA
>
> AUTHOR: Nascent
>
> URL: https://github.com/chnln/FiniteStateTransducer

## 1 算法原理
### 1.1 特征提取
在`lemma`和`inflection`中匹配得到最长公共子串 `lcr (longest common substring)`作为`stem`

分别通过`stem`和`inflection`、`stem`和`lemma`的对比得到词缀（前缀和后缀，不支持中缀），
及词缀在原型和曲折形式的对应关系与特征，可以表达为`(affix in lemma, features, affix in inflection)`三元组

允许词缀在lemma中的对应为空字符串，不允许inflection中存在空词缀
### 1.2 NFA
构造`Node`类，允许一个转移状态`label`对应多条边、指向多个节点，通过控制插入结点的先后顺序控制规则应用的先后顺序

开始结点`start`指向`irregular`、`prefix`和`suffix`三个结点

`irregular`通过多条边指向终止结点，每条边储存不规则变化，这里特指整体词型不变的情况

`prefix`通过多条前缀匹配的边指向终止结点；
终止结点指向自身，边的label为`'.'`，可以通过正则表达式匹配任意字符，实现字符原样输出

`suffix`先通过多条后缀匹配的边指向终止结点，再通过label为`'.'`的边指向自身，实现先尝试后缀匹配再原样输出
### 1.3 FST
深度优先搜索，按插入顺序依次遍历与`start`相连的边并进入对应结点开始新的DFS

匹配完所有字符后，将结果加入列表，返回结果列表。主程序根据权重排序后输出权重最大值对应的结果。
## 2 程序结构
运行方法：`python FiniteStateTransducer.py`

需要在preprocess.py文件中修改输入文件所在文件夹`task2_data`路径；
另可在主程序主函数修改测试集语言，有标准输出和文件输出两份输出

FiniteStateTransducer.py: 主程序
- language: 设置训练集的语言
- default_weight: 设置原样输出的边权值
- offset: 调整权重
- run_train()：训练
- run_dev()：改进；该部分功能可通过更改run_test()部分参数实现，故该部分代码未实现
- run_test(): 测试；正确率仅匹配lemma，特征未计入

NFA.py: 实现Node类、NFA类和NFA中的搜索
- show_nfa() 以层次结构展示NFA

preprocess.py：实现提取词缀
- fd_train 设置输入文件所在文件夹`task2_data`路径
- get_affix_list(): 返回提取的前缀、后缀

## 3 运行效果（正确率）
注释：正确率计算只匹配lemma，不考虑特征

Setting 1: default_weight = 0.1，offset = 1, 允许前缀匹配后进行后缀匹配

Setting 2: default_weight = 0.1，offset = 50, 允许前缀匹配后进行后缀匹配

|  参数   | English  |  Russian | Latin | Arabic | Navajo |
|  :----:  | :----:  | :----: |   :----:  | :----:  | :----: |
| Setting 1  | 65% |  27%  | 23%  | 11% | 3% |
| Setting 2  | 65% |  43%  | 30%  | 8% | 2% |

## 4 改进方向
- 目前只支持前缀、后缀，不支持中缀、环缀
- 准确率较低，特别在非英语语言中，词汇中部字符存在变换，模型运行效果不好
- 词型、词缀提取待优化
- 边权重计算待优化
- 训练集和测试集中多重前缀/后缀的情况极少，暂不支持对这种情况的处理
- 搜索待优化，目前在英语、俄语之外的语言耗时较长，
主要是因为Latin、Arabic和Navajo三种语言中存在较多前缀、后缀同时存在的情况，搜索比较冗长

## 相关缩写：
> inf inflection
>
> feat feature