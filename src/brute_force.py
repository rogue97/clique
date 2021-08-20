from datetime import datetime
import os
import sys


max = 0
clique_nodes = []

graph_1 = "[c125-9] 125 6963.txt"
graph_2 = "[brock200_4] 200 13089.txt"
graph_3 = "[gen400_p0-9_55] 400 71820.txt"
graph_4 = "[p_hat300-3] 300 33390.txt"
graph_5 = "[DSJC1000-5] 1000 499652.txt"

def intersection(a: list, b: list):
    return [value for value in a if value in b]


def process_data(filename) -> dict:
    g = {}
    try:
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            line = f.readline()
            while line[0] == 'c' or len(line) <= 1:
                line = f.readline()
            if line[0] == 'p':
                tok = line.split(' ')
                NUMBER_EDGES = int(tok[3])

            for _ in range(0, NUMBER_EDGES):
                line = f.readline()
                tok = line.split(' ')
                sv = int(tok[1])
                ev = int(tok[2])
                keys = g.keys()
                # pod pretpostavkom da nije duplo navodjeno
                if sv not in keys:
                    g[sv] = [ev]
                else:
                    g[sv] = g[sv] + [ev]
                if ev not in keys:
                    g[ev] = [sv]
                else:
                    g[ev] = g[ev] + [sv]
        return g
    except IOError as _:
        print("No file found")
    except:
        print("Unexpected error:", sys.exc_info())

def brute_force_clique_(G:dict, U:list, size, nodes:list):
    global max, clique_nodes
    if len(U) == 0:
        max = size
        clique_nodes = nodes
        return 
        
    while len(U) != 0:
        if size + len(U) <= max:
            return 
        i = U[0]
        nodes.append(i)
        U.remove(i)
        brute_force_clique_(G, intersection(U,G[i]), size+1,nodes[:]) 

def brute_force_clique(G:dict):
    brute_force_clique_(G, list(G.keys()), 0, [])


if __name__ == '__main__':
    print("Loading graph from :", graph_1)
    # G = process_data(graph_1)
    print("Brute force algorithm...", datetime.now())
    # brute_force_clique(G)
    # D = {
    #     'a' : ['b', 'c', 'd'],
    #     'b' : ['c', 'e', 'd', 'a'],
    #     'c' : ['a', 'b', 'd'],
    #     'g' : ['d','i'],
    #     'i' : ['j', 'g', 'd'],
    #     'd' : ['c', 'e','f', 'b','g','i'],
    #     'j' : ['i']
    # }
    D = {0: [1, 2, 3, 4, 5, 7, 9], 9: [0, 2, 3, 4, 5, 6, 7, 9], 1: [0, 1, 2, 3, 5, 6, 7, 8], 7: [0, 1, 2, 3, 5, 6, 7, 9], 8: [1, 3, 4, 5, 6], 3: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2: [0, 1, 3, 5, 7, 9], 5: [0, 1, 2, 3, 5, 6, 7, 8, 9], 4: [0, 8, 3, 9], 6: [1, 3, 5, 6, 7, 8, 9]}
    brute_force_clique(D)
    
    print(datetime.now(),"Maximum clique",str(max), "with nodes:\n", clique_nodes)
                        
