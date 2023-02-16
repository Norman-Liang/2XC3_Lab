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

def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

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

def experiment(n, k, s):
    times = []
    swaps = []
    for i in range(s): # swaps
        L = create_near_sorted_list(n,n,i)
        L2 = L.copy()
        time = 0
        for _ in range(k):
            L = L2.copy()
            start = timeit.default_timer()
            quicksort(L)
            end = timeit.default_timer()
            time += end - start
        times.append(time/k)
        swaps.append(i)
    return swaps, times

total = 0
n = 100
k = 50
s = 100
step = 100

for _ in range(k):
    L = create_near_sorted_list(n, n, s)

    start = timeit.default_timer()
    quicksort(L)
    end = timeit.default_timer()
    total += end - start

print("Runtime: ", total/k)

swaps, times = experiment(n,k,s)
plot.plot(swaps, times)
plot.xlabel("Swaps away from sorted") 
plot.ylabel('Time Taken (s)')
plot.show()