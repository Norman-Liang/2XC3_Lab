"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import random
import timeit
import matplotlib.pyplot as plot


# Create a random list length "length" containing whole numbers between 0 and max_value inclusive
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]


# Creates a near sorted list by creating a random list, sorting it, then doing a random number of swaps
def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L


# I have created this function to make the sorting algorithm code read easier
def swap(L, i, j):
    L[i], L[j] = L[j], L[i]


# ******************* Insertion sort code *******************

# This is the traditional implementation of Insertion Sort.
def insertion_sort(L):
    for i in range(1, len(L)):
        insert(L, i)


def insert(L, i):
    while i > 0:
        if L[i] < L[i-1]:
            swap(L, i-1, i)
            i -= 1
        else:
            return

# This is the optimization/improvement we saw in lecture **********************************
def insertion_sort2(L):
    for i in range(1, len(L)):
        insert2(L, i)


def insert2(L, i):
    value = L[i]
    while i > 0:
        if L[i - 1] > value:
            L[i] = L[i - 1]
            i -= 1
        else:
            L[i] = value
            return
    L[0] = value


# ******************* Bubble sort code *******************

# Traditional Bubble sort
def bubble_sort(L):
    for i in range(len(L)):
        for j in range(len(L) - 1):
            if L[j] > L[j+1]:
                swap(L, j, j+1)


# ******************* Selection sort code *******************

# Traditional Selection sort
def selection_sort(L):
    for i in range(len(L)):
        min_index = find_min_index(L, i)
        swap(L, i, min_index)


def find_min_index(L, n):
    min_index = n
    for i in range(n+1, len(L)):
        if L[i] < L[min_index]:
            min_index = i
    return min_index

# *************************** testing *********************************************

def bubble_test(n, m, step):
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
            bubble_sort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

def insertion_test(n, m, step):
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
            insertion_sort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

def selection_test(n, m, step):
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
            selection_sort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        lengths.append(len(L1))

    return lengths, times

lengths1, times1 = bubble_test(1000,25,100)
print(lengths1)
lengths2, times2 = insertion_test(1000,25,100)
lengths3, times3 = selection_test(1000,25,100)


plot.plot(lengths1, times1, 'b-', label = "bubble_sort")
plot.plot(lengths2, times2, 'g-', label = "insertion_sort")
plot.plot(lengths3, times3, 'r-', label = "selection_sort")

plot.xlabel('list/item size') 
plot.ylabel('Time Taken (s)')

plot.legend()
plot.show()