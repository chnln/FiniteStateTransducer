from NFA import *
import preprocess
from collections import Counter

lang_list = {"en": "english", "la": "latin", "ru": "russian", "na": "navajo", "ar": "arabic"}

EPSILON = "__EPSION__"
NOCHANGE = "__NO_CHANGE__"
default_weight = 0.1
offset = 50  # 1
language = lang_list["en"]  # set language


def cal_weight(affix_list):
    # 计算权重
    affix_list = sorted(affix_list, key=lambda x: (x[2], x[1]))
    res = []
    tot = len(affix_list)
    while affix_list:
        cmp = affix_list[0]
        weight = affix_list.count(cmp) / tot * offset
        res.append(cmp + [weight])
        affix_list = [word for word in affix_list if word != cmp]
    # for i in res:
    #     print(i)
    return res


def run_train():
    irregular, prefix, suffix = preprocess.get_affix_list(language, "train")

    prefix = cal_weight(prefix)
    suffix = cal_weight(suffix)

    # irregular 不规则变换（lemma和inflection形态一样）
    node_irregular_out = Node(accepting=True)  # name="irregular_out"
    # node_dict[node_irregular_out.name] = node_irregular_out
    for lemma, features, inflection in irregular:
        node_irregular.add_next(label=('^' + inflection + '$'), out=(lemma, features), node=node_irregular_out, weight=1)
    # print(node_irregular.next)

    # prefix 优先前缀匹配，再原样输出
    node_prefix_out = Node(accepting=True)  # name="prefix_out"
    node_prefix_out.add_next(label='.', out=(NOCHANGE, []), node=node_prefix_out, weight=default_weight)
    # node_dict[node_prefix_out.name] = node_prefix_out

    for lemma, features, inflection, weight in prefix:
        node_prefix.add_next(label=('^' + inflection), out=(lemma, features), node=node_prefix_out, weight=weight)
    # print(node_prefix.next)
    # print(node_prefix_out.next)

    # suffix 优先后缀匹配，再原样输出
    node_suffix_out = Node(accepting=True)  # name="suffix_out"
    # node_dict[node_suffix_out.name] = node_suffix_out

    for lemma, features, inflection, weight in suffix:
        node_suffix.add_next(label=(inflection + '$'), out=(lemma, features), node=node_suffix_out, weight=weight)

    node_suffix.add_next(label='.', out=(NOCHANGE, []), node=node_suffix, weight=default_weight)
    # print(node_suffix.next)
    # print(node_suffix_out.next)

    # 允许先进行前缀匹配，再进行后缀匹配
    node_prefix_out.add_next(label=EPSILON, out=("", []), node=node_suffix, weight=1)


def run_dev():
    # 和run_test程序框架一样，可以直接修改run_test函数第一行"test"为"dev"
    pass


def run_test():
    wl = preprocess.get_word_list(language, "test")
    tot = 0
    correct = 0
    output_list = []
    for lemma, inflection, feature in wl:
        g.result = []
        g.search(start, inflection, 0, "", [], 1)
        result = g.result
        result = sorted(result, key=lambda x: x[2], reverse=True)
        my_lemma, my_feat, my_weight = result[0][0], result[0][1], result[0][2]
        if my_lemma == "":  # 处理特殊情况
            my_lemma = lemma
        my_feat = ';'.join(list(set(my_feat)))  # 如果先后进行了前缀和后缀匹配，可能会出现特征重复，这里去重
        output = "No.%d inf: %s lemma: %s feat: %s my_ans: %s %s weight: %.4f\n" % \
                 (tot, inflection, lemma, feature, my_lemma, my_feat, my_weight)
        output_list.append(output)
        print(output, end="")
        # print(result)
        tot += 1
        if lemma == result[0][0]:
            correct += 1
    output_rate_correct = "language: %s 正确率（仅匹配lemma）： %.4f\n" % (language, correct/tot)
    output_list.append(output_rate_correct)
    print(output_rate_correct)  # 正确率，这里以lemma相同为正确标准，未考虑特征

    with open("result_%s.out" % language, "w", encoding="UTF-8") as f:
        f.write(''.join(output_list))


if __name__ == '__main__':
    # initialize NFA
    g = NFA()
    start = g.get_start_node()

    node_irregular = Node(accepting=False)  # name="irregular"
    node_prefix = Node(accepting=False)  # name="prefix",
    node_suffix = Node(accepting=False)  # name="suffix"
    start.add_next(label=EPSILON, out=("", []), node=node_irregular)
    start.add_next(label=EPSILON, out=("", []), node=node_prefix)
    start.add_next(label=EPSILON, out=("", []), node=node_suffix)

    # node_dict = {'start': start, "irregular": node_irregular, "prefix": node_prefix, "suffix": node_suffix}
    # print(start.next_list, start.next)

    # start training
    run_train()

    # show nfa
    # with open("show_nfa_%s.txt" % language, "w", encoding="UTF-8") as f:
    #     show_nfa(f, start, "", [])

    # start testing
    run_test()
