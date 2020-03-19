from NFA import *
import preprocess

lang_list = {"en": "english", "la": "latin", "ru": "russian", "na": "navajo", "ar": "arabic"}

EPSILON = "__EPSION__"
NOCHANGE = "__NO_CHANGE__"


def run_train():
    irregular, prefix, suffix = preprocess.get_affix_list(language, "train")

    # irregular 不规则变换（lemma和inflection形态一样）
    node_irregular_out = Node(name="irregular_out", accepting=True)
    node_dict[node_irregular_out.name] = node_irregular_out
    for lemma, feature, inflection in irregular:
        node_irregular.add_next(label=('^' + inflection + '&'), out=(lemma, feature), node=node_irregular_out)
    # print(node_irregular.next)

    # prefix 优先前缀匹配，再原样输出
    node_prefix_out = Node(name="prefix_out", accepting=True)
    node_prefix_out.add_next(label='.', out=(NOCHANGE, []), node=node_prefix_out)
    node_dict[node_prefix_out.name] = node_prefix_out

    for lemma, feature, inflection in prefix:
        node_prefix.add_next(label=('^' + inflection), out=(lemma, feature), node=node_prefix_out, weight=2)
    # print(node_prefix.next)
    # print(node_prefix_out.next)

    # suffix 优先原样输出，再后缀匹配
    node_suffix_out = Node(name="suffix_out", accepting=True)
    node_dict[node_suffix_out.name] = node_suffix_out

    for lemma, feature, inflection in suffix:
        node_suffix.add_next(label=(inflection + '$'), out=(lemma, feature), node=node_suffix_out, weight=2)

    node_suffix.add_next(label='.', out=(NOCHANGE, []), node=node_suffix)

    # print(node_suffix.next)
    # print(node_suffix_out.next)


def run_dev():
    pass


def run_test():
    wl = preprocess.get_word_list(language, "test")
    tot = 0
    correct = 0
    for lemma, inflection, feature in wl:
        g.result = []
        g.search(start, inflection, 0, "", [], 1)
        result = g.result
        result = sorted(result, key=lambda x: x[2], reverse=True)
        print("inf: %s ans: %s feat: %s my_ans: %s %s" %
              (inflection, lemma, feature, result[0][0], ';'.join(result[0][1])))
        tot += 1
        if lemma == result[0][0]:
            correct += 1
    print("%.4f" % (correct/tot))  # 正确率，这里以lemma相同为正确标准，未考虑特征


if __name__ == '__main__':
    # set language
    language = lang_list["en"]

    # initialize NFA
    g = NFA()
    start = g.get_start_node()

    node_irregular = Node(name="irregular", accepting=False)
    node_prefix = Node(name="prefix", accepting=False)
    node_suffix = Node(name="suffix", accepting=False)
    start.add_next(label=EPSILON, out=("", []), node=node_irregular)
    start.add_next(label=EPSILON, out=("", []), node=node_prefix)
    start.add_next(label=EPSILON, out=("", []), node=node_suffix)

    node_dict = {'start': start, "irregular": node_irregular, "prefix": node_prefix, "suffix": node_suffix}

    # print(start.next_list, start.next)

    # start training
    run_train()

    # show nfa
    # with open("out.txt", "w", encoding="UTF-8") as f:
    #     show_nfa(f, start, "", [])

    # start testing
    run_test()
