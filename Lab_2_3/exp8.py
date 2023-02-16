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

# To start with a oriented list and then slowly disorient it with each swap
def create_disoriented_list(length, max_value, swaps):
    L = create_near_sorted_list(length, max_value, 0)
    L.sort()
    for i in range(1, swaps + 1):
        L = create_near_sorted_list(length, max_value, i)
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

# *************************************


# ************ Merge Sort *************

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


def merge(left, right):
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

def hybrid_inmer_sort(L,optval):
    if len(L) <= optval:
        insertion_sort2(L)
    else:
        mergesort(L)

#optval=5 or anything, depending on list and swaps given.

        
#*************************************
#******************** Tester function for insertion sort **************

def insertion_sort_test(n, m, step):
    times = []
    listlength = []
    for i in range(1, n, step):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(i,i,i)
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
        listlength.append(len(L1))
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return listlength, times

#******************** Tester function for quick sort **************

def quicksort_test(n, m, step):
    times = []
    listlength = []
    for i in range(1, n, step):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(i,i,i)
        L2 = L1.copy()
        time = 0
        for _ in range(m):
            L1 = L2.copy()
            start = timeit.default_timer()
            quicksort(L1)
            end = timeit.default_timer()
            time += end - start
        avg_time = time / m
        times.append(avg_time)
        listlength.append(len(L1))
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return listlength, times

#******************** Tester function for merge sort **************

def merge_sort_test(n, m, step):
    times = []
    listlength = []
    for i in range(1, n, step):
        # L1 = create_random_list(i,i)
        L1 = create_near_sorted_list(i,i,i)
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
        listlength.append(len(L1))
        # x-axis will have m as limit since times.append is called in the loop with range(m)

    return listlength, times

#*************************Graph*********************

listlength, times = insertion_sort_test(25,5,1)
print(listlength,times)
plot.plot(listlength, times,'b-',label = "Insertion Sort")

listlength, times = quicksort_test(25,5,1)
print(listlength,times)
plot.plot(listlength, times,'g-',label = "Quick Sort")

listlength, times = merge_sort_test(25,5,1)
print(listlength,times)
plot.plot(listlength, times,'r-',label = "Merge Sort")

#times2 = experiement2(10000,100)
#times3 = experiement3(1000000)
#plot.plot(times3)
#plot.plot(times1,'b-',label = ".copy()")
#plot.plot(times2,'r-',label = 'item lookup')
plot.xlabel('List Length') 
plot.ylabel('Time Taken (s)')
plot.legend()
plot.show()
