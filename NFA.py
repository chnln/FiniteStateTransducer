import re

EPSILON = "__EPSION__"
NOCHANGE = "__NO_CHANGE__"

default_weight = 0.1


class Node:
    def __init__(self, accepting=False):
        # self.name = name
        self.accepting = accepting
        self.next = {}
        self.next_list = []  # 方便检索结点与结点的相连情况

    def add_next(self, label, out, node, weight=default_weight):
        if label not in self.next:
            self.next[label] = [(out, node, weight)]
            self.next_list.append(node)
        elif node not in self.next_list:
            self.next[label].append((out, node, weight))
            self.next_list.append(node)


class NFA:
    def __init__(self):
        self.start = Node(accepting=False)
        self.result = (EPSILON, [])

    def get_start_node(self):
        return self.start

    def search(self, state, labels, i, out_str, features, w):
        if i >= len(labels):
            self.result.append((out_str, features, w))
            # print((out_str, features, w))
            return
        for label, edges in state.next.items():
            for output, node, weight in edges:
                if label == EPSILON:  # irrugular、prefix或suffix三个结点之一（或者是前缀匹配完后进入后缀匹配）
                    # print("enter -> mode: ", node.name)
                    self.search(node, labels, i, out_str, features, w * weight)
                elif re.match(label, labels[i:]) is not None:
                    if label == '.':  # 原样输出
                        # print("enter->label: %s left: %s out_str: %s out_feat: %s weight: %d"
                        #       % (label, labels[i+1:], out_str+labels[i], features, w* weight))
                        self.search(node, labels, i + 1, out_str + labels[i], features, w * weight)
                    else:  # 匹配到了前后缀
                        match_len = len(label.strip("^$"))
                        # print("enter->label: %s left: %s out_str: %s out_feat: %s weight: %d"
                        #       % (label, labels[i+match_len:], out_str + output[0], features + output[1], w * weight))
                        if output[0] == EPSILON:  # 如果对应原型为空
                            self.search(node, labels, i + match_len, out_str, features + output[1],
                                        w * weight)
                        else:
                            self.search(node, labels, i + match_len, out_str + output[0], features + output[1],
                                        w * weight)

                else:
                    # print("Can't handle")
                    pass


def show_nfa(f, state, bl, visited):
    for str, edges in state.next.items():
        for edge in edges:
            if edge not in visited:
                f.write("%s %s -> %s + %s\n" % (bl, str, edge[0][0], ';'.join(edge[0][1])))
                visited.append(edge)
                show_nfa(f, edge[1], bl + " ", visited)
