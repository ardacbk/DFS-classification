class Edge:
    UNDISCOVERED = "undiscovered"
    TREE = "tree"
    FORWARD = "forward"
    BACK = "back"
    CROSS = "cross"

    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.type = Edge.UNDISCOVERED
    def set_type(self, edge_type):
        self.type = edge_type