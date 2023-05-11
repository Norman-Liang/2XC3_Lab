import min_heap
import math
import timeit
import random
import matplotlib.pyplot as plot
import numpy as np


class DirectedWeightedGraph:

    def __init__(self, n):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    # 1) Mark all nodes unvisited
    marked = {}
    pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} # Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    # 2) Assign every node a “known shortest distance” init to inf, ie. Init priority queue/heap and distances
    for node in nodes:
        marked[node] = False
        dist[node] = float("inf")
        Q.insert(min_heap.Element(node, float("inf")))
    
    # 2.1) Set the source node as the current node (it becomes min)
    Q.decrease_key(source, 0)
    dist[source] = 0   

    # Meat of the algorithm
    while not Q.is_empty():
        # 4) Set the closest unmarked node (min dist) to the curr node.
        current_element = Q.extract_min()
        current_node = current_element.value
        marked[current_node] = True
        # dist[current_node] = current_element.key

        # 3) Consider all unvisited neighbours of the current node
        for neighbour in G.adj[current_node]:
            edge_weight = G.w(current_node, neighbour)
            if not marked[neighbour]:

                # 3.1) Update the dist to those nghbrs if dist to curr node + weight of edge to that nghbr < curr dist for nghbr
                if dist[current_node] + edge_weight < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + edge_weight) # relaxing
                    dist[neighbour] = dist[current_node] + edge_weight
                    pred[neighbour] = current_node

    return dist

def bellman_ford(G, source):
    pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} # Distance dictionary
    nodes = list(G.adj.keys())

    # Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    # Meat of the algorithm, checks EVERY edge V-1 times ;
    for _ in range(G.number_of_nodes()):
        # checks EVERY edge ;
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist

def dijkstra_approx(G, source, k):
    relax = {} # tracks relaxations
    marked = {}
    pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} # Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    for node in nodes:
        marked[node] = False
        relax[node] = 0
        dist[node] = float("inf")
        Q.insert(min_heap.Element(node, float("inf")))
        
    Q.decrease_key(source, 0)
    dist[source] = 0   
    relax[source] = k

    # Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        marked[current_node] = True

        for neighbour in G.adj[current_node]:
            edge_weight = G.w(current_node, neighbour)
            if (not marked[neighbour] and relax[neighbour] < k):
                if dist[current_node] + edge_weight < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + edge_weight) # relaxing
                    dist[neighbour] = dist[current_node] + edge_weight
                    pred[neighbour] = current_node
                    relax[neighbour] += 1
    return dist

def bellman_ford_approx(G, source, k):
    relax = {} # tracks relaxations
    pred = {} # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} # Distance dictionary
    nodes = list(G.adj.keys())

    # Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        relax[node] = 0

    dist[source] = 0
    relax[source] = k

    # Meat of the algorithm, checks EVERY edge V-1 times ;
    for _ in range(G.number_of_nodes()):
        # checks EVERY edge ;
        for node in nodes:
            for neighbour in G.adj[node]:
                if(relax[neighbour] < k):
                    if dist[neighbour] > dist[node] + G.w(node, neighbour):
                        dist[neighbour] = dist[node] + G.w(node, neighbour)
                        pred[neighbour] = node
                        relax[neighbour] += 1
    return dist

def a_star(G,s,d,h):        
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    combDist = {} #Heuristic Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        combDist[node] = float("inf")
    Q.decrease_key(s, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        combDist[current_node] = h[current_node]
        
        if current_element == d:
            break
        
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) + h[neighbour] < combDist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour])
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                combDist[neighbour] = dist[current_node] + G.w(current_node, neighbour) + h[neighbour]
                pred[neighbour] = current_node
    
    #Path
    current_node = d
    path = []
    while current_node != s:
        path.append(current_node)
        current_node = pred[current_node]
    path.append(s)
    path.reverse()
    
    #New Pred
    newPred = {}
    for i in path:
        if i == s:
            continue
        newPred[i]=pred[i]
        
    return (newPred, path)

# sum of dist of all node's shortest paths :
def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total


def create_random_complete_graph(n, upper):
    G = DirectedWeightedGraph(n)
    for i in range(n):
        G.add_node(i)
    # add edges ;
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i, j, random.randint(1, upper))
    return G

# incomplete graph generator ;
def gen_rand_graph2(n, e, upper, lower):
    G = DirectedWeightedGraph(n)
    for i in range(n):
        G.add_node(i)
    # add edges ;
    for i in range(e):
        # Choose two distinct nodes at random
        u, v = random.sample(range(n), 2)
        # Add an edge with a random weight
        G.add_edge(u, v, random.randint(lower, upper))
    return G


