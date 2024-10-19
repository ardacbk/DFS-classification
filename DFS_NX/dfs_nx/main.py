import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

TREE = 'green'
FORWARD = 'blue'
BACK = 'purple'
CROSS = 'orange'

G = nx.DiGraph()
G.add_edges_from([(0, 1), (0,3), (3, 4), (4, 2), (0, 2), (3, 5), (1, 2), (4, 0)])

node_status = {node: "unvisited" for node in G.nodes()}
discovery_time = {}
finish_time = {}
edge_classification = {}
time = 0
pos = nx.spring_layout(G)

fig, ax = plt.subplots()
colors = []

# Keşif zamanlarını hesapla
def dfs_visit(node):
    global time
    discovery_time[node] = time
    node_status[node] = "current"
    time += 1
    yield draw_graph()

    for neighbor in G.neighbors(node):
        if node_status[neighbor] == "unvisited":
            edge_classification[(node, neighbor)] = "tree"  # Ağaç kenarı olarak sınıflandır
            yield from dfs_visit(neighbor)
        # Burada finish_time henüz güncellenmediği için sadece ağaç kenarını işliyoruz

    node_status[node] = "finished"
    finish_time[node] = time # Finish time'ları da hesapla
    time += 1
    yield draw_graph()

# Kenarları sınıflandır
def classify_edges():
    for edge in G.edges():
        u, v = edge
        if edge_classification.get((u, v)) == "tree":
            continue  # Tree edges zaten sınıflandırıldı
        
        # Discovery ve finish zamanlarına göre sınıflandırma yap
        if discovery_time[u] < discovery_time[v] and finish_time[u] > finish_time[v]:
            edge_classification[(u,v)] = "forward"
        elif discovery_time[u] > discovery_time[v] and finish_time[u] > finish_time[v]:
            edge_classification[(u,v)] = "cross"
        elif discovery_time[u] > discovery_time[v] and finish_time[u] < finish_time[v]:
            edge_classification[(u,v)] = "back"

def draw_graph():
    ax.clear()
    
    # Nodeların renklendirmesi
    node_colors = ['yellow' if node_status[n] == 'current' else 'green' if node_status[n] == 'finished' else 'grey' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax, node_size=700)
    
    # Edgelerin renklendirmesi
    edge_colors = [TREE if edge_classification.get(e) == "tree" else FORWARD if edge_classification.get(e) == "forward"
                   else BACK if edge_classification.get(e) == "back" else CROSS for e in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, ax=ax, connectionstyle='arc3,rad=0.1', width=2)
    
    # Node Yazıları
    nx.draw_networkx_labels(G, pos, font_color='black', font_size=10, ax=ax)

    ax.set_title('DFS Edge Classification')
    ax.set_axis_off()
    return ax

def run_dfs(start_node):
    global time
    time = 0
    yield from dfs_visit(start_node)  #Keşif zamanlarını hesapla

    #Bitiş zamanlarını kullanan kenar sınıflandırması
    classify_edges()
    yield draw_graph()  # Grafiği güncelle

# Animasyonu güncelle
def update_animation(_):
    return next(steps)

steps = run_dfs(0)
ani = animation.FuncAnimation(fig, update_animation, frames=len(G.nodes()) * 10, repeat=False, interval=1000)
plt.show()
