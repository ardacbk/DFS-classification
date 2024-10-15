from graph import Graph
from node import Node
import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


graph = Graph()

graph.add_node(Node(0, 200, 400, [1, 2]))   # 0 düğümü, 1 ve 2 ile bağlı
graph.add_node(Node(1, 400, 200, [0, 3, 4]))# 1 düğümü, 0, 3 ve 4 ile bağlı
graph.add_node(Node(2, 400, 600, [0, 3]))   # 2 düğümü, 0 ve 3 ile bağlı
graph.add_node(Node(3, 600, 400, [1, 2, 5]))# 3 düğümü, 1, 2 ve 5 ile bağlı
graph.add_node(Node(4, 600, 100, [1]))      # 4 düğümü, sadece 1 ile bağlı
graph.add_node(Node(5, 800, 400, [3, 6, 7, 8])) # 5 düğümü, 3, 6, 7 ve 8 ile bağlı
graph.add_node(Node(6, 800, 600, [5]))      # 6 düğümü, sadece 5 ile bağlı
graph.add_node(Node(7, 1000, 600, [5,8]))     # 7 düğümü, sadece 5 ile bağlı
graph.add_node(Node(8, 1000, 300, [5, 7, 9]))  # 8 düğümü, 5 ve 9 ile bağlı
graph.add_node(Node(9, 1200, 300, [8]))     # 9 düğümü, sadece 8 ile bağlı

graph.DFS(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
