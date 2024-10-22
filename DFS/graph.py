import math
import pygame
from node import Node
from edge import Edge
from forest import Forest
from forest import ForestNode

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TREE = (144, 238, 144)       # Pastel Green (Tree edges)
FORWARD = (102, 178, 255)    # Light Sky Blue (Forward edges)
BACK = (186, 85, 211)        # Medium Orchid (Back edges)
CROSS = (255, 165, 79)       # Light Orange (Cross edges)
CURRENT_COLOR = (255, 255, 153)  # Light Yellow (Current node)
FINISHED_COLOR = (255, 102, 102) # Light Coral (Finished node)

RADIUS = 30

FOREST_RADIUS = 20

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

def draw_curved_arrow(screen, start, end, color, arrow_size=20, arrow_angle=30, curvature=0.2, offset=10):
    # Başlangıç ve bitiş noktaları arasındaki açı
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    # Düğüm dışına ok eklemek için başlangıç ve bitiş noktalarını biraz ayarlıyoruz
    start_adjusted = (
        start[0] + RADIUS * math.cos(angle) + offset * math.sin(angle),
        start[1] + RADIUS * math.sin(angle) - offset * math.cos(angle)
    )
    end_adjusted = (
        end[0] - RADIUS * math.cos(angle) + offset * math.sin(angle),
        end[1] - RADIUS * math.sin(angle) - offset * math.cos(angle)
    )

    # Eğri için kontrol noktası (yumuşak bir bombe oluşturmak için)
    mid_x = (start_adjusted[0] + end_adjusted[0]) / 2
    mid_y = (start_adjusted[1] + end_adjusted[1]) / 2
    control_x = mid_x + curvature * (end_adjusted[1] - start_adjusted[1])
    control_y = mid_y - curvature * (end_adjusted[0] - start_adjusted[0])

    # Bezier eğrisi ile çizim
    points = []
    for t in range(101):
        t /= 100
        x = (1 - t) ** 2 * start_adjusted[0] + 2 * (1 - t) * t * control_x + t ** 2 * end_adjusted[0]
        y = (1 - t) ** 2 * start_adjusted[1] + 2 * (1 - t) * t * control_y + t ** 2 * end_adjusted[1]
        if t > 0:
            pygame.draw.line(screen, color, (prev_x, prev_y), (x, y), 3)
        prev_x, prev_y = x, y
        points.append((x, y))

    # Oku çizeceğimiz son iki nokta arasındaki açı
    if len(points) > 2:
        arrow_angle_direction = math.atan2(points[-1][1] - points[-2][1], points[-1][0] - points[-2][0])
    else:
        arrow_angle_direction = angle  # Default olarak eğer eğri kısa ise açıyı orijinal açıyla bırakırız.

    # Oku uca ekle
    left_wing = (end_adjusted[0] - arrow_size * math.cos(arrow_angle_direction - math.radians(arrow_angle)),
                 end_adjusted[1] - arrow_size * math.sin(arrow_angle_direction - math.radians(arrow_angle)))
    right_wing = (end_adjusted[0] - arrow_size * math.cos(arrow_angle_direction + math.radians(arrow_angle)),
                  end_adjusted[1] - arrow_size * math.sin(arrow_angle_direction + math.radians(arrow_angle)))

    pygame.draw.polygon(screen, color, [end_adjusted, left_wing, right_wing])


class Graph:
    def __init__(self):
        self.nodes = []
        self.time = 0
        self.forest = Forest()

    def add_node(self, node):
        self.nodes.append(node)

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

        pygame.draw.circle(screen, TREE, (1700, 20), 13)
        draw_text(screen, "Tree Edge", (1800, 20), WHITE)

        pygame.draw.circle(screen, BACK, (1700, 50), 13)
        draw_text(screen, "Back Edge", (1800, 50), WHITE)


        pygame.draw.circle(screen, FORWARD, (1700, 80), 13)
        draw_text(screen, "Forward Edge", (1800, 80), WHITE)


        pygame.draw.circle(screen, CROSS, (1700, 110), 13)
        draw_text(screen, "Cross Edge", (1800, 110), WHITE)

        self.draw_forest(screen)

    def draw_forest(self, screen):
        for node in self.forest.nodes:
            pygame.draw.circle(screen, FINISHED_COLOR, (node.pos_x, node.pos_y), FOREST_RADIUS, 0)
            draw_text(screen, str(node.id), (node.pos_x, node.pos_y), WHITE)
            for child in node.children:
                draw_arrow(screen, (node.pos_x, node.pos_y), (child.pos_x, child.pos_y), TREE, 10)
            for back_node in node.back_nodes:
                draw_curved_arrow(screen, (node.pos_x, node.pos_y), (back_node.pos_x, back_node.pos_y),BACK,10)
            for forward_node in node.forward_nodes:
                draw_curved_arrow(screen, (node.pos_x, node.pos_y), (forward_node.pos_x, forward_node.pos_y),FORWARD,10)
            for cross_node in node.cross_nodes:
                draw_curved_arrow(screen, (node.pos_x, node.pos_y), (cross_node.pos_x, cross_node.pos_y),CROSS,10)
    def DFS(self, screen):
        self.time = 0
        self.traversal_array = []
        forest_root = ForestNode(self.nodes[0].id,1400,150,None)
        self.forest.add_root(forest_root)
        for node in self.nodes:
            if not node.visited:
                self.traverse_dfs(node, screen)
        print("DFS Traversal:", self.traversal_array)
        self.classify_edges(self.nodes[0], screen)

    def classify_edges(self,node,screen):
        for node in self.nodes:
            for edge in node.edges:
                neighbor = self.nodes[edge.dest]
                if edge.type == Edge.TREE:
                    continue
                elif node.start_time < neighbor.start_time and node.end_time > neighbor.end_time:
                    edge.type = Edge.FORWARD
                    print('Forward Edge:', f"{node.id} --> {neighbor.id}")
                    self.forest.add_forward_node(node.id,neighbor.id)
                elif node.start_time > neighbor.start_time and node.end_time > neighbor.end_time:
                    edge.type = Edge.CROSS
                    self.forest.add_cross_node(node.id,neighbor.id)
                    print('Cross Edge:', f"{node.id} --> {neighbor.id}")
                elif node.start_time > neighbor.start_time and node.end_time < neighbor.end_time:
                    edge.type = Edge.BACK
                    self.forest.add_back_node(node.id,neighbor.id)
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
                self.forest.add_tree_node(node.id,adj)
                self.traverse_dfs(self.nodes[adj], screen)

        node.state = Node.FINISHED
        node.end_time = self.time
        self.time += 1
        self.draw_graph(screen)
        pygame.display.update()
        pygame.time.wait(500)
