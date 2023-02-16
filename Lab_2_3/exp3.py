"""
This file corresponds to the first graded lab of 2XC3.
Feel free to modify and/or add functions to this file.
"""
import timeit
import random
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


# This is the optimization/improvement we saw in lecture
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

#******************** Tester function for insertion sort **************

def insertion_sort_test(n, m, swapp):
    times = []
    swaps = []
    for i in range(swapp):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(n,n,i)
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
        swaps.append(i)
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return swaps, times

#******************** Tester function for bubble sort **************

def bubble_sort_test(n, m, swapp):
    times = []
    swaps = []
    for i in range(swapp):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(n,n,i)
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
        swaps.append(i)
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return swaps, times

#******************** Tester function for selection sort **************

def selection_sort_test(n, m, swapp):
    times = []
    swaps = []
    for i in range(swapp):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(n,n,i)
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
        swaps.append(i)
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return swaps, times

#*************************Graph*********************

swaps, times = insertion_sort_test(1000,5,100)
print(times)
plot.plot(swaps, times,'b-',label = "Insertion Sort")

swaps, times = bubble_sort_test(1000,5,100)
#print(swaps,times)
plot.plot(swaps, times,'g-',label = "Bubble Sort")

swaps, times = selection_sort_test(1000,5,100)
#print(swaps,times)
plot.plot(swaps, times,'r-',label = "Selection Sort")

#times2 = experiement2(10000,100)
#times3 = experiement3(1000000)
#plot.plot(times3)
#plot.plot(times1,'b-',label = ".copy()")
#plot.plot(times2,'r-',label = 'item lookup')
plot.xlabel('Swaps') 
plot.ylabel('Time Taken (s)')
plot.legend()
plot.show()
