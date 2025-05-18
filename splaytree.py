class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None
        self.cache = {}

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_right(self, root):
        temp = root.left
        root.left = temp.right
        temp.right = root
        return temp

    def _rotate_left(self, root):
        temp = root.right
        root.right = temp.left
        temp.left = root
        return temp

    def insert(self, key, value):
        self.cache[key] = value
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
        elif key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            self.root = new_node
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            self.root = new_node

    def find(self, key):
        if key in self.cache:
            return self.cache[key]
        return None
