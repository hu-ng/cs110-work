import math
import time
import matplotlib.pyplot as plt
import random
import numpy as np


def insertionsort(list):
    for j in range(1, len(list)):
        key = list[j]
        i = j - 1
        while i > -1 and list[i] > key:
            list[i + 1] = list[i]
            i = i - 1
        list[i + 1] = key


def merge_insertion(alist):
    # print("Splitting ", alist)

    # If the length of the list is below the chosen index, insertion sort is called.
    if len(alist) < 4:
        # print('Insertion Sort', alist)
        insertionsort(alist)
        # print('Finished', alist)

    if len(alist) >= 4:
        mid1 = len(alist)//3
        mid2 = mid1*2

        # Divide the list using subsets.
        lefthalf = alist[:mid1]
        middle = alist[mid1:mid2]
        righthalf = alist[mid2:]

        # Recursively call three_way_merge on the three thirds.
        merge_insertion(lefthalf)
        merge_insertion(middle)
        merge_insertion(righthalf)

        # i, y, j are indices of lefthalf, middle, and righthalf.
        # k is the index of the main list.
        i = 0
        y = 0
        j = 0
        k = 0

        while i < len(lefthalf) or y < len(middle) or j < len(righthalf):
            # min_val is used to keep track of the smallest element in the current loop instance.
            min_val = float('inf')

            # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.
            if i < len(lefthalf):
                if lefthalf[i] < min_val:
                    min_val = lefthalf[i]

            if y < len(middle):
                if middle[y] < min_val:
                    min_val = middle[y]

            if j < len(righthalf):
                if righthalf[j] < min_val:
                    min_val = righthalf[j]

            alist[k] = min_val
            k += 1

            # Incrementation of either i, y, or j.
            if i < len(lefthalf):
                if min_val == lefthalf[i]:
                    i += 1

            if y < len(middle):
                if min_val == middle[y]:
                    y += 1

            if j < len(righthalf):
                if min_val == righthalf[j]:
                    j += 1
        # print("Merging ", alist)


def three_way_merge(alist, s, e):
    if e - s + 1 > 3:
        mid1 = (s + e)//3
        mid2 = (mid1 + e)//2

        print(mid1, mid2)
        # Recursively call three_way_merge on the three thirds.
        three_way_merge(alist, s, mid1)
        three_way_merge(alist, mid1 + 1, mid2)
        three_way_merge(alist, mid2 + 1, e)

    if e - s == 2:
        mid1 = e
        mid2 = mid1 + 1

        print(s, mid1, mid2, e)
        three_way_merge(alist, s, mid1)
        three_way_merge(alist, mid1 + 1, mid2)
        three_way_merge(alist, mid2 + 1, e)

    if e - s == 1:
        if alist[e] > alist[s]:
            alist[e], alist[s] = alist[s], alist[e]


def merge_three(s, mid1, mid2, e):
    # Copy the numbers from the arrays into their lists.

    lefthalf = [None]*(mid1 - s + 1)
    middle = [None]*(mid2 - mid1)
    righthalf = [None]*(e - mid2)

    for i in range(len(lefthalf)):
        lefthalf[i] = alist[s + i]
    for y in range(len(middle)):
        middle[y] = alist[mid1 + 1 + y]
    for j in range(len(righthalf)):
        righthalf[j] = alist[mid2 + 1 + j]

    print(lefthalf, middle, righthalf)
    i = 0
    y = 0
    j = 0
    k = 0

    while i < len(lefthalf) or y < len(middle) or j < len(righthalf):
        # min_val is used to keep track of the smallest element in the current loop instance.
        min_val = float('inf')

        # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.
        if i < len(lefthalf):
            if lefthalf[i] < min_val:
                min_val = lefthalf[i]

        if y < len(middle):
            if middle[y] < min_val:
                min_val = middle[y]

        if j < len(righthalf):
            if righthalf[j] < min_val:
                min_val = righthalf[j]

        alist[k] = min_val
        k += 1

        if i < len(lefthalf):
            if min_val == lefthalf[i]:
                i += 1

        if y < len(middle):
            if min_val == middle[y]:
                y += 1

        if j < len(righthalf):
            if min_val == righthalf[j]:
                j += 1


def mergesort (A, p, r):
    if p < r:
        q = (p + r)//2
        mergesort(A, p, q)
        mergesort(A, q + 1, r)
        merge(A, p, q, r)
    return A


def merge(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    L = [None]*(n1 + 1)
    R = [None]*(n2 + 1)
    for i in range(n1):
        L[i] = A[p + i]
    for j in range(n2):
        R[j] = A[q + 1 + j]
    L[n1] = math.inf
    R[n2] = math.inf
    i = 0
    j = 0
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def average_run_time(num_values, num_lists):
    run_times = []
    for i in range(num_lists):
        mylist = random.sample(range(num_values), num_values)
        start_time = time.time()
        # mergesort(mylist, 0, len(mylist) - 1)
        # three_way_merge(mylist)
        merge_insertion(mylist)
        finish_time = time.time() - start_time
        run_times.append(finish_time)
    average = sum(run_times)/len(run_times)
    return average


def graph_runtimes(num_values, num_lists):
    run_time_merge = []
    run_time_threeway = []
    run_time_insertion = []
    for i in range(num_lists):
        mylist = random.sample(range(num_values), num_values)

        start_time = time.time()
        mergesort(mylist, 0, len(mylist) - 1)
        finish_time = time.time() - start_time
        run_time_merge.append(finish_time)

        start_time = time.time()
        three_way_merge(mylist)
        finish_time = time.time() - start_time
        run_time_threeway.append(finish_time)

        start_time = time.time()
        merge_insertion(mylist)
        finish_time = time.time() - start_time
        run_time_insertion.append(finish_time)


    normal_merge = plt.plot(run_time_merge, color = 'red')
    three_way = plt.plot(run_time_threeway, color = 'blue')
    three_way_insertion = plt.plot(run_time_insertion, color = 'green')
    plt.ylabel('Run time in seconds')
    plt.show()