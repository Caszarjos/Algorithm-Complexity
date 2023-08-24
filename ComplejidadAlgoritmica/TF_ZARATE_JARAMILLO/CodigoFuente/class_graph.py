class Graph:
    # CLASE GRAFO NO DIRIGIDO
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, node):
        self.nodes[node] = []
        
    def add_nodes(self, nodes):
        for node in nodes:
            self.nodes[node] = []
            
    def add_edge(self, ori, dest, peso):
        if ori in self.nodes and dest in self.nodes:
            self.nodes[ori].append((dest, peso))
            self.nodes[dest].append((ori, peso))
        else:
            print("Error: nodos no existentes")
    
    def add_edges(self, edges):
        for ori, dest, peso in edges: #ori, dest son structs
            ori = ori['NAME']
            dest = dest['NAME']
            if ori in self.nodes and dest in self.nodes:
                self.nodes[ori].append((dest, peso))
                self.nodes[dest].append((ori, peso))
            else:
                print(f"Error: nodo ({ori},{dest},{peso})")
    
    def get_info(self, node):
        return self.nodes[node]
    
    def get_adjList(self):
        return self.nodes
    
    def get_nodes(self): # Lista de nombres de hospitales
        return list(self.nodes.keys())
    
    def get_edges(self): # Lista de tuplas con informacion de los nodes
        edges = []
        for ori in self.nodes:
            for dest, peso in self.nodes[ori]:
                if (dest, ori, peso) not in edges:
                    edges.append((ori, dest, peso))
        return edges
    
    def print_edges(self):
        print(self.get_edges())

    def print_nodes(self):
        print(self.get_nodes())
        
    def print_lon_edges(self):
        print(len(self.get_edges()))
        
    def print_lon_nodes(self):
        print(len(self.get_nodes()))