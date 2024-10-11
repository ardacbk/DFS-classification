import pygame
from graph import Graph
from node import Node

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 30

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

graph = Graph()
nodes = [Node(1,120,100,(2,3))]

running = True
while running:
    for node in nodes:
        pygame.draw.circle(screen,WHITE,(node.pos_x,node.pos_y),RADIUS,0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
