#Hung
import math

def mergesort (A, start, end):
    mid1 = (end + start) // 3
    mid2 = (end + mid1) // 2
    print(mid1, mid2)
    if end - start >= 1 and start <= mid1:
        mergesort(A, start, mid1)
        #print(start, mid1)
        mergesort(A, mid1 + 1, mid2)
        print(mid1 + 1, mid2)
        mergesort(A, mid2 + 1, end)
        #print(mid2 + 1, end)
        #print(start, mid1, mid2, end)
        merge(A, start, mid1, mid2, end)

    return A

def merge(A, start, mid1, mid2, end):
    n1 = mid1 - start + 1
    n2 = mid2 - mid1
    n3 = end - mid2
    L = [None]*(n1 + 1)
    M = [None]*(n2 + 1)
    R = [None]*(n3 + 1)
    for i in range(n1):
        L[i] = A[start + i]
    for j in range(n2):
        M[j] = A[mid1 + 1 + j]
    for y in range(n3):
        R[y] = A[mid2 + 1 + y]
    print(L, M, R)
    L[n1] = math.inf
    M[n2] = math.inf
    R[n3] = math.inf
    i = 0
    j = 0
    y = 0
    for k in range(start, end + 1):
        if L[i] <= M[j] and L[i] <= R[y]:
            A[k] = L[i]
            i += 1
        elif M[j] <= L[i] and M[j] <= R[y]:
            A[k] = M[j]
            j += 1
        else:
            A[k] = R[y]
            y += 1


# list = [9,8,7,6,5,4,3,2,1]
L = [9,8,7,6,5,4,3,2,1]
print(mergesort(L, 0, len(L) - 1))