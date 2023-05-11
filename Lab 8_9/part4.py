import min_heap
import math
import timeit
import random
import matplotlib.pyplot as plot
from tqdm import tqdm
from icecream import ic
from abc import ABC, abstractmethod
import numpy as np

ic.configureOutput(prefix='test | ')

    
class Graph(ABC): #for the interface <Graph>
    
    @abstractmethod
    def add_node(self, node):
        pass
    
    @abstractmethod
    def add_edge(self, node1, node2, weight):
        pass
    
    @abstractmethod
    def get_neighbors(self, node):
        pass
    
    @abstractmethod
    def get_weight(self, node1, node2):
        pass
    
class DirectedWeightedGraph:

    def __init__(self, n):
        self.adj = {}
        self.weights = {}
        for i in range(n):
            self.adj[i] = []

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
    
class HeuristicGraph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        self.graph[node] = {}

    def add_edge(self, node1, node2, weight):
        self.graph[node1][node2] = weight

    def get_neighbors(self, node):
        return self.graph[node]
    
class SPAlgorithm(ABC): #for the <SPAlgorithm> Interface
    
    @abstractmethod
    def find_shortest_path(self, graph, source, dest): #to find the shortest path in graph
        pass

class ShortPathFinder(SPAlgorithm):
    def shortest_path(self, graph, source, dest):
        pass
    
class Dijkstra:
    
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
    
    
class bellmanford:
    
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
    
class astar:
    
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

#Until this line is the refactorisation of code for the UML diagram. Below are experiments and other functions related to different parts .
#------------------------------------------------------------------------------------------------

# sum of dist of all node's shortest paths :
def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n, upper):
    G = DirectedWeightedGraph(n)
    # for i in range(n):
    #     G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i, j, random.randint(1, upper))
    return G

# incomplete graph generator ;
def gen_rand_graph2(n, e, upper, lower):
    G = DirectedWeightedGraph(n)
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
    for i in tqdm(range(1, n)):
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
    for i in tqdm(range(1, d)):
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
    for i in tqdm(range(1, k)):
        gx = create_random_complete_graph(n, upper,)
        total_d.append(total_dist(dijkstra_approx(gx, 0, i)))
        total_bmf.append(total_dist(bellman_ford_approx(gx, 0, i)))
        k_vals.append(i)
    return k_vals, total_d, total_bmf

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

    for i in tqdm(range(2, n)):
        time = 0
        gx = gen_rand_graph2(i, i*i, upper, lower)

        start = timeit.default_timer()
        mystery(gx)
        end = timeit.default_timer()
        time += end - start

        num_nodes.append(i)
        times.append(time)
    return num_nodes, times

