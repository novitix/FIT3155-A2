# Student Name: Adam Ye
# Student ID: 31460798

from __future__ import annotations
from typing import List, Set, Dict, Tuple

TEST_STRING = "banbaddbac"


class Node:
    def __init__(self, start: int, end: int, child: Node = None, value: int = -1):
        self.start = start
        self.end = end
        self.children = [child] if child is not None else []
        self.value = value

    def __repr__(self):
        return TEST_STRING[self.start:self.end+1]

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def add_child(self, child):
        self.children.append(child)

    def get_active_node(self, j: int, i: int, string: str) -> Tuple[Node, int]:
        # find end of path denoting str[j..i] starting from this node
        active_node = self
        found_suffix = True
        while found_suffix:
            found_suffix = False
            for child in active_node.children:
                if string[j:i+1].startswith(string[child.start:child.end+1]):
                    j += child.end-child.start+1
                    active_node = child
                    found_suffix = True
                    break
        return [active_node, j]  # j points to start of remaining path str[j..i] that has not been matched yet


def insert_letter(root: Node, i: int, string: str):
    n = len(string)
    print('i=', str(i))
    for j in range(i+1):
        print('j=', str(j))
        active_node, start_rem_path = root.get_active_node(j, i, string)
        if active_node.is_leaf() and active_node != root:
            # Rule 1
            active_node.end += 1
        else:
            k = 0
            active_nodes_child = None
            for child in active_node.children:
                found = False
                while start_rem_path+k < n and string[child.start+k] == string[start_rem_path+k]:
                    k += 1
                    active_nodes_child = child
                    found = True
                if found:
                    break

            if k == 0:
                # Rule 2 (Alt)
                new_node = Node(start_rem_path, i)
                active_node.add_child(new_node)
            elif start_rem_path+k < i+1:
                # Rule 2 (Reg)
                # k points to 1st mismatch
                active_node.children.remove(active_nodes_child)
                new_node = Node(active_nodes_child.start, active_nodes_child.start+k-1)
                new_node_child = Node(start_rem_path+k, i, None)
                new_node.add_child(new_node_child)
                active_nodes_child.start += k
                new_node.add_child(active_nodes_child)
                active_node.add_child(new_node)
        print('finish i,j')


def build_suffix_tree(string: str):
    n = len(string)
    root = Node(0, -1)
    for i in range(n):
        insert_letter(root, i, string)
    return root


def print_tree(root: Node):
    # bfs
    visited = [root]
    queue = [root]
    while queue:
        cur = queue.pop(0)
        if cur is None:
            print('------------------')
        else:
            print(cur)
            for neighbour in root.children:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.append(neighbour)
            queue.append(None)  # marker


root = build_suffix_tree(TEST_STRING)
print_tree(root)
