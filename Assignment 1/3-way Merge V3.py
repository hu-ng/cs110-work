def three_way_merge(alist):
    # Solve for edge case: a list of 2 cannot be further divided by 3.
    if len(alist) == 2:
        if alist[1] < alist[0]:
            alist[1], alist[0] = alist[0], alist[1]

    print("Splitting ", alist)
    if len(alist) >= 3:
        mid1 = len(alist)//3
        mid2 = mid1*2

        # Divide the list using subsets.
        lefthalf = alist[:mid1]
        middle = alist[mid1:mid2]
        righthalf = alist[mid2:]

        # Recursively call three_way_merge on the three thirds.
        three_way_merge(lefthalf)
        three_way_merge(middle)
        three_way_merge(righthalf)

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

        print("Merging ", alist)

alist = [9,8,7,6,5,4,3,2,1,12,12,13,14]
three_way_merge(alist)
print(alist)
