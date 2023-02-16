from collections import deque

#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    def number_of_nodes():
        return len()


#BFS ; return True if a path exists from node1 -> node2, O(V+E)
def BFS(G, node1, node2):
    # deque instead of que as deque has 0(1) for popping left ele (idx 0)
    Q = deque([node1])
    marked = {node1 : True}
    # fill up marked ;
    for node in G.adj:
        if node != node1:
            marked[node] = False
    # main logic ;
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False

def BFS2(G, node1, node2):
    # deque instead of que as deque has 0(1) for popping left ele (idx 0)
    path = [node1]
    Q = deque([node1])
    marked = {node1 : True}
    # fill up marked ;
    for node in G.adj:
        if node != node1:
            marked[node] = False
    # main logic ;
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                path.append(node2)
                return path
            if not marked[node]:
                path.append(node)
                Q.append(node)
                marked[node] = True
    return []

def BFS3(G, node1):
    # deque instead of que as deque has 0(1) for popping left ele (idx 0)
    pred_dict = {}
    Q = deque([node1])
    marked = {node1 : True}
    # fill up marked ;
    for node in G.adj:
        if node != node1:
            marked[node] = False
    # main logic ;
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if not marked[node]:
                pred_dict[node] = current_node
                Q.append(node)
                marked[node] = True
    return pred_dict


#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}

    for node in G.adj:
        marked[node] = False

    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False

def DFS2(G, node1, node2):
    path = []
    S = [node1]
    marked = {}

    for node in G.adj:
        marked[node] = False
    
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            path.append(current_node)
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    path.append(node2)
                    return path
                if not marked[node]:
                    S.append(node)
                # print("S = ",S,'\n')
    return []

def DFS3(G, node1):
    pred_dict = {}
    S = [node1]
    marked = {}

    for node in G.adj:
        marked[node] = False
    
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if not marked[node]:
                    pred_dict[node] = current_node
                    S.append(node)
                # print("S = ",S,'\n')
    return pred_dict

#Use the methods below to determine minimum vertex covers

def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy

def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])

def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True

def MVC(G):
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover

G1 = Graph(10)
G1.add_edge(0, 1)
G1.add_edge(0, 4)
G1.add_edge(0, 7)
G1.add_edge(1, 2)
G1.add_edge(2, 3)
G1.add_edge(4, 5)
G1.add_edge(5, 6)
G1.add_edge(7, 8)
G1.add_edge(8, 9)

G2 = Graph(7)
G2.add_edge(1, 2)
G2.add_edge(1, 3)
G2.add_edge(2, 4)
G2.add_edge(3, 4)
G2.add_edge(3, 5)
G2.add_edge(4, 6)
G2.add_edge(5, 4)

print(G2.adj,'\n')
print(DFS3(G2,1))

