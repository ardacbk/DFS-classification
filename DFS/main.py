import pygame
from graph import Graph
from node import Node
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RADIUS = 30


def draw_text(screen, text, position, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_arrow(screen, start, end, color, arrow_size=20, arrow_angle=30):

    pygame.draw.line(screen, color, start, end, 3)


    angle = math.atan2(end[1] - start[1], end[0] - start[0])


    left_wing = (end[0] - arrow_size * math.cos(angle - math.radians(arrow_angle)),
                 end[1] - arrow_size * math.sin(angle - math.radians(arrow_angle)))
    right_wing = (end[0] - arrow_size * math.cos(angle + math.radians(arrow_angle)),
                  end[1] - arrow_size * math.sin(angle + math.radians(arrow_angle)))


    pygame.draw.polygon(screen, color, [end, left_wing, right_wing])

def adjust_end_for_circle(start, end, radius):

    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    adjusted_end = (
        end[0] - radius * math.cos(angle),
        end[1] - radius * math.sin(angle)
    )

    return adjusted_end

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

graph = Graph()

nodes = [Node(0,250,200,[1,2]),
         Node(1,1000,200,[0]),
         Node(2,250,600),
         Node(3,1000,600,[1,2])]

# nodes = [Node(0, 250, 200, (1, 2)),
#          Node(1, 550, 500),
#          Node(2, 350, 450)]

font = pygame.font.Font(None, 36)

running = True

while running:
    screen.fill(BLACK)

    for node in nodes:
        pygame.draw.circle(screen, WHITE, (node.pos_x, node.pos_y), RADIUS, 0)
        for adj in tuple(node.connected_nodes):
            adjusted_end = adjust_end_for_circle(
                (node.pos_x, node.pos_y),
                (nodes[adj].pos_x, nodes[adj].pos_y),
                RADIUS
            )
            # Oku çiz
            draw_arrow(screen, (node.pos_x, node.pos_y), adjusted_end, WHITE)
        draw_text(screen,str(node.id),(node.pos_x, node.pos_y), BLACK)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
