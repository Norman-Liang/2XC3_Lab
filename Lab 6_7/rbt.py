import random
import matplotlib.pyplot as plot

def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]

def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L

def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp
    
class RBNode:
    
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def color_flip(self):
        if self.is_black():
            self.make_red()
        else:
            self.make_black()

    def get_brother(self):
        # is right-child ?
        if self.parent.right == self:
            return self.parent.left
        # else 
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    # rotations tested below on tree from vid
    def rotate_right(self, tree):
        x = self # 10
        y = x.left # 5

        x.left = y.right # 10.left = 5.right = 8
        if(y.right != None):
            y.right.parent = x # 8.p = 10
        
        y.parent = x.parent
        if(x.parent == None):
            # tree root change
            tree.root = y
        elif(x == x.parent.left):
            x.parent.left = y
        else:
            x.parent.right = y

        y.right = x # 5.right = 10
        x.parent = y # 10.p = 5

    def rotate_left(self, tree):
        x = self # 5
        y = x.right # 10

        x.right = y.left # 5.r = 10.l = 12
        if(y.left != None):
            y.left.parent = x

        # parent child swap :
        y.parent = x.parent
         
        if(x.parent == None):
            # tree root change
            tree.root = y
        elif(x == x.parent.left):
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
         return "(" + str(self.value) + "," + self.colour + ")"

class BSTree:
    
    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    # recursive approach :
    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        # case-0 : empty tree, Z becomes root
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    # recursive approach, param `node` is the root ;
    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
            else:
                self.__insert(node.right, value)
                
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"

# from vid :
# n1 = RBNode(5)
# n2 = RBNode(12)
# n3 = RBNode(8)
# n4 = RBNode(10)
# n5 = RBNode(2)
# n1.left = n5
# n1.right = n4
# n4.right = n2
# n4.left = n3

# n1.rotate_left()
# n4.rotate_right()
# print(n1,'\n')

class RBTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    # recursive approach :
    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        # case-0 : empty tree, Z becomes root
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    # recursive approach, param `node` is the root ;
    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)

    def fix(self, node):
        # You may alter code in this method if you wish, it's merely a guide.
        if node.parent == None:
            node.make_black()
        # if we have a red parent and child, its a violation :
        while node != None and node.parent != None and node.parent.is_red():

            # case-1 : red uncle
            if(not node.uncle_is_black()):
                # color flips :
                node.parent.color_flip()
                node.get_uncle().color_flip()
                node.parent.parent.color_flip()
                node = node.parent.parent

            # case-2 : black uncle (can be None) + triangle
            elif(node.uncle_is_black and ((node.is_left_child() and node.parent.is_right_child()) or
            node.is_right_child() and node.parent.is_left_child())):

                # rotate Z's parent :
                if(node.is_left_child()):
                    node = node.parent
                    node.rotate_right(self)
                else:
                    node = node.parent
                    node.rotate_left(self)

            # case-3 : black uncle (can be None) + line
            elif(node.uncle_is_black and ((node.is_left_child() and node.parent.is_left_child()) or
            node.is_right_child() and node.parent.is_right_child())):

                # rotate Z's grandparent :
                if(node.parent.is_right_child()):
                    node.parent.parent.rotate_left(self)
                    node.parent.left.color_flip() # orginial gp's color flip
                else:
                    node.parent.parent.rotate_right(self)
                    node.parent.right.color_flip() # orginial gp's color flip

                # color-flip Z's parent ↓ & orginial grandparent ↑
                node.parent.color_flip()

        self.root.make_black()
                    
        
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"

# from example vid :
# rbt1 = RBTree()
# rbt1.insert(8)
# rbt1.insert(5)
# rbt1.insert(15)
# rbt1.insert(12)
# rbt1.insert(19)
# rbt1.insert(9)
# rbt1.insert(13)
# rbt1.insert(23)
# rbt1.insert(10)
# print(rbt1)
def exp1():
    diff = []
    # 10 randomly gen lists ;
    # for k in tqdm(range(20)):
    for k in range(20):
        list1 = [random.randint(1, 100) for j in range(10000)]
        rbt = RBTree()
        bst = BSTree()
        bst_sum = 0
        rbt_sum = 0

        for i in list1:
            rbt.insert(i)
            bst.insert(i)

        bst_sum += bst.get_height()
        rbt_sum += rbt.get_height()
        diff.append(bst_sum - rbt_sum)
    print("\nheight differences : \n",diff)
    sum1 = 0
    for i in diff:
        sum1 += i
    print("\nAvg height diff = ",sum1/len(diff))

exp1()

def experiment2(swapList, runs):
    diff = []
    for i in swapList:
        for _ in range(runs):
            L = create_near_sorted_list(10000,99999,i) 
            rbtavg = 0
            bstavg = 0
            rbt = RBTree()
            bst = BSTree()
            for j in L:
                rbt.insert(j)
                bst.insert(j)
            bstavg = bstavg + bst.get_height()
            rbtavg = rbtavg + rbt.get_height()
        diff.append(bstavg-rbtavg/runs)
    return swapList, diff

swaps, heights = experiment2([0,1,10,100,1000,10000,20000,50000,100000],10)
plot.plot(swaps, heights)
plot.xlabel("Number of Swaps") 
plot.ylabel("Height of Tree")
plot.show()