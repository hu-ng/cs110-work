import bisect


def bin_sort(lst, s, e, extend):
    """Binary insertion sort, assumed that lst[s:e + 1] is sorted.
    Extend the run by the number indicated by 'extend'"""

    for i in range(1, extend + 1):
        pos = 0
        start = s
        end = e + i
        value = lst[end]

        if value >= lst[end - 1]:
            continue

        while start <= end:
            if start == end:
                print('start == end condition')
                if lst[start] > value:
                    pos = start
                    break
                else:
                    pos = start + 1
                    break
            mid = (start + end) // 2
            if value >= lst[mid]:
                start = mid + 1
            else:
                end = mid - 1

        if start > end:
            print('start > end condition')
            pos = start

        if pos > e + i:
            print('pos > e + i condition')
            pos -= 1

        for x in range(e + i, pos, - 1):
            lst[x] = lst[x - 1]
        lst[pos] = value


lst = [12,13,14,15,16,1,2,3,4,5]
lst2 = [1,1,1,1,1,1,1,1,1,1,1]
bin_sort(lst2, 0, 4, 6)
print(lst2)