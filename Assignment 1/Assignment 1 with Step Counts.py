import math

# stepified. Check again for the steps, seems kinda weird
def insertionsort(list):
    step_ins = 0
    for j in range(1, len(list)):
        key = list[j]
        i = j - 1
        step_ins += 3
        step_ins += 2
        while i > -1 and list[i] > key:
            list[i + 1] = list[i]
            i = i - 1
            step_ins += 2
        list[i + 1] = key
        step_ins += 1
    return step_ins

# stepified
def merge_insertion(alist, index):
    global step_merge
    global step_ins

    step_merge = 0
    step_ins = 0

    print("Splitting ", alist)

    # If the length of the list is below the chosen index, insertion sort is called.
    if len(alist) < index:
        print('Insertion Sort', alist)
        step_ins = insertionsort(alist)
        print('Finished', alist, 'with {} steps'.format(step_ins))
        step_merge += 2

    if len(alist) >= index:
        mid1 = len(alist)//3
        mid2 = mid1*2

        # Divide the list using subsets.
        lefthalf = alist[:mid1]
        middle = alist[mid1:mid2]
        righthalf = alist[mid2:]
        step_merge += 6

        # Recursively call three_way_merge on the three thirds.
        merge_insertion(lefthalf, index)
        step_merge += 1
        merge_insertion(middle, index)
        step_merge += 1
        merge_insertion(righthalf, index)
        step_merge += 1

        # i, y, j are indices of lefthalf, middle, and righthalf.
        # k is the index of the main list.
        i = 0
        y = 0
        j = 0
        k = 0

        while i < len(lefthalf) or y < len(middle) or j < len(righthalf):
            # min_val is used to keep track of the smallest element in the current loop instance.
            min_val = float('inf')
            step_merge += 1
            # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.

            step_merge += 1
            if i < len(lefthalf):
                step_merge += 1
                if lefthalf[i] < min_val:
                    min_val = lefthalf[i]
                    step_merge += 1

            step_merge += 1
            if y < len(middle):
                step_merge += 1
                if middle[y] < min_val:
                    min_val = middle[y]
                    step_merge += 1

            step_merge += 1
            if j < len(righthalf):
                step_merge += 1
                if righthalf[j] < min_val:
                    min_val = righthalf[j]
                    step_merge += 1

            alist[k] = min_val
            k += 1

            step_merge += 2

            # Incrementation of either i, y, or j.

            step_merge += 1
            if i < len(lefthalf):
                step_merge += 1
                if min_val == lefthalf[i]:
                    i += 1
                    step_merge += 1
            step_merge += 1
            if y < len(middle):
                step_merge += 1
                if min_val == middle[y]:
                    y += 1
                    step_merge += 1
            step_merge += 1
            if j < len(righthalf):
                step_merge += 1
                if min_val == righthalf[j]:
                    j += 1
                    step_merge += 1

        print("Merging ", alist)
    return step_merge + step_ins

# stepified
def three_way_merge(alist):
    global steps
    steps = 0

    # Solve for edge case: a list of 2 cannot be further divided by 3.
    steps += 1
    if len(alist) == 2:
        steps += 1
        if alist[1] < alist[0]:
            alist[1], alist[0] = alist[0], alist[1]
            steps += 1

    print("Splitting ", alist)
    steps += 1
    if len(alist) >= 3:
        mid1 = len(alist)//3
        mid2 = mid1*2
        steps += 2

        # Divide the list using subsets.
        lefthalf = alist[:mid1]
        middle = alist[mid1:mid2]
        righthalf = alist[mid2:]
        steps += 3

        # Recursively call three_way_merge on the three thirds.
        three_way_merge(lefthalf)
        steps += 1
        three_way_merge(middle)
        steps += 1
        three_way_merge(righthalf)
        steps += 1

        i = 0
        y = 0
        j = 0
        k = 0

        steps += 3
        while i < len(lefthalf) or y < len(middle) or j < len(righthalf):
            # min_val is used to keep track of the smallest element in the current loop instance.
            min_val = float('inf')
            steps += 1
            # Due to the 'or' clause, the 'if' clauses are used to avoid index errors.

            steps += 1
            if i < len(lefthalf):
                steps += 1
                if lefthalf[i] < min_val:
                    steps += 1
                    min_val = lefthalf[i]

            steps += 1
            if y < len(middle):
                steps += 1
                if middle[y] < min_val:
                    steps += 1
                    min_val = middle[y]

            steps += 1
            if j < len(righthalf):
                steps += 1
                if righthalf[j] < min_val:
                    steps += 1
                    min_val = righthalf[j]

            alist[k] = min_val
            k += 1
            steps += 2

            steps += 1
            if i < len(lefthalf):
                steps += 1
                if min_val == lefthalf[i]:
                    steps += 1
                    i += 1

            steps += 1
            if y < len(middle):
                steps += 1
                if min_val == middle[y]:
                    steps += 1
                    y += 1

            steps += 1
            if j < len(righthalf):
                steps += 1
                if min_val == righthalf[j]:
                    steps += 1
                    j += 1

        print("Merging ", alist)
    return steps

alist = [9,8,7,6,5,4,3,2,1]
alist2 = [5,4,3,2,1]

print(merge_insertion(alist, 5))
print(alist)
