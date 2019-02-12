import time
import matplotlib.pyplot as plt
import random
import heapq


########### THREE WAY MERGESORT ###############


def three_way_merge(alist, l , r):
    # Solve for edge case: a list of 2 cannot be further divided by 3.
    if r - l > 1:

        # Find the midpoints
        mid1 = l + (r - l)//3
        mid2 = l +2*(r - l)//3

        # Recursively calls three_way_merge
        three_way_merge(alist, l, mid1)
        three_way_merge(alist, mid1, mid2)
        three_way_merge(alist, mid2, r)

        merge_three(alist, l, mid1, mid2, r)
    return alist

def merge_three(alist, l, mid1, mid2, r):

    # Reference the three parts of the list
    left = alist[l:mid1] + [float('inf')]
    middle = alist[mid1:mid2] + [float('inf')]
    right = alist[mid2:r] + [float('inf')]

    # initialize the index of the sublists
    left_idx = 0
    mid_idx = 0
    right_idx = 0

    # Compare the first element of each list to find the minimum value
    # Increment index counters appropriately
    for pos in range(l, r):
        min = None
        if left[left_idx] <= middle[mid_idx] and left[left_idx] <= right[right_idx]:
            min = left[left_idx]
            left_idx += 1
        elif right[right_idx] <= left[left_idx] and right[right_idx] <= middle[mid_idx]:
            min = right[right_idx]
            right_idx += 1
        else:
            min = middle[mid_idx]
            mid_idx += 1
        alist[pos] = min


########### MERGE INSERTION HYBRID ###############


def insertionsort(list):
    for j in range(1, len(list)):
        key = list[j]
        i = j - 1
        while i > -1 and list[i] > key:
            list[i + 1] = list[i]
            i = i - 1
        list[i + 1] = key


def merge_insertion(alist):
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


########### K-WAY MERGESORT ###############


def k_way_merge(lst, l, r, k):
    # If k is 1, don't allow the algorithm to run
    if k == 1:
        return
    # Base case where the list has 0 or 1 element
    if r - l <= 1:
        return lst

    # Calculate the indices in the middle
    mid_idx = [l + i*(r - l)//k for i in range(1, k)]

    # Use this list to continue the recursion
    to_sort = [l] + mid_idx + [r]

    # Recursively calls k_way_merge on k sublists
    for i in range(k):
        k_way_merge(lst, to_sort[i], to_sort[i + 1], k)

    k_merge(lst, to_sort)
    return lst

def k_merge(lst, idx_lst):
    # These are the boundaries of the merge
    l = idx_lst[0]
    r = idx_lst[-1]

    # list of k sorted sublists
    sorted = [lst[idx_lst[i]:idx_lst[i + 1]] for i in range(len(idx_lst) - 1) if lst[idx_lst[i]:idx_lst[i + 1]]]

    # initialize min_heap
    min_heap = []

    # Push the minimum element of each sorted sublist into the heap
    for list_index in range(len(sorted)):
        heapq.heappush(min_heap, (sorted[list_index][0], list_index, 0))

    # For every i in the merge boundaries, pop the minimum value from the heap
    # put it in the lst. Push the next element of the subarray to the heap if it's there.
    for i in range(l, r):
        val, list_index, val_index = heapq.heappop(min_heap)
        lst[i] = val

        if val_index + 1 < len(sorted[list_index]):
            heapq.heappush(min_heap, (sorted[list_index][val_index + 1],
                                      list_index, val_index + 1))


########### RUNTIME ANALYSIS ###############


# This function might take some time to run depending on how length_lst and repeats are chosen.
def graph_runtimes(length_lst, repeats):
    merge_avg = []
    three_way_avg = []
    merge_insert_avg = []

    for i in range(length_lst):
        merge_lst = []
        three_way_lst = []
        merge_insert_lst = []

        # repeats tells the for loop how many times to run the sort algorithms on mylist.
        # The larger repeats is, the more accurate the test will be.
        for x in range(repeats):
            # mylist is randomized at the beginning of every loop
            mylist = random.sample(range(i), i)

            # The running time of each algorithm on mylist is recorded in corresponding lists.
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

        # Results of the for loop are averaged.
        avg_merge = sum(merge_lst)/len(merge_lst)
        avg_three_way = sum(three_way_lst)/len(three_way_lst)
        avg_merge_insert = sum(merge_insert_lst)/len(merge_insert_lst)

        # Storing the average runtimes on different lengths of my list to another set of lists.
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
