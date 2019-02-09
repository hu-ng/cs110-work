import time
import matplotlib.pyplot as plt
import random


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
        left = alist[:mid1]
        middle = alist[mid1:mid2]
        right = alist[mid2:]

        # Recursively call three_way_merge on the three thirds.
        merge_insertion(left)
        merge_insertion(middle)
        merge_insertion(right)

        # i, y, j are indices of left, middle, and right.
        # k is the index of the main list.
        i = 0
        y = 0
        j = 0
        k = 0

        while i < len(left) or y < len(middle) or j < len(right):
            # min_val is used to keep track of the smallest element in the current loop instance.
            min_val = float('inf')

            # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.
            if i < len(left):
                if left[i] < min_val:
                    min_val = left[i]

            if y < len(middle):
                if middle[y] < min_val:
                    min_val = middle[y]

            if j < len(right):
                if right[j] < min_val:
                    min_val = right[j]

            alist[k] = min_val
            k += 1

            # Incrementation of either i, y, or j.
            if i < len(left):
                if min_val == left[i]:
                    i += 1

            if y < len(middle):
                if min_val == middle[y]:
                    y += 1

            if j < len(right):
                if min_val == right[j]:
                    j += 1
        # print("Merging ", alist)


def three_way_merge(alist):
    # Solve for edge case: a list of 2 cannot be further divided by 3.
    if len(alist) == 2:
        if alist[1] < alist[0]:
            alist[1], alist[0] = alist[0], alist[1]

    # print("Splitting ", alist)
    if len(alist) >= 3:
        mid1 = len(alist)//3
        mid2 = mid1*2

        # Divide the list using slicing.
        left = alist[:mid1]
        middle = alist[mid1:mid2]
        right = alist[mid2:]

        # Recursively call three_way_merge on the three thirds.
        three_way_merge(left)
        three_way_merge(middle)
        three_way_merge(right)

        i = 0
        y = 0
        j = 0
        k = 0

        while i < len(left) or y < len(middle) or j < len(right):
            # min_val is used to keep track of the smallest element in the current loop instance.
            min_val = float('inf')

            # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.
            if i < len(left):
                if left[i] < min_val:
                    min_val = left[i]

            if y < len(middle):
                if middle[y] < min_val:
                    min_val = middle[y]

            if j < len(right):
                if right[j] < min_val:
                    min_val = right[j]

            alist[k] = min_val
            k += 1

            if i < len(left):
                if min_val == left[i]:
                    i += 1

            if y < len(middle):
                if min_val == middle[y]:
                    y += 1

            if j < len(right):
                if min_val == right[j]:
                    j += 1

        # print("Merging ", alist)


def mergesort (A, start, end):
    if start < end:
        mid = (start + end) // 2
        mergesort(A, start, mid)
        mergesort(A, mid + 1, end)
        merge(A, start, mid, end)
    return A


def merge(A, start, mid, end):
    n1 = mid - start + 1
    n2 = end - mid
    L = [None]*(n1 + 1)
    R = [None]*(n2 + 1)
    for i in range(n1):
        L[i] = A[start + i]
    for j in range(n2):
        R[j] = A[mid + 1 + j]
    L[n1] = float('inf')
    R[n2] = float('inf')
    i = 0
    j = 0
    for k in range(start, end + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def average_run_time(num_values, num_lists):
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

    average_merge = sum(run_time_merge)/len(run_time_merge)
    average_threeway = sum(run_time_threeway)/len(run_time_threeway)
    average_insertion = sum(run_time_insertion)/len(run_time_insertion)
    return average_merge


def graph_runtimes2(num_values, num_lists):
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


def graph_runtimes(length_lst, repeats):
    merge_avg = []
    three_way_avg = []
    merge_insert_avg = []

    for i in range(length_lst):
        merge_lst = []
        three_way_lst = []
        merge_insert_lst = []

        for x in range(repeats):
            mylist = random.sample(range(i), i)

            start_time = time.time()
            mergesort(mylist, 0, len(mylist) - 1)
            finish_time = time.time() - start_time
            merge_lst.append(finish_time)

            start_time = time.time()
            three_way_merge(mylist)
            finish_time = time.time() - start_time
            three_way_lst.append(finish_time)

            start_time = time.time()
            merge_insertion(mylist)
            finish_time = time.time() - start_time
            merge_insert_lst.append(finish_time)

        avg_merge = sum(merge_lst)/len(merge_lst)
        avg_three_way = sum(three_way_lst)/len(three_way_lst)
        avg_merge_insert = sum(merge_insert_lst)/len(merge_insert_lst)

        merge_avg.append(avg_merge)
        three_way_avg.append(avg_three_way)
        merge_insert_avg.append(avg_merge_insert)

    plt.plot(merge_avg, color='red', label = '2-way Merge')
    plt.plot(three_way_avg, color='blue', label = '3-way Merge')
    plt.plot(merge_insert_avg, color='green', label = '3-way Insertion Merge')
    plt.xlabel("Length of the list")
    plt.ylabel("Average run-time")
    plt.legend()
    plt.show()

graph_runtimes2(200, 800)