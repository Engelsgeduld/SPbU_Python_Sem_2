import random
from copy import deepcopy
from typing import TypeVar, MutableMapping, Iterable, Callable, Optional, Any, Generic, Iterator

Value = TypeVar("Value")
Key = TypeVar("Key")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.value: Value = value
        self.key: Key = key
        self.prior: float = random.random()
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Node) and (self.key, self.value) == (other.key, other.value)

    def __repr__(self) -> str:
        return f"Node({self.key}, {self.value}, left:{self.left}, right:{self.right})"


class Treap(MutableMapping):
    def __init__(self, key_type: type) -> None:
        self.root: Optional[Node] = None
        self.length: int = 0
        self.key_type: type = key_type

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def _inner_merge(left_node: Optional[Node], right_node: Optional[Node]) -> Optional[Node]:
        if left_node is None:
            return right_node
        if right_node is None:
            return left_node
        if left_node.prior > right_node.prior:
            left_node.right = Treap._inner_merge(left_node.right, right_node)
            return left_node
        else:
            right_node.left = Treap._inner_merge(left_node, right_node.left)
            return right_node

    def _merge(self, right_tree: "Treap") -> "Treap":
        new_tree: "Treap" = Treap(self.key_type)
        new_tree.root = Treap._inner_merge(self.root, right_tree.root)
        return new_tree

    @staticmethod
    def _inner_split(root: Optional[Node], key: Key) -> tuple[Optional[Node], Optional[Node]]:
        if root is None:
            return None, None
        if root.key < key:
            first_root, second_root = Treap._inner_split(root.right, key)
            root.right = first_root
            return root, second_root
        else:
            first_root, second_root = Treap._inner_split(root.left, key)
            root.left = second_root
            return first_root, root

    def _split(self, value: object) -> tuple["Treap", "Treap"]:
        trees: tuple["Treap", "Treap"] = Treap(self.key_type), Treap(self.key_type)
        roots = Treap._inner_split(self.root, value)
        trees[0].root = roots[0]
        trees[1].root = roots[1]
        return trees

    def __setitem__(self, key: object, value: object) -> None:
        if not isinstance(key, self.key_type):
            raise KeyError(f"Key must be same type as Tree key type:{self.key_type}")
        if key in self:
            raise KeyError("Key already exist")
        new_element: "Treap" = Treap(self.key_type)
        new_element.root = Node(key, value)
        first_tree, second_tree = self._split(key)
        first_tree = first_tree._merge(new_element)
        first_tree = first_tree._merge(second_tree)
        self.length += 1
        self.root = first_tree.root

    def __contains__(self, key: object) -> bool:
        try:
            Treap._recursion_finding_node(self.root, key, self.root)
            return True
        except KeyError:
            return False

    @staticmethod
    def _recursion_finding_node(
        node: Optional[Node], key: object, parent_node: Optional[Node]
    ) -> Optional[tuple[Node[Any, Any], Node[Any, Any]]]:
        if node is None or parent_node is None:
            raise KeyError("Key not found")
        if node.key == key:
            return node, parent_node
        if node.key > key:
            return Treap._recursion_finding_node(node.left, key, node)
        if node.key < key:
            return Treap._recursion_finding_node(node.right, key, node)

    def __getitem__(self, key: Key) -> Optional[Value]:
        if not isinstance(key, self.key_type):
            raise KeyError("Key type mismatch")
        key_node = self._recursion_finding_node(self.root, key, self.root)
        if key_node is None:
            raise KeyError("Key not found")
        return key_node[0].value

    def get(self, key: object, default: Any = None) -> Optional[Value]:
        try:
            return self[key]
        except KeyError:
            return default

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
        pair = self._recursion_finding_node(self.root, key, self.root)
        if pair is None:
            raise KeyError("Key not found")
        key_node, parent_node = pair
        new_node = self._inner_merge(deepcopy(key_node.left), deepcopy(key_node.right))
        if key_node == self.root:
            self.root = self._inner_merge(self.root.left, self.root.right)
        elif parent_node.left == key_node:
            parent_node.left = new_node
        else:
            parent_node.right = new_node
        self.length -= 1

    def pop(self, __key: Any, /, default: Any = None) -> Any:
        try:
            old_value: Any = self[__key]
            del self[__key]
        except KeyError:
            return default
        return old_value

    def clear(self) -> None:
        self.root = None
        self.length = 0

    def __str__(self) -> str:
        return f"{self.items()}"

    def __repr__(self) -> str:
        return f"{self.__dict__}"
