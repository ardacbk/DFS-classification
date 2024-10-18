class ForestNode:
    def __init__(self,id,pos_x,pos_y):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.left = None
        self.right = None
        self.back_nodes = []
        self.cross_nodes = []
        self.forward_nodes = []

class Forest:
    def __init__(self):
        self.nodes = []
        self.root = None

    def add_root(self, node):
        self.nodes.append(node)
        self.root = node

    def add_tree_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        if node1.left is None:
            node2 = ForestNode(node2_id, node1.pos_x - 50, node1.pos_y + 100)
            node1.left = node2
            self.nodes.append(node2)
        else:
            node2 = ForestNode(node2_id, node1.pos_x + 50, node1.pos_y + 100)
            node1.right = node2
            self.nodes.append(node2)

    def add_back_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        node1.back_nodes.append(node2)
        self.nodes.append(node2)
    def add_forward_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        node1.forward_nodes.append(node2)
        self.nodes.append(node2)
    def add_cross_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        node1.cross_nodes.append(node2)
        self.nodes.append(node2)

    def find_node(self,id):
        for node in self.nodes:
            if node.id == id:
                return node
        else:
            print(f"Node {id} not found")
            return None