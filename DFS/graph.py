import math
import pygame
from node import Node

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 30

def draw_text(screen, text, position, color):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_arrow(screen, start, end, color, arrow_size=20, arrow_angle=30):
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    start_adjusted = (
        start[0] + RADIUS * math.cos(angle),
        start[1] + RADIUS * math.sin(angle)
    )
    end_adjusted = (
        end[0] - RADIUS * math.cos(angle),
        end[1] - RADIUS * math.sin(angle)
    )
    pygame.draw.line(screen, color, start_adjusted, end_adjusted, 3)

    left_wing = (end_adjusted[0] - arrow_size * math.cos(angle - math.radians(arrow_angle)),
                 end_adjusted[1] - arrow_size * math.sin(angle - math.radians(arrow_angle)))
    right_wing = (end_adjusted[0] - arrow_size * math.cos(angle + math.radians(arrow_angle)),
                  end_adjusted[1] - arrow_size * math.sin(angle + math.radians(arrow_angle)))
    pygame.draw.polygon(screen, color, [end_adjusted, left_wing, right_wing])

class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def draw_graph(self, screen):
        screen.fill(BLACK)
        for node in self.nodes:
            if(node.state == Node.UNVISITED):
                pygame.draw.circle(screen, WHITE, (node.pos_x, node.pos_y), RADIUS, 0)
            elif (node.state == Node.VISITED):
                pygame.draw.circle(screen, (255, 0, 0), (node.pos_x, node.pos_y), RADIUS, 0)
            elif (node.state == Node.CURRENT):
                pygame.draw.circle(screen, (255,255,0), (node.pos_x, node.pos_y), RADIUS, 0)
            for adj in tuple(node.connected_nodes):
                draw_arrow(screen, (node.pos_x, node.pos_y), (self.nodes[adj].pos_x, self.nodes[adj].pos_y), WHITE)
            draw_text(screen, str(node.id), (node.pos_x, node.pos_y), BLACK)

    def DFS(self,screen):
        stack = [self.nodes[0]]
        while stack:
            node = stack.pop()
            if node.visited is False:
                print("Node " + str(node.id) + " is visited.")
                node.state = Node.VISITED
                node.visited = True
                self.draw_graph(screen)
                pygame.display.update()
                pygame.time.wait(500)
                for adj in tuple(node.connected_nodes):
                    if not self.nodes[adj].visited:
                        stack.append(self.nodes[adj])
                        self.nodes[adj].state = Node.CURRENT
