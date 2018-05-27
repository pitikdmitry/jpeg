from pydot import *


class TreeUtils:
    def __init__(self):
        self.counter = 0

    def save_tree(self, tree):
        graph = Dot(graph_type='graph')
        # pre_order(tree.root)
        # print("")
        self.pre_order_tree(tree.root, graph)
        print("")
        type = ""
        if tree.ac_dc_class == 0:
            type = "dc_"
        else:
            type = "ac_"

        id = str(tree.haff_table_id)
        graph.write_png('trees/tree_' + type + id + '.png')

    def pre_order_tree(self, node, graph):
        if node is None:
            return
        print(node.value, end=" ")
        if node.left is not None:
            if node.value == "node":
                node.value += str(self.counter)
                self.counter += 1
            if node.left.value == "node":
                node.left.value += str(self.counter)
                self.counter += 1
            edge = Edge(node.value, node.left.value)
            graph.add_edge(edge)
            self.pre_order_tree(node.left, graph)
        if node.right is not None:
            if node.value == "node":
                node.value += str(self.counter)
                self.counter += 1
            if node.right.value == "node":
                node.right.value += str(self.counter)
                self.counter += 1
            edge = Edge(node.value, node.right.value)
            graph.add_edge(edge)
            self.pre_order_tree(node.right, graph)
