class Node:
    def __init__(self, id, pos_x, pos_y,connected_nodes=None):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        if connected_nodes == None:
            connected_nodes = []
        self.connected_nodes = connected_nodes
        self.visited = False
    def set_visited(self):
        self.visited = True