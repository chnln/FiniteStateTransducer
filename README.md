# Finite State Transducer in Morphology Analysis
> TERM: 2020 Spring: Principles of Compilers, exercise about NFA
>
> AUTHOR: Nascent
>
> URL: https://github.com/chnln/FiniteStateTransducer

## 程序结构

FiniteStateTransducer.py：主程序

- language：设置训练集的语言

NFA.py：实现Node类、NFA类和NFA中的搜索

- show_nfa() 以层次结构展示NFA

preprocess.py：实现提取词缀

结点的name属性及FiniteStateTransducer.node_list没有使用，可删去
状态转移时label使用的正则表达式，但作用不大，使用普通字符串也可

## 改进方向

只支持前缀、后缀，不支持中缀、环缀，对拉丁语等词中字符存在变换的语言支持也不好

词型提取和权重赋值待优化；搜索过程不清晰，需要优化；暂不支持前缀匹配后再后缀匹配

相关缩写：
inf inflection
feat feature