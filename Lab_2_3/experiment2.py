import random
import timeit
import matplotlib.pyplot as plot

# Create a random list length "length" containing whole numbers between 0 and max_value inclusive
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]

def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp
    
#Traditional bubble sort
def bubblesort(L):
    for i in range(len(L)):
        for j in range(len(L)-i-1):
            if L[j] > L[j+1]:
                swap(L,j,j+1)

def bubblesort2(L):
    for i in range(len(L)):
        for j in range(len(L)-i-1):
            value = L[j]
            if value > L[j+1]:
                L[j] = L[j+1]
                L[j+1] = value
                
def selectsort(L):
    for i in range(len(L)):
        min_pos = i
        for j in range(i+1, len(L)):
            if L[j] < L[min_pos]:
                min_pos = j
        swap(L, i, min_pos)

def selectsort2(L):
    for i in range(len(L)//2):
        min_pos = i
        max_pos = i
        for j in range(i+1, len(L)-i):
            if L[j] < L[min_pos]:
                min_pos = j
            if L[j] > L[max_pos]:
                max_pos = j
        swap(L,i,min_pos)
        swap(L,len(L)-i-1,max_pos)

def experiment(n, k,step):
    times = []
    lengths = []
    for i in range(1,n,step):
        time = 0
        L = create_random_list(i,i)
        L2 = L.copy()
        for _ in range(k):
            L = L2.copy()
            start = timeit.default_timer()
            # Change for different sorting algorithm
            bubblesort(L)
            end = timeit.default_timer()
            time = end - start
        times.append(time/k)
        lengths.append(len(L))
    return lengths, times

def experimentMod(n, k,step):
    times = []
    lengths = []
    for i in range(1,n,step):
        time = 0
        L = create_random_list(i,i)
        L2 = L.copy()
        for _ in range(k):
            L = L2.copy()
            start = timeit.default_timer()
            # Change for different sorting algorithm
            bubblesort2(L)
            end = timeit.default_timer()
            time = end - start
        times.append(time/k)
        lengths.append(len(L))
    return lengths, times

total1 = 0
total2 = 0
n = 1000
k = 20
step = 100

for i in range(1, n, step):
    for num in range(k):
        L = create_random_list(i, i)
        L2 = L.copy()

        start = timeit.default_timer()
        # Change for different sorting algorithm 
        selectsort(L)
        end = timeit.default_timer()
        total1 += end - start

        start = timeit.default_timer()
        # Change for different sorting algorithm
        selectsort2(L2)
        end = timeit.default_timer()
        total2 += end - start

    print("\nList Length: " + str(i) + "\nMethod 1: ", total1/k)
    print("Method 2: ", total2/k)
    print("Improvement of ", (1 - total2/total1) * 100, "%")

lengths, times = experiment(n,k,50)
lengthsMod, timesMod = experimentMod(n,k,50)

plot.plot(lengths, times, 'g-', label = "Regular bubble sort")
plot.plot(lengthsMod, timesMod, 'r-', label = "Modified bubble sort")
plot.xlabel("List Length") 
plot.ylabel('Time Taken (s)')
plot.legend()
plot.show()