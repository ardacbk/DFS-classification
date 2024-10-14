from graph import Graph
from node import Node

graph = Graph()

graph.add_node(Node(0,250,200,[1,2]))
graph.add_node(Node(1,1000,200,[0]))
graph.add_node(Node(2,250,600))
graph.add_node(Node(3,1000,600,[1,2]))

nodes = graph.get_nodes()

graph.draw_graph()