
from __future__ import annotations
from dataclasses import dataclass
from auto_trans.utils import Utils
from typing import List, Optional


@dataclass
class Node:
    syllable: str
    left: Optional[Node] = None
    right: Optional[Node] = None


class Tree:
    

    def __init__(self, util:Utils) -> None:
        self.root: Optional[Node] = None
        self._leaves: List[str] = []
        self.util = util
        
    def add(self, syllable: str) :

        self.root = self._addNode(self.root, syllable)
    
    def _addNode(self, node: Optional[Node], syllable: str) -> Optional[Node]:

        if syllable:
            node = Node(syllable)
            left, right = self.util.syllabify(node.syllable)
            node.left = Node(left)
            node.right = self._addNode(node.right, right)
        
        return node
        
    def create(self, syllable: str):
        self.add(syllable)



    def display(self):
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node: Optional[Node]):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""

    
        # No child.
        if node.right is None and node.left is None:
            line = f"{node.syllable}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            s = f"{node.syllable}"
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            s = f"{node.syllable}"
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x =  self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = f"{node.syllable}"
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
    def _get_leaves(self, node: Optional[Node]) -> List[str]:
       
        # If node is null, return
        if (not node):
            return self._leaves
    
        # If node is leaf node,
        # print its data
        if (not node.left and
            not node.right):
            self._leaves.append(node.syllable)
        
        # If left child exists,
        # check for leaf recursively
        if node.left:
            self._get_leaves(node.left)
    
        # If right child exists,
        # check for leaf recursively
        if node.right:
            self._get_leaves(node.right)

        return self._leaves

    def get_leaves(self):
        return self._get_leaves(self.root)

if __name__ == "__main__":
    pass

