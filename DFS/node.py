from edge import Edge

class Node:
    FINISHED = "finished"
    UNVISITED = "unvisited"
    CURRENT = "current"
    def __init__(self, id, pos_x, pos_y,connected_nodes=None):
        self.id = id
        self.pos_x = pos_x
        self.edges = []
        self.pos_y = pos_y
        self.visited = False
        if connected_nodes == None:
            connected_nodes = []
        self.connected_nodes = connected_nodes
        for connected_id in self.connected_nodes:
            self.edges.append(Edge(id,connected_id))
        self.state = Node.UNVISITED
        self.start_time = -1
        self.end_time = -1