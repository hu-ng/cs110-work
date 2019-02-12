def three_way_merge(alist, l , r):
    # Solve for edge case: a list of 2 cannot be further divided by 3.
    if r - l > 1:
        mid1 = l + (r - l)//3
        mid2 = l +2*(r - l)//3

        three_way_merge(alist, l, mid1)
        three_way_merge(alist, mid1, mid2)
        three_way_merge(alist, mid2, r)

        merge_three(alist, l, mid1, mid2, r)
    return alist

def merge_three(alist, l, mid1, mid2, r):
    left = alist[l:mid1] + [float('inf')]
    middle = alist[mid1:mid2] + [float('inf')]
    right = alist[mid2:r] + [float('inf')]
    left_idx = 0
    mid_idx = 0
    right_idx = 0

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
