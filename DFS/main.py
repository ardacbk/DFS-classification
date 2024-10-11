from graph import Graph
from node import Node

graph = Graph()
nodes = []

for i in range(11):
    nodes.append(Node(i,100+i*10,100+i*3,[i+1,i-1]))
    graph.add_node(nodes[i])


for node in graph.nodes:
    print("Node id: "+ str(node.id) + "\nX,Y:" + str(node.pos_x) + "," + str(node.pos_y) + "\nConnected Nodes:" + str(node.connected_nodes))

