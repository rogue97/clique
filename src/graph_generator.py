import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
n_nodes = 10

def intersection(a: list, b: list):
    return [value for value in a if value in b]

class GraphVisualization: 
   
    def brute_force_clique_(self, G:dict, U:list, size, nodes:list):
        if len(U) == 0:
            self.max = size
            self.clique_nodes = nodes
            return 
            
        while len(U) != 0:
            if size + len(U) <= self.max:
                return 
            i = U[0]
            nodes.append(i)
            U.remove(i)
            self.brute_force_clique_(G, intersection(U,G[i]), size+1,nodes[:]) 

    def brute_force_clique(self):
        mapa = self.getMap()
        self.brute_force_clique_(mapa, list(mapa.keys()), 0, [])

    def __init__(self): 
          
        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.visual = [] 
        self.max = 0
        self.clique_nodes = []
          
    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b): 
        temp = [a, b] 
        self.visual.append(temp) 
          
    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.Graph() 
        G.add_edges_from(self.visual) 
        nx.random_layout(G)
        nx.draw(G, with_labels=True)
        # nx.draw_networkx(G) 
        plt.show() 
    
    def getMap(self):
        mapa = {}
        for i in self.visual:
            if i[0] not in mapa.keys():
                mapa[i[0]] = set([])
            if i[1] not in mapa.keys():
                mapa[i[1]] = set([])
            mapa[i[0]].add(i[1])
            mapa[i[1]].add(i[0])
        for k, v in mapa.items():
            mapa[k] = list(v)
        return mapa
    
    def visualizeMaxClique(self):
        self.brute_force_clique()
        if self.clique_nodes is not None:
            G = nx.Graph()
            for v in self.visual:
                if v[0] in self.clique_nodes and v[1] in self.clique_nodes:
                    G.add_edge(v[0], v[1], color='red')
                    # TODO ne radi bojenje
                    # print("r", v[0], v[1])
                else:
                    # print("b", v[0], v[1])
                    G.add_edge(v[0], v[1], color='blue')
            
            nx.draw(G, with_labels=True)
            # nx.draw_networkx(G) 
            plt.show() 
        else:
            print("nema kliku")
            self.visualize()
    



# Driver code 
G = GraphVisualization() 
# G.visualize() 

matrica = {}
random.seed(1)
if __name__ == '__main__':
    # random generisanje grafa
    for i in range(n_nodes):
        matrica[i] = random.sample(range(n_nodes), random.randint(0, n_nodes-1)) 
        if len(matrica[i]) == 0:
            matrica[i] = [random.randint(0, n_nodes-1)]
        for m in matrica[i]:
            G.addEdge(i, m)

    # print (matrica)
    mapa = G.getMap()
    G.visualizeMaxClique()