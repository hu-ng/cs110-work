import bisect


def bisect_right(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """



    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x < a[mid]: hi = mid
        else: lo = mid+1
    return lo


def bisect_left(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] < x: lo = mid+1
        else: hi = mid
    return lo


def make_temp_array(lst, s, e):
    array = []
    while s <= e:
        array.append(lst[s])
        s += 1
    return array


def gallop(lst, val, low, high, ltr):
    # lst = original list
    # val = a value
    # ltr = tells the func to start looking from the right or the left.
    if ltr == True:
        # k = 1
        # not_found = True
        # while not_found:
        #     if lst[run[0] + 2**(k - 1)] < val and val <= lst[run[0] + 2**k]:
        #         not_found = False
        #     else:
        #         k += 1
        # # We use bisect_left here because we want whatever is to the left of pos is smaller,
        # # because we're inserting the value there
        pos = bisect_left(lst, val, low, high)
        return pos

    else:
        # k = 1
        # not_found = True
        # while not_found:
        #     if lst[run[1] - 2**k] <= val and val < lst[run[1] - 2**(k - 1)]:
        #         not_found = False
        #     else:
        #         k += 1
        pos = bisect_right(lst, val, low, high)
        return pos


def merge_low(lst, a, b, min_gallop):
    """Merges the two runs quasi in-place if a is the smaller array
    a and b are lists that store data of runs"""
    temp_array = make_temp_array(lst, a[0], a[1])
    # The first index of the sorting area
    k = a[0]
    # Counter for the temp array of a
    i = 0
    # Counter for b, starts at the beginning
    j = b[0]

    gallop_thresh = min_gallop
    while True:
        a_count = 0  # number of times a win in a row
        b_count = 0  # number of times b win in a row

        # Doing the normal merge, taking note of how many times a and b wins in a row.
        # If wins > threshold, break the loop and move to galloping
        print('enter normal')
        while i <= len(temp_array) - 1 and j <= b[1]:
            if temp_array[i] <= lst[j]:
                lst[k] = temp_array[i]
                k += 1
                i += 1

                a_count += 1
                b_count = 0

                # If a runs out during linear merge
                if i > len(temp_array) - 1:
                    while j <= b[1]:
                        lst[k] = lst[j]
                        k += 1
                        j += 1
                    return

                if a_count >= gallop_thresh:
                    break

            else:
                lst[k] = lst[j]
                k += 1
                j += 1

                a_count = 0
                b_count += 1

                # If b runs out during linear merge
                if j > b[1]:
                    while i <= len(temp_array) - 1:
                        lst[k] = temp_array[i]
                        k += 1
                        i += 1
                    return

                if b_count >= gallop_thresh:
                    break

        # If one run is winning consistently, switch to galloping mode.
        # i, j, and k is incremented accordingly
        while True:
            print('thresh', gallop_thresh)
            print('enter gallop')
            # Look for the position of B[j] in A
            # This calls bisect_left. a_adv is the index in the slice i, len(temp_array)
            # so that every element before temp_array{a_adv] is smaller than lst[j]
            a_adv = gallop(temp_array, lst[j], i, len(temp_array), True)
            # Copy the elements prior to a_adv to the merge area, increment k
            for x in range(i, a_adv):
                lst[k] = temp_array[x]
                k += 1

            # Update the a_count to check successfulness of galloping
            a_count = a_adv - i

            # Advance i to a_adv, two conditions might happen
            i = a_adv

            # # If i reached the last index of a
            # if i == len(temp_array) - 1:
            #     # If b ran out of elements
            #     if j > b[1]:
            #         lst[k] = temp_array[i]
            #         k += 1
            #         i += 1
            #     # If there are still elements in b: return to normal merge
            #     else:
            #         while i < len(temp_array) and j <= b[1]:
            #             if temp_array[i] <= lst[j]:
            #                 lst[k] = temp_array[i]
            #                 k += 1
            #                 i += 1
            #             else:
            #                 lst[k] = lst[j]
            #                 k += 1
            #                 j += 1
            #         if i < len(temp_array):
            #             lst[k] = temp_array[i]
            #             k += 1
            #             i += 1
            #         while j <= b[1]:
            #             lst[k] = lst[j]
            #             k += 1
            #             j += 1
            #     print('a_adv condition: i reached last element of a')
            #     return

            # If run a runs out
            if i > len(temp_array) - 1:
                # Copy all of b over, if there are any left
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                print('a_adv condition: a ran out')
                return

            # Copy the element of B after the chunk
            lst[k] = lst[j]
            k += 1
            j += 1

            # If b runs out.
            if j > b[1]:
                while i < len(temp_array):
                    lst[k] = temp_array[i]
                    k += 1
                    i += 1
                print('a_adv condition: b ran out')
                return

            # ----------------------------------------------------------
            # Look for the position of A[i] in B
            b_adv = gallop(lst, temp_array[i], j, b[1] + 1, True)
            print('b_adv', b_adv)
            for y in range(j, b_adv):
                lst[k] = lst[y]
                k += 1

            # Update the counters and check the conditions
            b_count = b_adv - j
            j = b_adv

            # If b ran out
            if j > b[1]:
                while i <= len(temp_array) - 1:
                    lst[k] = temp_array[i]
                    k += 1
                    i += 1
                print('b_adv condition: b ran out')
                return

            lst[k] = temp_array[i]
            i += 1
            k += 1

            if i > len(temp_array) - 1:
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                print('b_adv condition: a ran out')
                return

            if a_count < gallop_thresh and b_count < gallop_thresh:
                print('exit gallop')
                break

        gallop_thresh += 1


def merge_high(lst, a, b, min_gallop):
    """Merges the two runs quasi in-place if b is the smaller array
    a and b are lists that store data of runs"""
    temp_array = make_temp_array(lst, b[0], b[1])
    # Counter for the merge area, starts at the last index of array b
    k = b[1]
    # Counter for the temp array
    i = len(temp_array) - 1  # Lower bound is 0
    # Counter for a, starts at the end this time
    j = a[1]

    gallop_thresh = min_gallop
    while True:
        a_count = 0  # number of times a win in a row
        b_count = 0  # number of times b win in a row

        # Linear merge
        # If a_count or b_count > threshold, switch to gallop
        print('enter normal')
        while i >= 0 and j >= a[0]:
            print('continue normal')
            if temp_array[i] > lst[j]:
                lst[k] = temp_array[i]
                k -= 1
                i -= 1

                a_count = 0
                b_count += 1

                # If b runs out during linear merge
                if i < 0:
                    while j >= a[0]:
                        lst[k] = lst[j]
                        k -= 1
                        j -= 1
                    print('normal merge: b runs out')
                    return

                if b_count >= gallop_thresh:
                    break

            else:
                lst[k] = lst[j]
                k -= 1
                j -= 1

                a_count += 1
                b_count = 0

                # If a runs out during linear merge
                if j < a[0]:
                    while i >= 0:
                        lst[k] = temp_array[i]
                        k -= 1
                        i -= 1
                    print('normal merge: a runs out')
                    return

                if a_count >= gallop_thresh:
                    break

        while True:
            print('Start thresh', gallop_thresh)
            print('enter gallop')
            # Look at the SLICE lst[a[0], j + 1]
            # Look for the position of B[i] in A
            a_adv = gallop(lst, temp_array[i], a[0], j + 1, False)

            # Copy the elements from a_adv -> j to merge area
            # Go backwards to the index a_adv
            for x in range(j, a_adv - 1, -1):
                lst[k] = lst[x]
                k -= 1

            # # Update the a_count to check successfulness of galloping
            a_count = j - a_adv + 1

            # Decrement index j
            j = a_adv - 1

            # If run a runs out:
            if j < a[0]:
                while i >= 0:
                    lst[k] = temp_array[i]
                    k -= 1
                    i -= 1
                print('a_adv cond a runs out')
                return

            # Copy the element of B into the merge area
            lst[k] = temp_array[i]
            k -= 1
            i -= 1

            # If B runs out:
            if i < 0:
                while j >= a[0]:
                    lst[k] = lst[j]
                    k -= 1
                    j -= 1
                print("a_adv condition B runs out")
                return

            # ----------------------------------------------
            # Look for the position of A[j] in B:
            b_adv = gallop(temp_array, lst[j], 0, i + 1, False)
            for y in range(i, b_adv - 1, -1):
                lst[k] = temp_array[y]
                k -= 1

            b_count = i - b_adv + 1
            i = b_adv - 1

            # If B runs out:
            if i < 0:
                while j >= a[0]:
                    lst[k] = lst[j]
                    k -= 1
                    j -= 1
                print("b_adv condition B runs out")
                return

            # Copy the A[j] back to the merge area
            lst[k] = lst[j]
            k -= 1
            j -= 1

            # If A runs out:
            if j < a[0]:
                while i >= 0:
                    lst[k] = temp_array[i]
                    k -= 1
                    i -= 1
                print('b_adv cond a runs out')
                return

            if a_count < gallop_thresh and b_count < gallop_thresh:
                print('exit gallop')
                break
        gallop_thresh += 1



stack = [[0, 511, True, 512], [512, 767, True, 256], [768, 895, True, 128], [896, 959, True, 64], [960, 999, True, 40]]
lst_partial = [4, 5, 5, 6, 6, 9, 11, 13, 14, 14, 17, 17, 21, 22, 24, 26, 27, 27, 32, 33, 34, 36, 44, 45, 50, 53, 57, 57, 58, 59, 59, 59, 59, 60, 62, 63, 64, 64, 65, 68, 69, 69, 69, 70, 79, 81, 82, 86, 87, 88, 93, 93, 93, 99, 100, 100, 104, 104, 105, 105, 106, 106, 108, 112, 115, 121, 122, 125, 126, 127, 129, 131, 132, 132, 135, 136, 140, 143, 147, 148, 149, 150, 150, 151, 151, 153, 154, 155, 159, 161, 161, 161, 164, 165, 166, 166, 166, 168, 172, 173, 174, 176, 177, 179, 182, 183, 185, 187, 189, 189, 192, 194, 195, 196, 197, 199, 200, 200, 205, 206, 206, 212, 212, 213, 220, 222, 225, 228, 229, 231, 233, 234, 235, 240, 240, 241, 241, 242, 244, 246, 247, 248, 249, 255, 255, 260, 265, 267, 269, 271, 274, 275, 277, 281, 283, 284, 289, 290, 291, 292, 293, 294, 294, 300, 301, 302, 302, 302, 304, 304, 305, 313, 315, 316, 320, 320, 324, 325, 328, 329, 329, 332, 334, 336, 337, 338, 342, 345, 346, 350, 352, 353, 353, 354, 355, 361, 363, 363, 365, 366, 370, 372, 372, 377, 377, 377, 380, 381, 382, 383, 385, 385, 387, 387, 389, 390, 390, 394, 394, 396, 399, 399, 400, 401, 408, 409, 409, 412, 413, 421, 424, 432, 432, 437, 437, 442, 442, 443, 443, 444, 444, 445, 447, 449, 451, 457, 457, 457, 459, 459, 460, 461, 463, 464, 468, 469, 471, 472, 474, 481, 481, 483, 485, 486, 488, 490, 490, 490, 493, 496, 496, 497, 502, 506, 506, 509, 512, 514, 515, 518, 520, 521, 522, 523, 528, 529, 531, 537, 538, 540, 540, 545, 546, 549, 551, 555, 562, 565, 565, 568, 568, 574, 575, 577, 581, 582, 585, 586, 588, 588, 589, 591, 593, 594, 599, 599, 600, 601, 610, 611, 612, 616, 618, 619, 622, 623, 625, 627, 628, 628, 629, 630, 630, 636, 641, 642, 642, 648, 648, 650, 652, 652, 656, 659, 661, 662, 662, 663, 663, 664, 666, 667, 668, 668, 670, 671, 672, 675, 676, 677, 679, 686, 687, 687, 688, 688, 690, 694, 695, 697, 697, 698, 699, 700, 702, 704, 708, 709, 709, 710, 713, 713, 718, 719, 720, 721, 722, 724, 726, 728, 730, 732, 734, 736, 737, 741, 742, 743, 743, 746, 746, 756, 760, 761, 765, 768, 773, 779, 781, 782, 784, 785, 786, 791, 792, 794, 797, 798, 800, 801, 803, 804, 804, 805, 806, 807, 815, 816, 816, 826, 828, 829, 833, 835, 836, 837, 838, 838, 846, 848, 854, 855, 861, 866, 867, 867, 870, 873, 875, 875, 875, 876, 879, 881, 882, 883, 885, 886, 886, 887, 889, 891, 892, 894, 896, 900, 902, 902, 903, 911, 913, 913, 915, 916, 916, 916, 917, 922, 923, 930, 931, 932, 940, 944, 945, 946, 947, 951, 955, 957, 958, 959, 959, 960, 967, 967, 969, 970, 971, 981, 982, 985, 987, 988, 988, 989, 989, 989, 992, 993, 996, 1000, 2, 6, 10, 10, 18, 18, 22, 27, 30, 30, 30, 34, 38, 38, 39, 43, 49, 52, 55, 58, 67, 71, 73, 77, 79, 81, 89, 93, 95, 95, 101, 107, 115, 117, 125, 131, 139, 150, 153, 155, 157, 165, 170, 171, 173, 174, 184, 185, 191, 192, 197, 201, 206, 216, 218, 218, 219, 220, 226, 228, 228, 243, 249, 251, 252, 259, 261, 266, 270, 271, 287, 288, 289, 294, 297, 299, 306, 310, 312, 318, 333, 334, 339, 340, 341, 342, 346, 348, 349, 353, 356, 357, 360, 367, 370, 371, 380, 384, 386, 390, 392, 394, 403, 405, 412, 412, 414, 418, 420, 421, 427, 428, 428, 430, 433, 437, 465, 468, 470, 471, 474, 475, 482, 485, 490, 509, 510, 512, 517, 523, 526, 526, 531, 536, 540, 548, 554, 558, 559, 561, 567, 571, 575, 579, 585, 586, 590, 615, 616, 619, 623, 625, 627, 638, 641, 651, 652, 654, 654, 658, 661, 692, 694, 698, 701, 704, 708, 709, 711, 716, 725, 727, 731, 735, 738, 742, 745, 745, 753, 754, 754, 755, 760, 763, 770, 774, 775, 781, 781, 786, 788, 788, 793, 794, 810, 812, 815, 822, 828, 829, 830, 836, 844, 846, 847, 848, 850, 852, 853, 853, 854, 857, 857, 860, 860, 861, 864, 866, 870, 875, 883, 886, 887, 889, 891, 893, 897, 900, 905, 910, 912, 916, 927, 929, 938, 941, 946, 946, 947, 948, 948, 953, 956, 956, 967, 973, 976, 978, 982, 982, 984, 986, 986, 993, 994, 996, 0, 1, 14, 15, 16, 40, 40, 46, 59, 72, 72, 73, 77, 78, 78, 85, 107, 114, 124, 132, 138, 148, 161, 164, 168, 172, 177, 182, 185, 193, 194, 207, 211, 237, 247, 251, 258, 260, 275, 284, 291, 293, 302, 303, 304, 312, 319, 321, 324, 328, 349, 350, 356, 371, 372, 376, 381, 384, 391, 398, 402, 407, 418, 431, 438, 440, 467, 473, 484, 492, 498, 502, 511, 519, 521, 527, 532, 536, 554, 557, 566, 577, 578, 590, 591, 592, 614, 620, 628, 631, 634, 647, 651, 658, 663, 680, 687, 702, 708, 715, 721, 727, 739, 749, 751, 760, 766, 772, 775, 782, 795, 802, 812, 812, 813, 814, 829, 848, 852, 863, 870, 878, 897, 908, 912, 928, 942, 996, 4, 35, 71, 88, 144, 164, 164, 168, 177, 190, 191, 245, 248, 278, 280, 301, 302, 306, 321, 328, 334, 335, 350, 352, 372, 373, 428, 441, 467, 470, 499, 523, 528, 540, 549, 554, 589, 597, 622, 622, 639, 651, 661, 670, 691, 702, 745, 759, 760, 801, 812, 818, 825, 839, 843, 844, 853, 895, 904, 915, 917, 919, 945, 975, 5, 32, 33, 33, 84, 84, 175, 188, 197, 208, 233, 258, 269, 305, 335, 365, 366, 372, 384, 416, 436, 478, 478, 566, 569, 609, 660, 676, 696, 696, 715, 716, 724, 725, 790, 810, 811, 887, 983, 994]

# stuff = lst_partial[0:768]
# stuff.sort()
# merge_high(lst_partial, stack[0], stack[1], 7)
# print(lst_partial[0:768])
# print(stuff)
# print(stuff == lst_partial[0:768])

# stuff = lst_partial[512:896]
# stuff.sort()
# merge_high(lst_partial, stack[1], stack[2], 7)
# print(lst_partial[512:896])
# print(stuff)
# print(stuff == lst_partial[512:896])

stuff = lst_partial[768:960]
stuff.sort()
merge_high(lst_partial, stack[2], stack[3], 7)
print(lst_partial[768:960])
print(stuff)
print(stuff == lst_partial[768:960])
