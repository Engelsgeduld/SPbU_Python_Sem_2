import random
from typing import Any, Callable, Generic, Iterable, Iterator, MutableMapping, Optional, TypeVar

Value = TypeVar("Value")
Key = TypeVar("Key")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.value: Value = value
        self.key: Key = key
        self.prior: float = random.random()
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    @staticmethod
    def inner_merge(
        left_node: Optional["Node[Any, Any]"], right_node: Optional["Node[Any, Any]"]
    ) -> Optional["Node[Any, Any]"]:
        if left_node is None:
            return right_node
        if right_node is None:
            return left_node
        if left_node.prior > right_node.prior:
            left_node.right = Node.inner_merge(left_node.right, right_node)
            return left_node
        else:
            right_node.left = Node.inner_merge(left_node, right_node.left)
            return right_node

    @staticmethod
    def inner_split(
        node: Optional["Node[Any, Any]"], key: Key
    ) -> tuple[Optional["Node[Any, Any]"], Optional["Node[Any, Any]"]]:
        if node is None:
            return None, None
        if node.key < key:
            first_root, second_root = Node.inner_split(node.right, key)
            node.right = first_root
            return node, second_root
        else:
            first_root, second_root = Node.inner_split(node.left, key)
            node.left = second_root
            return first_root, node

    @staticmethod
    def recursion_finding_node(
        original_node: Optional["Node[Any, Any]"], node: Optional["Node[Any, Any]"], key: Key
    ) -> Optional[tuple["Node[Any, Any]", "Node[Any, Any]"]]:
        if node is None or original_node is None:
            return None
        if node.key == key:
            return node, original_node
        if node.key > key:
            return Node.recursion_finding_node(node, node.left, key)
        if node.key < key:
            return Node.recursion_finding_node(node, node.right, key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and (self.key, self.value) == (other.key, other.value)

    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value})"

    def recursion_repr(self) -> str:
        left_children = self.left.recursion_repr() if self.left else None
        right_children = self.right.recursion_repr() if self.right else None
        return f"Node({self.key}, {self.value}, left:{left_children}, right:{right_children})"


class Treap(MutableMapping, Generic[Key, Value]):
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    def _merge(self, right_tree: "Treap") -> None:
        if self.root is None:
            self.root = right_tree.root
        else:
            self.root = self.root.inner_merge(self.root, right_tree.root)

    def _split(self, value: Key | object) -> tuple["Treap", "Treap"]:
        tree: "Treap" = Treap()
        if self.root is None:
            return self, tree
        roots = self.root.inner_split(self.root, value)
        self.root = roots[0]
        tree.root = roots[1]
        return self, tree

    def __setitem__(self, key: Key, value: Value) -> None:
        key_type = type(self.root.key) if self.root else object
        if not isinstance(key, key_type):
            raise KeyError(f"Key must be same type as Tree key type:{key_type}")
        if key in self:
            raise KeyError("Key already exist")
        new_element: "Treap" = Treap()
        new_element.root = Node(key, value)
        first_tree, second_tree = self._split(key)
        first_tree._merge(new_element)
        first_tree._merge(second_tree)
        self.length += 1
        self.root = first_tree.root

    def __contains__(self, key: object) -> bool:
        return True if self.root and self.root.recursion_finding_node(self.root, self.root, key) else False

    def __getitem__(self, key: Key) -> Optional[Value]:
        if self.root is None:
            raise ValueError("Tree is empty")
        if not isinstance(key, type(self.root.key)):
            raise KeyError("Key type mismatch")
        key_node = self.root.recursion_finding_node(self.root, self.root, key)
        if key_node is None:
            raise KeyError(f"Key not found")
        return key_node[0].value

    def _iterator(self) -> Iterator[Value]:
        def _inorder_comparator(node: Node) -> Iterable[Node]:
            return filter(None, (node.left, node, node.right))

        keys = []

        def traverse_recursion(cur_node: Optional[Node], order_func: Callable) -> None:
            node_order = order_func(cur_node)
            for node in node_order:
                if node is not cur_node:
                    traverse_recursion(node, order_func)
                else:
                    keys.append(node.key)

        traverse_recursion(self.root, _inorder_comparator)
        return iter(keys)

    def __iter__(self) -> Iterator[Any]:
        return self._iterator()

    def __delitem__(self, key: Key) -> None:
        if self.root is None:
            raise IndexError("pop from empty tree")
        pair = self.root.recursion_finding_node(self.root, self.root, key)
        if pair is None:
            raise KeyError("Key not found")
        key_node, parent_node = pair
        new_node = key_node.inner_merge(key_node.left, key_node.right)
        if key_node == self.root:
            self.root = new_node
        elif parent_node.left == key_node:
            parent_node.left = new_node
        else:
            parent_node.right = new_node
        self.length -= 1

    def pop(self, key: Any, /, default: Any = None) -> Any:
        try:
            old_value: Any = self[key]
        except KeyError:
            return default
        del self[key]
        return old_value

    def clear(self) -> None:
        self.root = None
        self.length = 0

    def __str__(self) -> str:
        if self.root is None:
            return f"Treap(root: {self.root}, length: {len(self)})"
        return f"Treap(root: {self.root.recursion_repr()}, length: {len(self)})"

    def __repr__(self) -> str:
        return f"{self.__dict__}"
