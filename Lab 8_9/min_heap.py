import math

'''Instead of just storing numbers, I'm storing it in a more traditional way that you actually have a priority que,
where you have a value that you keep there and that value & key pair can be anything. 
The value can be a number of the key, can be a number'''

class MinHeap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.map = {}
        # Element("A",5) : (value,key) which is in L
        for i in range(len(L)):
            self.map[L[i].value] = i
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.sink(i)

    def sink(self, i):
        smallest_known = i
        if self.left(i) < self.length and self.data[self.left(i)].key < self.data[i].key:
            smallest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)].key < self.data[smallest_known].key:
            smallest_known = self.right(i)
        if smallest_known != i:
            self.data[i], self.data[smallest_known] = self.data[smallest_known], self.data[i]
            self.map[self.data[i].value] = i
            self.map[self.data[smallest_known].value] = smallest_known
            self.sink(smallest_known)

    def insert(self, element):
        if len(self.data) == self.length:
            self.data.append(element)
        else:
            self.data[self.length] = element

        # new ele is added at the end and then we swim it up
        self.map[element.value] = self.length
        self.length += 1
        self.swim(self.length - 1)

    def insert_elements(self, L):
        for element in L:
            self.insert(element)

    # based on key, ie. the weight of the edge ;
    def swim(self, i):
        while i > 0 and self.data[i].key < self.data[self.parent(i)].key:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            self.map[self.data[i].value] = i
            self.map[self.data[self.parent(i)].value] = self.parent(i)
            i = self.parent(i)

    def get_min(self):
        if len(self.data) > 0:
            return self.data[0]

    def extract_min(self):
        # swap first and last values ;
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]

        # update hashmap, recall ("A",5) : (value,key)
        self.map[self.data[self.length - 1].value] = self.length - 1
        self.map[self.data[0].value] = 0

        # popped ele ;
        min_element = self.data[self.length - 1]
        self.length -= 1
        self.map.pop(min_element.value) # ele removed from hashmap
        self.sink(0)
        return min_element

    # eg. dec_key("A", 500) : (value, key) ie. (node, weight/distTo)
    def decrease_key(self, value, new_key):
        # won't change if the new_key is bigger
        if new_key >= self.data[self.map[value]].key:
            return
        index = self.map[value]
        # no shift here, direct replacement ; 
        self.data[index].key = new_key
        self.swim(index)

    # returns the type Element ;
    def get_element_from_value(self, value):
        # hashmap stores value : index pairs
        return self.data[self.map[value]]

    def is_empty(self):
        return self.length == 0

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height + height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s


class Element:

    def __init__(self, value, key):
        self.value = value
        self.key = key

    def __str__(self):
        return "(" + str(self.value) + "," + str(self.key) + ")"

# "A" is the value, 5 is the key ie (value,key)
nodes1 = [Element("A", 5), Element("B", 1), Element("C", 10), Element("D", 2), Element("E", -3)]
nodes2 = [Element(1, 1), Element(2, 1), Element(3, 10), Element(4, 2), Element(5, -3)]