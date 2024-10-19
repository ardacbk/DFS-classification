from graph import Graph
from node import Node
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1920, 960))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_button(screen, x, y, w, h, text):
    pygame.draw.rect(screen, (0, 200, 0), (x, y, w, h))
    pygame.draw.rect(screen, (0, 255, 0), (x, y, w, h), 3)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

def button_click(x, y, w, h, pos):
    return x < pos[0] < x + w and y < pos[1] < y + h



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen before drawing the graph and button

    graph = Graph()

    # graph.add_node(Node(0, 100, 400, [1, 3, 4]))  # Node A
    # graph.add_node(Node(1, 400, 200, [5]))  # Node B
    # graph.add_node(Node(2, 400, 350, [1]))  # Node C
    # graph.add_node(Node(3, 400, 500, [2, 7]))  # Node D
    # graph.add_node(Node(4, 400, 700, [7]))  # Node E
    # graph.add_node(Node(5, 700, 250, [6, 8]))  # Node F
    # graph.add_node(Node(6, 700, 400, [1, 2]))  # Node G
    # graph.add_node(Node(7, 700, 600))  # Node H
    # graph.add_node(Node(8, 900, 400, [7]))  # Node I


    # graph.add_node(Node(0, 100, 400, [1, 2, 3]))  # Node a, connected to b, d, e (1, 3, 4)
    # graph.add_node(Node(1, 300, 200, [2,6]))        # Node b, connected to c (2)
    # graph.add_node(Node(2, 500, 200))             # Node c, no outgoing connections
    # graph.add_node(Node(3, 300, 600, [4,5]))      # Node d, connected to e (4, 5)
    # graph.add_node(Node(4, 500, 600, [2,0]))      # Node e, connected to c and f (2, 5)
    # graph.add_node(Node(5, 700, 400, []))         # Node f, no outgoing connections

    graph.add_node(Node(0, 300, 100, [2, 3]))  # Node S
    graph.add_node(Node(1, 700, 150, [5,6]))  # Node T
    graph.add_node(Node(2, 300, 250, [3,4]))  # Node Z
    graph.add_node(Node(3, 400, 350, [7]))  # Node W
    graph.add_node(Node(4, 100, 300, [7]))  # Node Y
    graph.add_node(Node(5, 550, 200, [0,3]))  # Node V
    graph.add_node(Node(6, 700, 350, [1,5]))  # Node U
    graph.add_node(Node(7, 100, 450, [2]))  # Node X

    graph.DFS(screen)
    graph.draw_graph(screen)

    # Show the button
    draw_button(screen, 840, 850, 240, 50, 'Tekrar Baslat')

    # Check for button click
    button_shown = True
    while button_shown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                button_shown = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_click(840, 850, 240, 50, pygame.mouse.get_pos()):
                    button_shown = False

        pygame.display.flip()
        clock.tick(60)

    pygame.display.update()  # Update display outside of the button loop
    clock.tick(60)

pygame.quit()