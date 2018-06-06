from decoder.exceptions.exceptions import BadDecodeException


class Node:
    def __init__(self, level: int, value: str = "node"):
        self._value = value
        self._level = level
        self._left = None
        self._right = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: str) -> None:
        self._value = val

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
    def __init__(self, haff_amount_arr: [], haff_value_arr: [], ac_dc_class: int, haff_table_id: int):
        self._haff_amount_arr = haff_amount_arr
        self._haff_value_arr = haff_value_arr
        self._ac_dc_class = ac_dc_class
        self._haff_table_id = haff_table_id
        self._arr_of_nodes = []
        self._root = Node(0, "root")
        self._build_tree()

    @property
    def root(self):
        return self._root

    @property
    def ac_dc_class(self) -> int:
        return self._ac_dc_class

    @property
    def haff_table_id(self) -> int:
        return self._haff_table_id

    def _add_node(self, current_level, current_node: Node, new_node: Node):
        #   1=ok 2=bad, need to go to another branch

        if current_node.left is None:
            current_level += 1
            if current_level == new_node.level:
                current_node.left = new_node
                return 1
            elif current_level < new_node.level:
                current_node.left = Node(current_level)
                return self._add_node(current_level, current_node.left, new_node)
            else:
                return -2
        elif current_node is not None and current_node.left.value == "node":
            # try to go left
            current_level += 1
            result = self._add_node(current_level, current_node.left, new_node)
            if result == 1:
                return 1
            elif result == -2:
                # try to go right
                if current_node.right is None:
                    current_node.right = Node(current_level)
                result = self._add_node(current_level, current_node.right, new_node)
                return result
        elif current_node.right is None:
            current_level += 1
            if current_level == new_node.level:
                current_node.right = new_node
                return 1
            elif current_level < new_node.level:
                if current_node.right is None:
                    current_node.right = Node(current_level)
                current_node.right = Node(current_level)
                return self._add_node(current_level, current_node.right, new_node)
            else:
                return -2
        elif current_node is not None and current_node.right.value == "node":
            # try to go left
            current_level += 1
            result = self._add_node(current_level, current_node.right, new_node)
            if result == 1:
                return 1
            elif result == -2:
                # try to go right
                result = self._add_node(current_level, current_node.right, new_node)
                return result
        else:
            return -2

    def _parse_nodes(self):
        current_level = 1
        current_index_for_val = 0  # 0...15 для количества

        for i in range(0, len(self._haff_amount_arr)):
            amount_of_nodes_on_cur_level = int(self._haff_amount_arr[i], 16)

            for i in range(0 , amount_of_nodes_on_cur_level):
                value = self._haff_value_arr[current_index_for_val]
                node = Node(current_level, value)
                self._arr_of_nodes.append(node)
                current_index_for_val += 1

            current_level += 1

    def _build_tree(self):
        self._parse_nodes()
        for i in range(0, len(self._arr_of_nodes)):
            node = self._arr_of_nodes[i]
            self._add_node(0, self.root, node)  # передаю current_level чтобы начать рекурсию

    def get_value_by_code(self, code: str):
        current_node = self.root
        for c in code:
            if c == "0" and current_node.left is not None:
                current_node = current_node.left
            elif c == "0" and current_node.left is None:
                return current_node
            if c == "1" and current_node.right is not None:
                current_node = current_node.right
            elif c == "1" and current_node.right is None:
                return current_node
        return current_node

    def get_next_value(self, code: str, arr_for_index: []):
        f_index = arr_for_index[0]
        index = arr_for_index[0]
        current_node = self.root
        while index < len(code):
            c = code[index]
            if c == "0" and current_node.left is not None:
                current_node = current_node.left
            elif c == "0" and current_node.left is None:
                # index -= 1
                arr_for_index[0] = index
                return current_node, code[f_index: arr_for_index[0]]
            elif c == "1" and current_node.right is not None:
                current_node = current_node.right
            elif c == "1" and current_node.right is None:
                # index -= 1
                arr_for_index[0] = index
                return current_node, code[f_index: arr_for_index[0]]
            else:
                raise BadDecodeException
            index += 1

    def get_next_n_bits(self, code: str, arr_for_index: [], n: int):
        index = arr_for_index[0]
        counter = 0
        current_code = ""
        while counter < n:
            c = code[index]
            current_code += c
            index += 1
            counter += 1

        arr_for_index[0] = index
        return current_code
