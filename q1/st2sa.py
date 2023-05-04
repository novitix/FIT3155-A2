# Student Name: Adam Ye
# Student ID: 31460798

from __future__ import annotations
from typing import List, Tuple, Optional, Union


def c2i(s: str) -> int:
    return ord(s)-37


class Node:
    __ASCII_RANGE = 90
    __children_count = 0

    def __init__(self, start: int, end: int, s: str, value: int):
        self.start = start
        self.end = end
        self.children: List[Node | None] = [None]*self.__ASCII_RANGE
        self.suffix_link: Optional[Node] = None
        self.value: int = value
        self.atestchildren = []
        self.s = s

    def __len__(self):
        return self.end-self.start+1

    def __repr__(self):
        return self.s[self.start:self.end+1]
    

    def myprint(self, level=0):
        ret = "   "*level+self.s[self.start:self.end+1]+"\n"
        for child in self.atestchildren:
            ret += child.myprint(level+1)
        return ret
    
    def is_leaf(self) -> bool:
        return self.__children_count == 0

    def add_child(self, child: Node, string: str):
        idx = c2i(string[child.start:child.start+1])
        if self.children[idx] is None:
            self.__children_count += 1
        self.children[idx] = child
        self.atestchildren.append(child)

    def remove_child(self, child: Node, string: str):
        idx = c2i(string[child.start:child.start+1])
        if self.children[idx] is not None:
            self.__children_count -= 1
        self.children[idx] = None
        self.atestchildren.remove(child)

    def get_active_node(self, start: int, end: int, string: str) -> Tuple[Node, int]:
        # finds last node IN str[start..end] starting from this node
        print('end' + str(end))
        cur_node = self
        next_child = cur_node.children[c2i(string[start:start+1])]
        while next_child is not None and len(next_child) < end-start+1 and not next_child.is_leaf():
            cur_node = next_child
            start += len(next_child)
            next_child = cur_node.children[c2i(string[start:start+1])]
        # start points to remaining path str[start..end]
        # that has not been matched yet
        return (cur_node, start)

# def skip_count(sub_root: Node, start: int, end: int) -> Node:
#     while end > sub_root.end - sub_root.start + 1:
#         for child in sub_root:
#             if child[0] ==


def insert_letter(root: Node, i: int, string: str):
    n = len(string)
    active_node, start_rem_path, node_needing_suffix_link = None, None, None

    for j in range(i+1):
        if active_node is None:
            active_node, start_rem_path = root.get_active_node(j, i, string)
        else:
            active_node, start_rem_path = active_node.suffix_link.get_active_node(j, i, string)

        active_nodes_child = active_node.children[c2i(string[start_rem_path])]

        if active_nodes_child is not None and active_nodes_child.is_leaf() and str(active_nodes_child) == string[start_rem_path:i]:
            # Rule 1
            active_nodes_child.end += 1
            active_nodes_child.value = j+1
            if node_needing_suffix_link is not None:
                node_needing_suffix_link.suffix_link = active_node
                node_needing_suffix_link = None
        else:
            k = 0
            if active_nodes_child is not None:
                while (start_rem_path+k < n and string[active_nodes_child.start+k] == string[start_rem_path+k]):
                    k += 1
            if active_nodes_child is None:
                # Rule 2 (Alt)
                new_node = Node(start_rem_path, i, string, j+1)
                active_node.add_child(new_node, string)

                if node_needing_suffix_link is not None:
                    node_needing_suffix_link.suffix_link = active_node
                    node_needing_suffix_link = None
            elif start_rem_path+k < i+1:
                # Rule 2 (Reg)

                # k points to 1st mismatch
                assert active_nodes_child is not None
                active_node.remove_child(active_nodes_child, string)
                new_node = Node(active_nodes_child.start,
                                active_nodes_child.start+k-1, string, j+1)
                new_node_child = Node(start_rem_path+k, i, string, -1)
                new_node.add_child(new_node_child, string)
                active_nodes_child.start += k
                new_node.add_child(active_nodes_child, string)
                active_node.add_child(new_node, string)

                # resolve suffix link from previous iteration
                if node_needing_suffix_link is not None:
                    node_needing_suffix_link.suffix_link = new_node
                    node_needing_suffix_link = None

                # add suffix link
                node_needing_suffix_link = new_node
            else:
                # Rule 3
                if node_needing_suffix_link is not None:
                    node_needing_suffix_link.suffix_link = active_node
                    node_needing_suffix_link = None
        
        print('finish i,j')


def build_suffix_tree(string: str):
    n = len(string)
    root = Node(0, -1, string, -1)
    root.suffix_link = root
    for i in range(n):
        insert_letter(root, i, string)
    return root

def build_suffix_array(root: Node, n: int):
    suf_arr: List[int] = [-1] * n
    visited = []
    stack = [root]
    while stack:
        cur_node = stack.pop(0)
        visited.append(cur_node)
        children: List[Node] = []
        for child in cur_node.children:
            if child is not None:
                children.insert(0, child)
        stack += children
        


if __name__ == '__main__':
    s = 'babcbd'
    s += '$'
    root = build_suffix_tree(s)
    print(root.myprint())
    suf_arr = build_suffix_array(root, len(s))
    print(suf_arr)
