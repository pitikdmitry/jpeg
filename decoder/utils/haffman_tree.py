from decoder.exceptions.exceptions import HaffmanException


class Node:
    def __init__(self, level: int, value: int = -1):
        self._value = value
        self._level = level
        self._left = None
        self._right = None

    @property
    def value(self):
        return self._value

    @property
    def level(self):
        return self._level

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, node: "Node") -> None:
        self._left = node

    @right.setter
    def right(self, node: "Node") -> None:
        self._right = node


class HaffmanTree:
    def __init__(self, haff_arr_bytes: []):
        self._arr = haff_arr_bytes
        self._arr_of_nodes = []
        self._build_tree()
        self._root = Node(0)

    @property
    def root(self):
        return self._root

    def _add_node(self, current_level, current_node: Node, new_node: Node):
        #   1=ok 2=bad, need to go to another branch
        if current_node.left is None:
            current_level += 1
            if current_level == new_node.level:
                current_node.left = new_node
                return 1
            else:
                current_node.left = Node(current_level)
                return self._add_node(current_level, current_node.left, new_node)
        elif current_node is not None and current_node.left.value == -1:
            # try to go left
            current_level += 1
            result = self._add_node(current_level, current_node.left, new_node)
            if result == 1:
                return 1
            elif result == -2:
                # try to go right
                result = self._add_node(current_level, current_node.right, new_node)
                return result
        elif current_node.right is None:
            current_level += 1
            if current_level == new_node.level:
                current_node.right = new_node
                return 1
            else:
                current_node.right = Node(current_level)
                return self._add_node(current_level, current_node.right, new_node)
        elif current_node is not None and current_node.right.value == -1:
            # try to go left
            current_level += 1
            result = self._add_node(current_level, current_node.left, new_node)
            if result == 1:
                return 1
            elif result == -2:
                # try to go right
                result = self._add_node(current_level, current_node.right, new_node)
                return result
        else:
            return -2



    def _parse_nodes(self):
        amount_of_nodes = 16
        current_level = 1
        current_index_for_val = 16  # 0...15 для количества

        for i in range(0, amount_of_nodes):
            amount_of_nodes_on_cur_level = int(self._arr[i], 16)

            for i in range(0 , amount_of_nodes_on_cur_level):
                value = int(self._arr[current_index_for_val], 16)
                node = Node(current_level, value)
                self._arr_of_nodes.append(node)
                current_index_for_val += 1

            current_level += 1

    def _build_tree(self):
        self._parse_nodes()
        for i in range(0, len(self._arr_of_nodes)):
            node = self._arr_of_nodes[i]
            self._add_node(0, self.root, node)
