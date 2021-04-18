max = 0
clique_nodes = []


def intersection(a: list, b: list):
    return [value for value in a if value in b]


def brute_force_clique_(G: dict, U: list, size, nodes: list):
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
        brute_force_clique_(G, intersection(U, G[i]), size + 1, nodes[:])


def brute_force_clique(G: dict):
    brute_force_clique_(G, list(G.keys()), 0, [])


if __name__ == '__main__':
    D = {
        'a': ['b', 'c', 'd'],
        'b': ['c', 'e', 'd', 'a'],
        'c': ['a', 'b', 'd'],
        'g': ['d', 'i'],
        'i': ['j', 'g', 'd'],
        'd': ['c', 'e', 'f', 'b', 'g', 'i'],
        'j': ['i']
    }

    brute_force_clique(D)

    print(max)
    print(clique_nodes)
