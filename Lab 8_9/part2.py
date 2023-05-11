import min_heap
import random

class DirectedWeightedGraph:
    
    def __init__(self):
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

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G

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
    Q.decrease_key(s, float(h[s]))
    dist[s] = 0

    #Meat of the algorithm
    while not Q.is_empty():
        
        current_element = Q.extract_min()
        current_node = current_element.value
        combDist[current_node] = current_element.key
        
        if current_node == d:
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

####### TEST CODE ########

n = 13
upper = 10

A = DirectedWeightedGraph()
for i in range(13):
    A.add_node(i)
A.add_edge(0,1,7)
A.add_edge(0,2,2)
A.add_edge(0,3,3)
A.add_edge(1,0,7)
A.add_edge(1,2,3)
A.add_edge(1,4,4)
A.add_edge(2,0,2)
A.add_edge(2,1,3)
A.add_edge(2,4,4)
A.add_edge(2,8,4)
A.add_edge(3,0,3)
A.add_edge(3,12,2)
A.add_edge(4,1,4)
A.add_edge(4,2,4)
A.add_edge(4,6,5)
A.add_edge(5,7,2)
A.add_edge(5,11,5)
A.add_edge(6,4,5)
A.add_edge(6,8,3)
A.add_edge(7,8,2)
A.add_edge(7,5,2)
A.add_edge(8,2,1)
A.add_edge(8,6,3)
A.add_edge(8,7,2)
A.add_edge(9,12,4)
A.add_edge(9,11,4)
A.add_edge(10,9,6)
A.add_edge(10,11,4)
A.add_edge(10,12,4)
A.add_edge(11,9,4)
A.add_edge(11,10,4)
A.add_edge(11,5,5)

aDict = {0:10,1:9,2:7,3:8,4:8,5:0,6:6,7:3,8:6,9:4,10:4,11:3,12:6}

source = 5
destination = 12
print(a_star(A,source,destination,aDict))