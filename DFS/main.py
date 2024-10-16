from graph import Graph
from node import Node
import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()


graph = Graph()

#
# graph.add_node(Node(0, 200, 400, [1, 2, 3]))  # Node a, connected to b, d, e (1, 3, 4)
# graph.add_node(Node(1, 400, 200, [2]))        # Node b, connected to c (2)
# graph.add_node(Node(2, 600, 200))     # Node c, connected to b and f (1, 5)
# graph.add_node(Node(3, 400, 600, [4,5]))        # Node d, connected to e (4)
# graph.add_node(Node(4, 600, 600, [2,0]))     # Node e, connected to c and f (2, 5)
# graph.add_node(Node(5, 800, 400, []))         # Node f, no outgoing edges
#

# Nodes (A: 0, B: 1, C: 2, D: 3, E: 4, F: 5, G: 6, H: 7, I: 8)

graph.add_node(Node(0, 200, 400,[1,3,4]))  # Node A
graph.add_node(Node(1, 500, 200,[5]))  # Node B
graph.add_node(Node(2, 500, 350,[1]))  # Node C
graph.add_node(Node(3, 500, 500,[2,7]))  # Node D
graph.add_node(Node(4, 500, 700,[7]))  # Node E
graph.add_node(Node(5, 800, 250,[6,8]))  # Node F
graph.add_node(Node(6, 800, 400,[1,2]))  # Node G
graph.add_node(Node(7, 800, 600))  # Node H
graph.add_node(Node(8, 1000, 400,[7]))  # Node I


graph.DFS(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
