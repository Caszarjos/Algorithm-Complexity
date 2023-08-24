#LIBRERIAS
import csv
import networkx as nx
import matplotlib.pyplot as plt
from class_graph import Graph
from sklearn.neighbors import KDTree
from collections import deque

def read_hospitals_csv():
    # LEER HOSPITALES
    with open('TF_ZARATE_JARAMILLO/CSV/test.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        hospitals_names = []
        hospitals = []
        for row in reader:
            hospital = {
                'NAME': row['NAME'],
                'CITY': row['CITY'],
                'STATE': row['STATE'],
                'COUNTY': row['COUNTY'],
                'LATITUDE': float(row['LATITUDE']),
                'LONGITUDE': float(row['LONGITUDE'])
            }
            hospitals.append(hospital)
            hospitals_names.append(hospital['NAME'])
    return hospitals, hospitals_names

def generate_edges(hospitals, k=5):
    # Generar las aristas (A partir de las 5 distancias mas cortas)
    # INPUT: Lista de hospitales, k: total de hospitales mas cercanos
    # OUTPUT: Lista de aristas que crean las relaciones de los grafos
    edges = []
    coordinates = [(hospital['LATITUDE'], hospital['LONGITUDE']) for hospital in hospitals]
    kd_tree = KDTree(coordinates)
    for hospital in hospitals:
        coord = (hospital['LATITUDE'], hospital['LONGITUDE'])
        distances, indices = kd_tree.query([coord], k=k+1)
        nearest_indices = indices[0][1:]
        for j, index in enumerate(nearest_indices):
            dist = distances[0][j+1]
            #dist = distance(coord, coordinates[j]).kilometers
            hospital_tuple = (hospital['NAME'], 
                              hospital['CITY'], 
                              hospital['STATE'], 
                              hospital['COUNTY'])
            target_hospital_tuple = (hospitals[index]['NAME'], 
                                     hospitals[index]['CITY'], 
                                     hospitals[index]['STATE'],
                                     hospitals[index]['COUNTY'])
            edges.append((hospital, hospitals[index], round(dist, 2)))
    # edge = (object1,object2,distance)
    return edges

def kruskal_mst(graph):
    # Generar el arbol de expansion minimo
    # INPUT: Grafo generado 
    # OUTPUT: Grafo de expansion minimo
    mst = Graph()
    mst.add_nodes(graph.get_nodes())
    
    sorted_edges = sorted(graph.get_edges(), key=lambda x: x[2])
    parents = {node: node for node in graph.get_nodes()}
    rank = {node: 0 for node in parents.keys()}
    
    def find(node):
        if parents[node] != node:
            parents[node] = find(parents[node])
        return parents[node]
    def union(act_node, target_node):
        root_u = find(act_node)
        root_v = find(target_node)
        if rank[root_u] < rank[root_v]:
            parents[root_u] = root_v
        elif rank[root_u] > rank[root_v]:
            parents[root_v] = root_u
        else:
            parents[root_v] = root_u
            rank[root_u] += 1
    for edge in sorted_edges:
        act_node, target_node, weight = edge
        if find(act_node) != find(target_node):
            mst.add_edge(act_node, target_node, weight)
            union(act_node, target_node)
    return mst

def bfs_with_limitations(graph, start_node, max_nodes=None, max_depth=None):
    # Funcion que permite la busqueda de hospitales mas cercanos al hospital ingresado
    # INPUT: graph: grafo general o mst, start_node: hospital inicial, max_nodes: numero maximo de nodos a recorrer, max_depth: altura maxima a recorrer
    # OUTPUT: array de hospitales mas cercanos
    
    visited = set()
    queue = deque([(start_node, 0)])
    result = []
    nxList = []

    while queue:
        node, depth = queue.popleft()
        visited.add(node)
        if max_nodes is not None and len(result) >= max_nodes:
            break
        if max_depth is not None and depth > max_depth:
            break
        result.append(node)
        for neighbor, weight in graph.get_info(node):
            if neighbor not in visited and depth < max_depth:
                nxList.append((node, neighbor, weight))
                queue.append((neighbor, depth + 1))
                
    nxGraph = nx.DiGraph()
    nxGraph.add_weighted_edges_from(nxList)
    return result, nxGraph

def dfs_by(graph, type_, name, hospitals):
    start_node = 'CENTRAL VALLEY GENERAL HOSPITAL'
    path = []
    nxList = []
    visited = { hospital: False for hospital in graph.get_nodes()}
    hospitals = { hospital['NAME']: hospital for hospital in hospitals}
    
    def _dfs(act_node):
        visited[act_node] = True
        for target_node, weight in graph.get_info(act_node):
            if not visited[target_node]:
                if hospitals[target_node][type_] == name:
                    nxList.append((act_node, target_node))
                    path.append(target_node)
                _dfs(target_node)
    _dfs(start_node)
    
    nxGraph = nx.Graph()
    nxGraph.add_edges_from(nxList)
    return path, nxGraph

def kosajaru(graph):
    def reverseGraph(edges):
        graph_dict = dict()
        for edge in edges:
            source, target, weight = edge
            if target not in graph_dict:
                graph_dict[target] = []
            graph_dict[target].append(source)
        return graph_dict
    def dfs(graph, start, lst, visited):
        if start not in graph.keys():
            graph[start] = []
        visited[start] = True
        for v in graph[start]:
            if not visited[v]:
                dfs(graph, v, lst, visited)
        lst.append(start) 
    def to_adjList(adjList):
        aux = dict()
        for node in adjList.keys():
            aux[node] = [n for n,w in adjList[node]]
        return aux
    
    nodes = graph.get_nodes()
    edges = graph.get_edges() 
    
    n = len(nodes)
    visited = {node: False for node in nodes}
    f = []

    grev = reverseGraph(edges)            # step 1
    adj_list = to_adjList(graph.get_adjList())

    for node in nodes:                        # step 2
        if not visited[node]:
            dfs(grev, node, f, visited)
    visited = {node: False for node in list(reversed(nodes))}    # step 3
    scc = []
    for node in list(reversed(f)):
        if not visited[node]:
            cc = []
            dfs(adj_list, node, cc, visited)
            scc.append(cc)
    return max(scc, key=len)

def generate_quality(graph):
    with open('TF_ZARATE_JARAMILLO/CSV/test.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        hospitals_names = []
        hospitals = dict()
        for row in reader:
            hospitals[row['NAME']] = {
                'TRAUMA': row['TRAUMA'],
                'BEDS': int(row['BEDS']),
                'POPULATION': int(row['POPULATION']),
                'QUALITY': int(0)
            }
    
    scc_hospitals = kosajaru(graph)
    
    for hospital in hospitals:
        increment = 0
        quality = 0
        
        if hospitals[hospital]['TRAUMA'] in ['LEVEL III','LEVEL IV','LEVEL V']:
            increment = 2
        elif hospitals[hospital]['TRAUMA'] == 'NOT AVAILABLE':
            increment = 0
        else: increment = 1
        quality += increment
        
        if hospitals[hospital]['BEDS'] < 100:
            increment = 0
        elif hospitals[hospital]['BEDS'] >= 100 and hospitals[hospital]['BEDS'] < 500:
            increment = 1
        else: increment = 2
        quality += increment
        
        if hospitals[hospital]['POPULATION'] < 100:
            increment = 0
        elif hospitals[hospital]['POPULATION'] >= 100 and hospitals[hospital]['POPULATION'] < 500:
            increment = 1
        else: increment = 2
        quality += increment
        
        if hospital == scc_hospitals: increment = 1
        quality += increment
        
        hospitals[hospital]['QUALITY'] = quality
    return hospitals

def visualize_qualityGraph(hospitals, graph, names):
    node_colors = {
        7: '#00FFAE',
        6: '#44E8D4',
        5: '#59D765',
        4: '#59D765',
        3: '#54945A',
        2: '#6F8070',
        1: '#4E564E',
        }
    list_tuples = []
    qgraph = nx.Graph()
    
    for u,v,w in graph.get_edges(): list_tuples.append(((u, hospitals[u]['QUALITY']),(v, hospitals[u]['QUALITY']),w))
    
    qgraph.add_weighted_edges_from(list_tuples)
    plt.figure(figsize=(8,8))
    pos = nx.spring_layout(qgraph, scale=1)
    
    node_color_list = [node_colors.get(quality, '#0F1010') for node, quality in qgraph.nodes()]
    labels = {(node,quality): (node, quality) if node in names else '' for node, quality in qgraph.nodes()}
    
    nx.draw(qgraph, pos, node_color= node_color_list, node_size=25)
    nx.draw_networkx_labels(qgraph, pos, labels=labels, font_color='Black', font_size=8)#, font_weight='bold')
    
    plt.title("Quality Graph")
    plt.axis('off')
    plt.show()
    
def visualize_graph(nxGraph):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(nxGraph)
    nx.draw(nxGraph, pos, with_labels=False, node_size=50)
    if len(nxGraph.nodes()) < 20:
        nx.draw_networkx_labels(nxGraph, pos, font_color='Black', font_size=7, font_weight='bold')
    nx.draw_networkx_edge_labels(nxGraph, pos, edge_labels=nx.get_edge_attributes(nxGraph, 'weight'))
    
    plt.title("Finding hospitals with BFS")
    plt.axis('off')
    plt.show()
