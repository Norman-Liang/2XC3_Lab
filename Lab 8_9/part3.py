import csv
import math
import min_heap
import random
import timeit
import matplotlib.pyplot as plt

file = open("london_stations.csv", "r")
stationInfo = list(csv.reader(file, delimiter=","))
file.close()

file = open("london_connections.csv", "r")
connectionInfo = list(csv.reader(file, delimiter=","))
file.close()

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

#Modified version of Dijkstra's Algorithm, which returns a tuple of the predeccesor dictionary and the path
def dijkstra(G,s,d):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(s, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key 
        
        if current_node == d:
            break
        
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
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
#The a_star function as seen in part2.py
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
#Find the distance between two stations
def distance(station1, station2):
    deltaLat = float(station1[1])-float(station2[1])
    deltaLong = float(station1[2])-float(station2[2])
    dist = math.sqrt(deltaLat**2+deltaLong**2)
    return abs(dist)
#Choose random station id
def random_station():
    station_list = [i for i in range(304) if i != 189]
    return random.choice(station_list)
#Finds the lines which are used on the path
def transfers(path,connections):
    lines = []
    for i in range(len(path)-1):
        for j in connections:
            if (j[0] == str(path[i]) and j[1] == str(path[i+1])) or (j[1] == str(path[i]) and j[0] == str(path[i+1])):
                if int(j[2]) not in lines:
                    lines.append(int(j[2]))
    return lines
#Get name of station based on id
def name(stationInfo, id):
    for i in stationInfo:
        if str(id) == i[0]:
            return i[3]
    
latlong = [[int(i[0]),float(i[1]),float(i[2])] for i in stationInfo if i[0] != 'id']

stations = [int(i[0]) for i in stationInfo if i[0]!='id']
connections = [[int(i[0]),int(i[1])] for i in connectionInfo if i[0] != 'station1']

#Dictionary which finds the distance between any two stations
distances = {}
for i in latlong:
    distances[i[0]] = {}
    for j in latlong:
        distances[i[0]][j[0]] = distance(i,j)

#Creating a Weighted Graph model of the subway map
subwayMap = DirectedWeightedGraph()
for i in stations:
    subwayMap.add_node(i)
for i in connections:
        if i[0] != i[1]:
            subwayMap.add_edge(i[0],i[1],distances[i[0]][i[1]])
            subwayMap.add_edge(i[1],i[0],distances[i[0]][i[1]])

#The following functions time the execution of the algorithm
def timeD(G, source, destination, k):
    dTime = 0
    
    for _ in range(k):
        start = timeit.default_timer()
        dijkstra(G,source,destination)
        end = timeit.default_timer()
        dTime = end - start
    
    return dTime/k
def timeA(G, source, destination, heuristic, k):
    aTime = 0
    
    for _ in range(k):
        start = timeit.default_timer()
        a_star(G,source,destination,heuristic)
        end = timeit.default_timer()
        aTime = end - start
    
    return aTime/k   

####### TEST CODE #######

G = subwayMap
source = random_station()
destination = random_station()
heuristic = distances[destination]
n = 10
k = 1000
dTime = timeD(G, source, destination, k)
aTime = timeA(G, source, destination,heuristic, k)

print(name(stationInfo, source))
print(name(stationInfo, destination))
print(distances[source][destination])
print(dTime)
print(aTime)
print(transfers(a_star(G, source, destination,heuristic)[1], connectionInfo))