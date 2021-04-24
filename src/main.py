max = 0
clique_nodes = []

def intersection(a: list, b: list):
    return [value for value in a if value in b]

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
    
    print(max)
    print(clique_nodes)
                        