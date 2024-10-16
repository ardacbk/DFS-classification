import math
import pygame
from fontTools.misc.classifyTools import classify

from node import Node
from edge import Edge

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TREE = (144, 238, 144)       # Pastel Green (Tree edges)
FORWARD = (102, 178, 255)    # Light Sky Blue (Forward edges)
BACK = (186, 85, 211)        # Medium Orchid (Back edges)
CROSS = (255, 165, 79)       # Light Orange (Cross edges)
CURRENT_COLOR = (255, 255, 153)  # Light Yellow (Current node)
FINISHED_COLOR = (255, 102, 102) # Light Coral (Finished node)

RADIUS = 30

def draw_text(screen, text, position, color):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def draw_arrow(screen, start, end, color, arrow_size=20, arrow_angle=30, offset=10):
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    start_adjusted = (
        start[0] + RADIUS * math.cos(angle) + offset * math.sin(angle),
        start[1] + RADIUS * math.sin(angle) - offset * math.cos(angle)
    )
    end_adjusted = (
        end[0] - RADIUS * math.cos(angle) + offset * math.sin(angle),
        end[1] - RADIUS * math.sin(angle) - offset * math.cos(angle)
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
        self.time = 0

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def draw_graph(self, screen):
        screen.fill(BLACK)
        for node in self.nodes:
            if node.state == Node.UNVISITED:
                pygame.draw.circle(screen, WHITE, (node.pos_x, node.pos_y), RADIUS, 0)
                draw_text(screen, str(node.id), (node.pos_x, node.pos_y), BLACK)
            elif node.state == Node.FINISHED:
                pygame.draw.circle(screen, FINISHED_COLOR, (node.pos_x, node.pos_y), RADIUS, 0)
                draw_text(screen, str(node.id), (node.pos_x, node.pos_y), WHITE)
            elif node.state == Node.CURRENT:
                pygame.draw.circle(screen, CURRENT_COLOR, (node.pos_x, node.pos_y), RADIUS, 0)
                draw_text(screen, str(node.id), (node.pos_x, node.pos_y), BLACK)
            time_str = str(node.start_time)+"/"+str(node.end_time)
            draw_text(screen, time_str, (node.pos_x-15, node.pos_y -50), WHITE)


            for edge in node.edges:
                if edge.type == Edge.TREE:
                    color = TREE # Tree edges are green
                elif edge.type == Edge.BACK:
                    color = BACK  # Back edges are red
                elif edge.type == Edge.FORWARD:
                    color = FORWARD  # Forward edges are blue
                elif edge.type == Edge.CROSS:
                    color = CROSS  # Cross edges are yellow
                else:
                    color = WHITE  # Default color for unknown edges
                draw_arrow(screen, (node.pos_x, node.pos_y), (self.nodes[edge.dest].pos_x, self.nodes[edge.dest].pos_y), color)

        pygame.draw.circle(screen, TREE, (1200, 20), 13)
        draw_text(screen, "Tree Edge", (1300, 20), WHITE)

        pygame.draw.circle(screen, BACK, (1200, 50), 13)
        draw_text(screen, "Back Edge", (1300, 50), WHITE)


        pygame.draw.circle(screen, FORWARD, (1200, 80), 13)
        draw_text(screen, "Forward Edge", (1300, 80), WHITE)


        pygame.draw.circle(screen, CROSS, (1200, 110), 13)
        draw_text(screen, "Cross Edge", (1300, 110), WHITE)

    def DFS(self, screen):
        self.time = 0
        self.traversal_array = []

        for node in self.nodes:
            if not node.visited:
                self.traverse_dfs(node, screen)

        print("DFS Traversal:", self.traversal_array)
        self.classify_edges(self.nodes[0], screen)

    def classify_edges(self,node,screen):
        for edge in node.edges:
            neighbor = self.nodes[edge.dest]
            if edge.type == Edge.TREE:
                self.classify_edges(neighbor,screen)
            elif node.start_time < neighbor.start_time and node.end_time > neighbor.end_time:
                edge.type = Edge.FORWARD
                print('Forward Edge:', f"{node.id} --> {neighbor.id}")
            elif node.start_time > neighbor.start_time and node.end_time > neighbor.end_time:
                edge.type = Edge.CROSS
                print('Cross Edge:', f"{node.id} --> {neighbor.id}")
            elif node.start_time > neighbor.start_time and node.end_time < neighbor.end_time:
                edge.type = Edge.BACK
                print('Back Edge:', f"{node.id} --> {neighbor.id}")
            self.draw_graph(screen)
            pygame.display.update()
            pygame.time.wait(500)



    def traverse_dfs(self, node, screen):
        node.state = Node.CURRENT
        node.visited = True
        self.traversal_array.append(node.id)
        node.start_time = self.time
        self.time += 1
        self.draw_graph(screen)
        pygame.display.update()
        pygame.time.wait(500)

        for adj in node.connected_nodes:
            if not self.nodes[adj].visited:
                # Tree edge
                for edge in node.edges:
                    if edge.dest == adj:
                        edge.set_type(Edge.TREE)
                        break
                print('Tree Edge:', f"{node.id} --> {adj}")
                self.traverse_dfs(self.nodes[adj], screen)
            # else:
            #     # Classifying edges: Back, Forward, or Cross
            #     for edge in node.edges:
            #         if edge.dest == adj:
            #             if self.start_time[adj] < self.start_time[node.id] and ((self.end_time[node.id] < self.end_time[adj]) or (self.end_time[node.id] == -1 and self.end_time[adj]==-1) ):
            #                 edge.set_type(Edge.BACK)
            #                 print('Back Edge:', f"{node.id} --> {adj}")
            #             elif self.start_time[adj] > self.start_time[node.id] and ((self.end_time[node.id] > self.end_time[adj]) or self.end_time[node.id] == 0):
            #                 edge.set_type(Edge.FORWARD)
            #                 print('Forward Edge:', f"{node.id} --> {adj}")
            #             elif self.start_time[node.id] > self.start_time[adj] and self.end_time[node.id] > self.end_time[adj]:
            #                 edge.set_type(Edge.CROSS)
            #                 print('Cross Edge:', f"{node.id} --> {adj}")
            #             break

        node.state = Node.FINISHED
        node.end_time = self.time
        self.time += 1
        self.draw_graph(screen)
        pygame.display.update()
        pygame.time.wait(500)
