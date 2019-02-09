#Hung
import math
import time


steps = 0
def mergesort (A, p, r):
    global steps
    if p < r:
        q = (p + r)//2
        steps += 1
        mergesort(A, p, q)
        steps += 1
        mergesort(A, q + 1, r)
        steps += 1
        merge(A, p, q, r)
    return steps


def merge(A, p, q, r):
    global steps
    n1 = q - p + 1
    n2 = r - q
    steps += 2
    L = [None]*(n1 + 1)
    R = [None]*(n2 + 1)
    steps += 2
    for i in range(n1):
        L[i] = A[p + i]
        steps += 2
    for j in range(n2):
        R[j] = A[q + 1 + j]
        steps += 2
    L[n1] = math.inf
    R[n2] = math.inf
    steps += 2
    i = 0
    j = 0
    steps += 2
    for k in range(p, r + 1):
        steps += 1
        steps += 1
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
            steps += 2
        else:
            A[k] = R[j]
            j += 1
            steps += 2


list = [9,8,7,6,5,4,3,2,1]
mergesort(list, 0, len(list) - 1)
print(list)
print("Running time is {} steps".format(steps))