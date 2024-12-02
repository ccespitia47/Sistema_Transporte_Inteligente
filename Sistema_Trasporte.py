import networkx as nx
import heapq
import matplotlib.pyplot as plt

def create_transport_network():
    G = nx.Graph()
    
    # Primero defino las estaciones por nodos
    G.add_node('Estacion_A', tipo='principal')
    G.add_node('Estacion_B', tipo='intermedia')
    G.add_node('Estacion_C', tipo='intermedia')
    G.add_node('Estacion_D', tipo='intermedia')
    G.add_node('Estacion_E', tipo='terminal')
    G.add_node('Estacion_F', tipo='terminal')

    G.add_edge('Estacion_A', 'Estacion_B', weight=3000)
    G.add_edge('Estacion_A', 'Estacion_C', weight=5000)
    G.add_edge('Estacion_B', 'Estacion_D', weight=3000)
    G.add_edge('Estacion_C', 'Estacion_D', weight=4000)
    G.add_edge('Estacion_D', 'Estacion_E', weight=2000)
    G.add_edge('Estacion_C', 'Estacion_F', weight=6000)
    G.add_edge('Estacion_E', 'Estacion_F', weight=3000)

    return G

def dijkstra_k_shortest_paths(graph, source, target, k):


    k_shortest_paths = []
    heap = [(0, source, [source])]

    while heap and len(k_shortest_paths) < k:
        (cost, current, path) = heapq.heappop(heap)
        
        if current == target:
            k_shortest_paths.append((cost, path))
        
        for neighbor in graph.neighbors(current):
            if neighbor not in path:
                new_cost = cost + graph[current][neighbor]['weight']
                new_path = path + [neighbor]
                heapq.heappush(heap, (new_cost, neighbor, new_path))

    return k_shortest_paths

def plot_graph(graph):
    pos = nx.spring_layout(graph)
    
    # Aca clasifico los nodos
    node_colors = []
    for node in graph.nodes(data=True):
        tipo = node[1].get('tipo', 'intermedia')
        if tipo == 'principal':
            node_colors.append('red')
        elif tipo == 'terminal':
            node_colors.append('green')
        else:
            node_colors.append('lightblue')
    
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.title("Red de transporte clasificada")
    plt.show()

def main():
    G = create_transport_network()
    source = 'Estacion_A'
    target = 'Estacion_F'
    k = 5

    routes = dijkstra_k_shortest_paths(G, source, target, k)

    if routes:
        print(f"la {k} ruta mas corta desde {source} a {target} es:")
        for idx, (cost, path) in enumerate(routes):
            print(f"ruta {idx + 1}: {path} con un costo de ${cost}")

        # Ahora se imprime la ruta
        shortest_route = min(routes, key=lambda x: x[0])
        print(f"\n la ruta mas corta es la: {shortest_route[1]} con un costo de $ {shortest_route[0]}")
    else:
        print(f"No se encontraron rutas desde {source} a {target}.")

 
    plot_graph(G)

if __name__ == "__main__":
    main()
