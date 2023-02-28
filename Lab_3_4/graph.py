import math
from tqdm import tqdm
from collections import deque
import copy
import random
import matplotlib.pyplot as plot

# Undirected graph using an adjacency list
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

    def get_size(self):
        return len(self.adj)

# ---------------------------------------------------------------------------------------------------------------------------------------

# BFS ; return True if a path exists from node1 -> node2, O(V+E)
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
        # print(Q)
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


# Depth First Search ------------------------------------------------------------------------------------------------------------------
def DFS(G, node1, node2):
    S = [node1] # stack
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
        # print("stack = ",S)
        current_node = S.pop()
        if not marked[current_node]:
            path.append(current_node)
            marked[current_node] = True
            if current_node == node2:
                return path
            for node in G.adj[current_node]:
                S.append(node)
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

# Vertex Cover ------------------------------------------------------------------------------------------------------------------
# Use the methods below to determine minimum vertex covers

# returns a new 2D list where the input element has been appended to each of the sub-lists in the input list.
def add_to_each(sets, element): # sets is a 2D list [[]]
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy


# gives all possible pairs of the nodes of a Graph ;
def power_set(set : list): # set is [0,1,2,3..] ie. all nodes
    # print(set)
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])
    # use python tutor to visualize recursive part


# checks if C is a vertex-cover of G ;
def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True


# Brute force approach : Tries all spanning trees Ω(2^n) where n = len(V)
def MVC(G):
    # list containing all nodes of the graph
    nodes = [i for i in range(G.get_size())]
    subsets = power_set(nodes)  # all possible subsets 
    # start with list containing all nodes/vertcies
    min_cover = nodes 
    # traverse over the power-set Ω(2^n) , updating min_cover accordingly ;
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover

# MVC Approximations -------------------------------------------------------------------------------------------------------

def approx1(G : Graph):
    # 1. Start with an empty set C = {}
    C = set()
    adj = copy.deepcopy(G.adj) # copy of adjacency dict
    while not (is_vertex_cover(G,C)):
        # 2. Find the vertex with the highest deg in G, call it v.
        max_deg = 0 # init val.
        v = 0 # init. val
        for i in adj:
            if len(adj[i]) > max_deg:
                v = i
                max_deg = len(adj[i])
            # if 2 nodes have same deg, take the smaller one
            elif len(adj[i]) == max_deg and i < v:
                v = i
                max_deg = len(adj[i])
        # 3. Add v to C
        C.add(v)
        # 4. Remove all edges incident to node v from G
        for i in adj[v]:
            if v in adj[i]:
                adj[i].remove(v)
        adj[v] = []
        # print(adj,"-",C)

    # 5. If C is a Vertex Cover return C, else go to Step 2
    return C
    
def approx2(G : Graph):
    # 1. Start with an empty set C = {}
    C = set()
    while not (is_vertex_cover(G,C)):
        # 2. Select a vertex randomly from G which is not already in C, call this vertex v.
        v = random.randint(0,G.get_size()-1)
        # 3. Add v to C
        if v not in C:
            C.add(v)

    # 4. If C is a Vertex Cover return C, else go to Step 2
    return C

def approx3(G : Graph):
    # 1. Start with an empty set C = {}
    C = set()
    adj = copy.deepcopy(G.adj) # copy of adjacency dict

    while not (is_vertex_cover(G,C)):
        # 2. Select an edge randomly from G, call this edge (u,v)
        while True:
            u = random.randint(0,G.get_size()-1)
            if (len(adj[u]) == 0): # to avoid empty range error in randint
                continue
            else:
                break
        v = adj[u][random.randint(0,len(adj[u])-1)]

        # 3. Add u and v to C
        if u not in C:
            C.add(u)
        if v not in C:
            C.add(v)

        # 4. Remove all edges incident to u or v from G
        for i in adj[u]:
            if u in adj[i]:
                adj[i].remove(u)
        for i in adj[v]:
            if v in adj[i]:
                adj[i].remove(v)
        adj[u] = []
        adj[v] = []

    # 5. If C is a Vertex Cover return C, else go to Step 2
    return C

# MVC approx experiments ---------------------------------------------------------------------------------------------------------

# generates random graph with given no. of nodes & edges ;
def rand_graph(nodes : int, edges : int):
    G = Graph(nodes)
    # how to ensure graph is connected ?
    for i in range(edges):
        u = random.randint(0,G.get_size()-1)
        while True:
            v = random.randint(0,G.get_size()-1)
            if u == v: # To avoid self loops
                continue
            else: 
                break
        G.add_edge(u,v)
    return G

# func to get the fraction for all 3 approx funcs ;
def test(nodes, edges, graphs): 
    total_opt = 0 # sum of len of all MVCs gen by MVC(G)
    total_appx1 = 0 # sum of len of all MVCs gen by appx1(G)
    total_appx2 = 0
    total_appx3 = 0
    for i in tqdm(range(graphs)):
        G = rand_graph(nodes, edges)
        total_opt += len(MVC(G))
        total_appx1 += len(approx1(G))
        total_appx2 += len(approx2(G))
        total_appx3 += len(approx3(G))
    return total_appx1/total_opt, total_appx2/total_opt, total_appx3/total_opt

