"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.

It contains traditional implementations for:
1) Quick sort
2) Merge sort
3) Heap sort

Author: Vincent Maccio
"""

import math
import timeit
import random
import matplotlib.pyplot as plot

# ************ Quick Sort ************

def quicksort(L):
    copy = quicksort_copy(L)
    for i in range(len(L)):
        L[i] = copy[i]

def quicksort_copy(L):
    if len(L) < 2:
        return L
    pivot = L[0]
    left, right = [], []
    for num in L[1:]:
        if num < pivot:
            left.append(num)
        else:
            right.append(num)
    return quicksort_copy(left) + [pivot] + quicksort_copy(right)

# ************ Dual Quick Sort *************

def dual_quicksort(L : list):
    copy = quicksort_copy(L)
    for i in range(len(L)):
        L[i] = copy[i]

def quicksort_copy(L):
    if len(L) < 2:
        return L

    # 1) select 1st & 2nd ele as small & big pivots resp ;
    if(L[0] < L[1]):
        pivot1 = L[0]
        pivot2 = L[1]
    else:
        pivot1 = L[1]
        pivot2 = L[0]

    left, mid, right = [], [], []
    for num in L[2:]:
        if num < pivot1:
            left.append(num)
        elif(num >= pivot1 and num <= pivot2):
            mid.append(num)
        else:
            right.append(num)

    return quicksort_copy(left) + [pivot1] + quicksort_copy(mid) + [pivot2] + quicksort_copy(right)

# ************ Merge Sort *************

# https://upload.wikimedia.org/wikipedia/commons/c/cc/Merge-sort-example-300px.gif?20151222172210

def mergesort(L):
    if len(L) <= 1:
        return
    mid = len(L) // 2
    left, right = L[:mid], L[mid:]

    mergesort(left)
    mergesort(right)
    temp = merge(left, right)

    for i in range(len(temp)):
        L[i] = temp[i]

def merge(left : list, right : list):
    L = []
    i = j = 0

    while i < len(left) or j < len(right):
        if i >= len(left):
            L.append(right[j])
            j += 1

        elif j >= len(right):
            L.append(left[i])
            i += 1

        else:
            if left[i] <= right[j]:
                L.append(left[i])
                i += 1

            else:
                L.append(right[j])
                j += 1
    return L

# ************ BU Merge Sort (the iterative approach) *************

def bottom_up_mergesort(L : list):
    # Base Case ;
    if len(L) <= 1:
        return
        
    width = 1 # window size
    while width < len(L): # inc window size (width) of sub-arrays
        l = 0
        # print('\n')
        while l < len(L) - width: # iterate through the entire list merging sub-arrays
            r = min(l + (width*2), len(L))         
            m = min(l + width, len(L))
            left, right = L[l:m], L[m:r]
            # 2 sorted lists will be merged to get the full sorted list ;
            temp = merge(left, right)
            print("merged to : ",temp)

            # copying ;
            L[l:r] = temp

            l += width*2
        width = width * 2

# ************* Heap Sort *************

def heapsort(L):
    heap = Heap(L)
    for _ in range(len(L)):
        heap.extract_max()

class Heap:
    length = 0
    data = []

    def __init__(self, L):
        self.data = L
        self.length = len(L)
        self.build_heap()

    def build_heap(self):
        for i in range(self.length // 2 - 1, -1, -1):
            self.heapify(i)

    def heapify(self, i):
        largest_known = i
        if self.left(i) < self.length and self.data[self.left(i)] > self.data[i]:
            largest_known = self.left(i)
        if self.right(i) < self.length and self.data[self.right(i)] > self.data[largest_known]:
            largest_known = self.right(i)
        if largest_known != i:
            self.data[i], self.data[largest_known] = self.data[largest_known], self.data[i]
            self.heapify(largest_known)

    def insert(self, value):
        if len(self.data) == self.length:
            self.data.append(value)
        else:
            self.data[self.length] = value
        self.length += 1
        self.bubble_up(self.length - 1)

    def insert_values(self, L):
        for num in L:
            self.insert(num)

    def bubble_up(self, i):
        while i > 0 and self.data[i] > self.data[self.parent(i)]:
            self.data[i], self.data[self.parent(i)] = self.data[self.parent(i)], self.data[i]
            i = self.parent(i)

    def extract_max(self):
        self.data[0], self.data[self.length - 1] = self.data[self.length - 1], self.data[0]
        max_value = self.data[self.length - 1]
        self.length -= 1
        self.heapify(0)
        return max_value

    def left(self, i):
        return 2 * (i + 1) - 1

    def right(self, i):
        return 2 * (i + 1)

    def parent(self, i):
        return (i + 1) // 2 - 1

    def __str__(self):
        height = math.ceil(math.log(self.length + 1, 2))
        whitespace = 2 ** height
        s = ""
        for i in range(height):
            for j in range(2 ** i - 1, min(2 ** (i + 1) - 1, self.length)):
                s += " " * whitespace
                s += str(self.data[j]) + " "
            s += "\n"
            whitespace = whitespace // 2
        return s


# **************** Tests ********************    

def create_random_list(length, max_value):
    L = []
    for _ in range(length):
        L.append(random.randint(0, max_value))
    return L

# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L

def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


def quick_test(n, m, step):
    times = []
    lengths = []
    for i in range(1, n, step):
        L1 = create_random_list(i,i)
        # L1 = create_near_sorted_list(i, i,5)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            # print("L1 b4 = ",L1,'\n')
            start = timeit.default_timer()
            quicksort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

def dual_quick_test(n, m, step):
    times = []
    lengths = []
    for i in range(1, n, step):
        L1 = create_random_list(i,i)
        # L1 = create_near_sorted_list(i, i,5)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            # print("L1 b4 = ",L1,'\n')
            start = timeit.default_timer()
            dual_quicksort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))
        # print("L1 after = ",L1,'\n')
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return lengths, times

def merge_test(n, m, step):
    times = []
    lengths = []
    for i in range(1, n, step):
        L1 = create_random_list(i,i)
        # L1 = create_near_sorted_list(i, i,5)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            start = timeit.default_timer()
            mergesort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

def bu_merge_test(n, m, step):
    times = []
    lengths = []
    for i in range(1, n, step):
        L1 = create_random_list(i,i)
        # L1 = create_near_sorted_list(i, i,5)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            start = timeit.default_timer()
            bottom_up_mergesort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

def heap_test(n, m, step):
    times = []
    lengths = []
    for i in range(1, n, step):
        L1 = create_random_list(i,i)
        # L1 = create_near_sorted_list(i, i,5)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            start = timeit.default_timer()
            heapsort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

lengths1, times1 = quick_test(10000,5,100)
length2, times2 = heap_test(1000,100,50)
lengths3, times3 = merge_test(10000,5,100)
# print(lengths3)
# lengths5, times5 = bu_merge_test(10000,5,100)
# lengths4, times4 = dual_quick_test(10000,5,100)


plot.plot(lengths1,times1,'b-',label = "quick_sort")
plot.plot(length2,times2,'r-',label = "heap_sort")
plot.plot(lengths3,times3,'g-',label = "merge_sort")
# plot.plot(lengths5,times5,'r-',label = "BU_merge_sort")
# # plot.plot(lengths4,times4,'m-',label = "dual_quick_sort")

plot.xlabel('list/item size') 
plot.ylabel('Time Taken (s)')

plot.legend()
plot.show()