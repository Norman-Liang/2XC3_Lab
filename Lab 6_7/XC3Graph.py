import matplotlib.pyplot as plot

class XC3Graph:

    def __init__(self, degree):
        self.children = {}
        for i in range(degree):
            self.children[i] = {}
        self.children = self.xc3ify(self.children)
            
    def xc3ify(self, list):
        if len(list) <= 2:
            return list
        for i in range(2,len(list)):
            for j in range(0,i-1):
                list[i][j] = {}
        return {k:self.xc3ify(list) for k, list in list.items()}

    def get_degree(self):
        return len(self.children)
    
    def number_of_nodes(self):
        return str(self.children).count('{')
    
    def get_height(self):
        count = 0
        for i in str(self.children)[::-1]:
            if i == "}":
                count = count + 1
            else:
                return count
    
    def __str__(self):
        return str(self.children)
            
g = XC3Graph(8)
print(g)
print(g.number_of_nodes())

################
# Experiment 3 #
################

degrees = []
heights = []

for i in range(26):
    tree = XC3Graph(i)
    degrees.append(i)
    heights.append(tree.get_height())
    
plot.plot(degrees, heights)
plot.xlabel("Degree of XC3 Tree") 
plot.ylabel("Height of XC3 Tree")
plot.show()