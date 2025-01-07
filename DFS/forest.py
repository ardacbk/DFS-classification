class ForestNode:
    def __init__(self,id,pos_x,pos_y,parent):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.children = []
        self.back_nodes = []
        self.cross_nodes = []
        self.forward_nodes = []
        self.max_width = 250
        self.parent = parent
class Forest:
    def __init__(self):
        self.nodes = []
        self.root = None

    def add_root(self, node):
        self.nodes.append(node)
        self.root = node

    def add_tree_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        if node1 is None:
            node1 = ForestNode(node1_id,self.nodes[0].pos_x + 200,self.nodes[0].pos_y,None)
            self.nodes.append(node1)
            node2 = ForestNode(node2_id, node1.pos_x - 50, node1.pos_y + 100, node1)  # Left child
            node1.children.append(node2)
            self.nodes.append(node2)
            self.handle_collision(node2)
            return
        if not node1.children : # Children listesi bos ise
            node2 = ForestNode(node2_id, node1.pos_x - 50, node1.pos_y + 100,node1) # Left child
            node1.children.append(node2)
            self.nodes.append(node2)
            self.handle_collision(node2)
        elif len(node1.children)==1:
            node2 = ForestNode(node2_id, node1.pos_x + 50, node1.pos_y + 100,node1) # Right child
            node1.children.append(node2)
            self.nodes.append(node2)
            self.handle_collision(node2)
        else:
            node2 = ForestNode(node2_id, node1.pos_x, node1.pos_y+100,node1)
            node1.children.append(node2)
            space = node1.max_width/(len(node1.children)-1)
            pos_x = node1.pos_x-(node1.max_width/2)
            for child in node1.children:
                child.pos_x = pos_x
                pos_x+=space
            self.nodes.append(node2)
            node1.max_width += 25
            self.adjust_positions(node1.id)
            self.handle_collision(node2)
    def add_back_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        if node1 is None or node2 is None:
            return
        node1.back_nodes.append(node2)
        self.nodes.append(node2)
    def add_forward_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        if node1 is None or node2 is None:
            return
        node1.forward_nodes.append(node2)
        self.nodes.append(node2)
    def add_cross_node(self,node1_id,node2_id):
        node1 = self.find_node(node1_id)
        node2 = self.find_node(node2_id)
        if node1 is None or node2 is None:
            return
        node1.cross_nodes.append(node2)
        self.nodes.append(node2)

    def find_node(self,id):
        for node in self.nodes:
            if node.id == id:
                return node
        else:
            print(f"Node {id} not found")
            return None
    def adjust_positions(self,id):
        stack = [self.find_node(id)]
        while stack:
            node = stack.pop()
            if len(node.children) > 2:
                space = node.max_width / (len(node.children) - 1)
                pos_x = node.pos_x - (node.max_width / 2)
                for child in node.children:
                    stack.append(child)
                    child.pos_x = pos_x
                    pos_x += space
            else:
                space = 100
                pos_x = node.pos_x - 50
                for child in node.children:
                    child.pos_x = pos_x
                    pos_x += space
                    stack.append(child)

    def handle_collision(self,node):
        if node.id==0: return
        for n in self.nodes:
            if n.id == node.id: continue
            if n.pos_x == node.pos_x and n.pos_y == node.pos_y:
                if(n.parent.pos_x > node.parent.pos_x):
                    n.pos_x += 20
                    node.pos_x -= 20
                else:
                    n.pos_x -= 20
                    node.pos_x += 20