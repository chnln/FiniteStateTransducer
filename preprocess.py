fd_train = r"C:\Users\chnln\Desktop\Course\李素建孙薇薇编译原理\homework\fst\task2_data"
lang_list = {"en": "english", "la": "latin", "ru": "russian", "na": "navajo", "ar": "arabic"}
EPSILON = "__EPSION__"


def find_lcs(s1, s2):   # 求最长公共子串
    s1_l, s2_l = len(s1), len(s2)
    m = [[0 for j in range(s2_l)] for i in range(s1_l)]
    max_l = 0
    p = -1
    for i in range(s1_l):
        for j in range(s2_l):
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    m[i][j] = 1
                else:
                    m[i][j] = m[i - 1][j - 1] + 1
                if m[i][j] > max_l:
                    max_l = m[i][j]
                    p = i + 1
    return s1[p - max_l:p]


def get_word_list(lang, mode, sort=False):
    # mode = "train|dev|test"
    fp_train = fd_train + r"\%s\%s-%s" % (lang, lang, mode)
    word_list = []
    with open(fp_train, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            word_list.append(line[0:-1].split('\t'))
    if sort is False:
        return word_list
    else:
        return sorted(word_list, key=lambda x: x[1])


def get_prefix(stem, inf):  # 根据stem从inflection中提取词首部分
    n = inf.find(stem)
    if n == 0:
        return EPSILON
        # return ""
    else:
        return inf[0:n]


def get_suffix(stem, inf):  # 根据stem从inflection中提取词尾部分
    n = inf.find(inf) + len(stem)
    if n >= len(inf):
        return EPSILON
        # return ""
    else:
        return inf[n:]


def get_affix_list(lang, mode="train"):  # 返回提取出的不规则变化、前缀和后缀，均为(lemma, feature, inflection)三元组
    irregular = []
    prefix = []
    suffix = []

    word_list = get_word_list(lang, mode, sort=True)

    for lemma, inflection, feature in word_list:
        if lemma == inflection:  # irregular form
            # irregular[lemma + '+' + feature] = inflection
            irregular.append((lemma, feature.split(';'), inflection))
        else:
            stem = find_lcs(lemma, inflection)
            if get_prefix(stem, inflection) != EPSILON:
                # prefix[get_prefix(stem, lemma) + '+' + feature] = get_prefix(stem, inflection)
                prefix.append((get_prefix(stem, lemma), feature.split(';'), get_prefix(stem, inflection)))
            if get_suffix(stem, inflection) != EPSILON:
                # suffix[get_suffix(stem, inflection)] = get_suffix(stem, lemma)
                # suffix[get_suffix(stem, lemma) + '+' + feature] = get_suffix(stem, inflection)
                suffix.append((get_suffix(stem, lemma), feature.split(';'), get_suffix(stem, inflection)))

    return irregular, prefix, suffix


if __name__ == '__main__':
    language = lang_list["en"]
    a, b, c = get_affix_list(language)
    # b = sorted(b.items(), key=lambda x: x[0])
    # c = sorted(c.items(), key=lambda x: x[0])
    for i in a:
        print(i)
    print('\n```````\n')
    for i in b:
        print(i)
    print('\n```````\n')
    for i in c:
        print(i, ' ')
    # print(a, '\n', b, '\n', c)

    # words_list = get_word_list("la")
    # words_list = sorted(words_list, key=lambda x: x[0])
    # for word in words_list:
    #     lemma, inflection, feature = word[0], word[1], word[2]
    #     lcr = find_lcs(lemma, inflection)
    #     lcr_l = len(lcr)
    #     # print("lemma: %s inflection: %s feature: %s stem: %s prefix: %s suffix: %s"
    #     #      % (lemma, inflection, feature, lcr, get_prefix(lcr, inflection), get_suffix(lcr, inflection)))
    #     if get_prefix(lcr, inflection) != EPSILON:
    #         print("%s: %s-%s-%s + %s -> %s" % (lemma, get_prefix(lcr, inflection), lcr, get_suffix(lcr, inflection),
    #                                        feature, inflection))