# print(test(8,18,1000))

# G4 = rand_graph(8,10)
# print("\nG4 = ",G4.adj,'\n')
# print("MVC G1 = ",MVC(G4))
# print("appx1 = ",approx1(G4))
# print("appx2 = ",approx2(G4))
# print("appx3 = ",approx3(G4))

graphs = 1000
n = 8

# plotting funcs ;
def appx_exp1():
    exp_val1 = []
    exp_val2 = []
    exp_val3 = []
    num_edges = []
    for edges in range(1,35,5):
        val1, val2, val3 = test(n, edges, graphs)
        exp_val1.append(val1)
        exp_val2.append(val2)
        exp_val3.append(val3)
        num_edges.append(edges)
    return exp_val1, exp_val2, exp_val3, num_edges

# exp_val1, exp_val2, exp_val3, num_edges = appx_exp1()

# plot.plot(num_edges,exp_val1,'b-',label = "approx1")
# plot.plot(num_edges,exp_val2,'r-',label = "approx2")
# plot.plot(num_edges,exp_val3,'g-',label = "approx3")
# plot.xlabel('no. of edges')

def appx_exp2():
    exp_val1 = []
    exp_val2 = []
    exp_val3 = []
    num_nodes = []
    for nodes in range(2,15,2):
        val1, val2, val3 = test(nodes, math.floor(nodes*1.5), graphs)
        exp_val1.append(val1)
        exp_val2.append(val2)
        exp_val3.append(val3)
        num_nodes.append(nodes)
    return exp_val1, exp_val2, exp_val3, num_nodes

# exp_val1, exp_val2, exp_val3, num_nodes = appx_exp2()

# plot.plot(num_nodes,exp_val1,'b-',label = "approx1")
# plot.plot(num_nodes,exp_val2,'r-',label = "approx2")
# plot.plot(num_nodes,exp_val3,'g-',label = "approx3")
# plot.xlabel('no. of nodes')

# generate all possible edges for a graph of size 5;
def get_edges():
    nodes = [0, 1, 2, 3, 4]
    edges = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            edges.append((nodes[i], nodes[j]))
    return edges

# print((power_set(get_edges())))

''' func to get all possible graphs of size 5 using power set of edges &
test approx1 on all these graphs : '''
def appx_exp3():
    exp_val1 = []
    num_edges = []
    G0 = Graph(5)

    all_edges = get_edges()
    powset_edges = power_set(all_edges) # contains edges list for 1024 graphs
    sorted_powset = sorted(powset_edges, key=len)
    # print(sorted_powset)

    for i in sorted_powset[1:]: # i -> list of all edges of a graph
        for edge in i:
            G0.add_edge(edge[0],edge[1])

        # graph is ready, add lens to total ;
        # print(G0.adj,'\n')
        # print(MVC(G0), approx1(G0))
        exp_val1.append(len(MVC(G0))/len(approx1(G0)))
        num_edges.append(len(i))
    return exp_val1, num_edges

# exp_val1, num_edges = appx_exp3()
# print(len(exp_val1))
# plot.plot(num_edges,exp_val1,'b-',label = "approx1")
# plot.xlabel('no. of edges')

# plot.ylabel('expected performance')
# plot.legend()
# plot.show()

# runs -----------------------------------------------------------------------------------------------------------------------

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

# print("\nG1 = ",G1.adj,'\n')
# print("MVC G1 = ",MVC(G1))
# print("appx1 = ",approx1(G1))
# print("appx2 = ",approx2(G1))
# print("appx3 = ",approx3(G1))
# print(BFS2(G1,0,9))

# from lab_3_4 doc
G2 = Graph(7)
G2.add_edge(1,2)
G2.add_edge(1,3)
G2.add_edge(2,4)
G2.add_edge(3,4)
G2.add_edge(3,5)
G2.add_edge(4,5)
G2.add_edge(4,6)

# print(DFS3(G2,1))
# print("\nG2 = ",G2.adj,'\n')
# print("MVC G2 = ",MVC(G2))
# print("appx1 = ",approx1(G2))
# print("appx2 = ",approx2(G2))
# print("appx3 = ",approx3(G2))

# from vid
G3 = Graph(9)
G3.add_edge(0, 1)
G3.add_edge(0, 6)
G3.add_edge(1, 2)
G3.add_edge(1, 3)
G3.add_edge(1, 4)
G3.add_edge(4, 5)
G3.add_edge(6, 7)
G3.add_edge(7, 8)

# print(DFS2(G3,0,2))
# print("\nG3 = ",G3.adj,'\n')
# print("MVC G3 = ",MVC(G3))
# print("appx1 = ",approx1(G3))
# print("appx2 = ",approx2(G3))
# print("appx3 = ",approx3(G3))