# dependency on no. of nodes (n) & weights (upper)
def exp1(n, upper):
    num_nodes = []
    total_d = []
    total_bmf = []
    for i in range(1, n):
        gx = create_random_complete_graph(i, upper)
        total_d.append(total_dist(dijkstra(gx, 0)))
        total_bmf.append(total_dist(bellman_ford(gx, 0)))
        num_nodes.append(i)
    return num_nodes, total_d, total_bmf

# dependency on density/no. of edges ;
def exp2(n, upper, d):
    num_edges = []
    total_d = []
    total_bmf = []
    for i in range(1, d):
        e = int(i*n*(n-1)/10) # no. of edges, increased gradually
        gx = gen_rand_graph2(n, e, upper, 1)

        total_d.append(total_dist(dijkstra(gx, 0)))
        total_bmf.append(total_dist(bellman_ford(gx, 0)))
        num_edges.append(e)
    return num_edges, total_d, total_bmf

# dependency on value of k
def exp3(n, upper, k):
    k_vals = []
    total_d = []
    total_bmf = []
    for i in range(1, k):
        gx = create_random_complete_graph(n, upper,)
        total_d.append(total_dist(dijkstra_approx(gx, 0, i)))
        total_bmf.append(total_dist(bellman_ford_approx(gx, 0, i)))
        k_vals.append(i)
    return k_vals, total_d, total_bmf



# num_of_nodes, dist_d, dist_blf = exp1(100, 100)
# num_of_edges, dist_d, dist_blf = exp2(25, 400, 10)
# k_list, dist_d, dist_blf = exp3(100, 500, 15)
# dist_d = np.nan_to_num(dist_d, posinf=15000)
# dist_blf = np.nan_to_num(dist_blf, posinf=15000)
# print(dist_blf)

# plot.plot(num_of_edges, dist_d, 'b-', label = "dijkstra's")
# plot.plot(num_of_edges, dist_blf, 'r-', label = "bellman_ford")


def all_pairs_shortest_path(G, sign):
    n = G.number_of_nodes()
    d = init_d(G)
    for i in range(n):
        if(sign == "+ve"):
            dist = dijkstra(G, i) # returns a dict (with source i)= {i : 0, 1: 4, 2: 7} ie. node : length
        elif(sign == "-ve"):
            dist = bellman_ford(G, i) # returns a dict (with source i)= {i : 0, 1: 4, 2: 7} ie. node : length
        for j in range(n):
            d[i][j] = dist[j]
    return d

# Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    # 2D matrix rep the shortest path b/w all node pairs ;
    d = [[float("inf") for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d

def mystery_exp(n, upper, lower):
    num_nodes = []
    times = []

    for i in range(2, n):
        time = 0
        gx = gen_rand_graph2(i, i*i, upper, lower)

        start = timeit.default_timer()
        mystery(gx)
        end = timeit.default_timer()
        time += end - start

        num_nodes.append(i)
        times.append(time)
    return num_nodes, times

mys_num_nodes, mys_times = mystery_exp(100, 400, -5)
plot.loglog(mys_num_nodes, mys_times, 'r-', label = "mystery")

# converting to log plot ;
# plot.loglog(mys_num_nodes, mys_times, 'r-', label = "mystery")

# getting slope ;
# x = np.log(mys_num_nodes)
# y = np.log(mys_times)

# Fit a line to the data ;
# coefficients = np.polyfit(x, y, 1)

# The first coefficient is the slope ;
# slope = coefficients[0]

# print("The slope of the line is:", slope)

plot.xlabel('no. of nodes') 
plot.ylabel('time')

plot.legend()
plot.show()

# tests : 

g = DirectedWeightedGraph(5)
for i in range(5):
    g.add_node(i)
g.add_edge(0,1,35)
g.add_edge(1,0,35)
g.add_edge(0,2,15)
g.add_edge(2,0,15)
g.add_edge(0,3,25)
g.add_edge(3,0,25)
g.add_edge(1,2,15)
g.add_edge(2,1,15)
g.add_edge(1,4,5)
g.add_edge(4,1,5)
g.add_edge(2,3,35)
g.add_edge(3,2,35)
g.add_edge(2,4,5)
g.add_edge(4,2,5)
g.add_edge(3,4,20)
g.add_edge(4,3,20)

# print(dijkstra(g, 0))
# print(dijkstra_approx(g, 0, 1))
# print(bellman_ford_approx(g, 0, 1))

g2 = DirectedWeightedGraph(5)
for i in range(5):
    g2.add_node(i)
g2.add_edge(0,1,10)
g2.add_edge(0,2,15)
g2.add_edge(0,3,25)
g2.add_edge(3,4,20)
g2.add_edge(4,1,-40)
g2.add_edge(4,2,-35)
g2.add_edge(3,2,35)

# print(bellman_ford(g2, 0))
# print(dijkstra_approx(g2, 0, 1))
# print(mystery(g))
# print(all_pairs_shortest_path(g, "-ve"))
# print(bellman_ford_approx(g2, 0, 1))