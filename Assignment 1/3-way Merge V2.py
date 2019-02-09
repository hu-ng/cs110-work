def mergeSort(alist):
    if len(alist) == 2:
        if alist[1] < alist[0]:
            alist[1], alist[0] = alist[0], alist[1]
    print("Splitting ", alist)
    if len(alist) >= 3:
        mid1 = len(alist)//3
        mid2 = mid1*2
        lefthalf = alist[:mid1]
        middle = alist[mid1:mid2]
        righthalf = alist[mid2:]

        mergeSort(lefthalf)
        mergeSort(middle)
        mergeSort(righthalf)

        i = 0
        j = 0
        y = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf) and y < len(middle):
            if lefthalf[i] < righthalf[j] and lefthalf[i] < middle[y]:
                alist[k] = lefthalf[i]
                i += 1
            elif righthalf[j] < lefthalf[i] and righthalf[j] < middle[y]:
                alist[k] = righthalf[j]
                j += 1
            else:
                alist[k] = middle[y]
                y += 1
            k = k + 1

        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k] = righthalf[j]
                k = k+1
            k = k +1

        while j < len(righthalf) and y < len(middle):
            if righthalf[j] < middle[y]:
                alist[k]=righthalf[j]
                j = j + 1

            else:
                alist[k] = middle[y]
                y = y + 1
            k = k + 1

        while y < len(middle) and i < len(lefthalf):
            if middle[y] < lefthalf[i]:
                alist[k] = middle[y]
                y = y + 1
            else:
                alist[k] = lefthalf[i]
                i = i + 1
            k = k + 1

        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            alist[k] = righthalf[j]
            j += 1
            k += 1

        while y < len(middle):
            alist[k] = middle[y]
            y += 1
            k += 1

    print("Merging ", alist)

alist = [7,6,5,4,3,2,1,8]
mergeSort(alist)
print(alist)
