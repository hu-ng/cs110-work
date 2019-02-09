import random
import bisect


def reverse(lst, s, e):
    """Reverse the order of a list in place
    Input: s = starting index, e = ending index"""
    while s < e and s != e:
        lst[s], lst[e] = lst[e], lst[s]
        s += 1
        e -= 1


def make_temp_array(lst, s, e):
    """From the lst given, make a copy from index s to index e"""
    array = []
    while s <= e:
        array.append(lst[s])
        s += 1
    return array


def merge_compute_minrun(n):
    """Returns the minimum length of a run from 23 - 64 so that
    the len(array)/minrun is less than or equal to a power of 2."""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def count_run(lst, s_run):
    """Count the length of one run, returns starting/ending indices,
    a boolean value to present increasing/decreasing run,
    and the length of the run"""
    increasing = True

    # If count_run started at the final position of the array
    if s_run == len(lst) - 1:
        return [s_run, s_run, increasing, 1]
    else:
        e_run = s_run
        # Decreasing run (strictly decreasing):
        if lst[s_run] > lst[s_run + 1]:
            while lst[e_run] > lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            increasing = False
            return [s_run, e_run, increasing, e_run - s_run + 1]

        # Increasing run (non-decreasing):
        else:
            while lst[e_run] <= lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            return [s_run, e_run, increasing, e_run - s_run + 1]


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


def gallop(lst, val, low, high, ltr):
    if ltr == True:
        pos = bisect.bisect_left(lst, val, low, high)
        return pos

    else:
        pos = bisect.bisect_right(lst, val, low, high)
        return pos


def merge(lst, stack, run_num):
    """Merge the two runs and update the instructions in the stack"""

    # Make references to the to-be-merged runs
    run_a = stack[run_num]
    run_b = stack[run_num + 1]

    # Add a reference to where the new combined run would be.
    new_run = [run_a[0], run_b[1], True, run_b[1] - run_a[0] + 1]

    # Add this to the stack
    stack[run_num] = new_run

    # Delete the run from the stack
    del stack[run_num + 1]

    # If the length of run_a is smaller than length of run_b
    if run_a[3] <= run_b[3]:
        merge_low(lst, run_a, run_b, 7)
    else:
        merge_high(lst, run_a, run_b, 7)


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
                    print('normal merge a runs out')
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
                    print('normal merge b runs out')
                    return

                if b_count >= gallop_thresh:
                    break

        # If one run is winning consistently, switch to galloping mode.
        # i, j, and k is incremented accordingly
        while True:
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

            # If run a runs out
            if i > len(temp_array) - 1:
                # Copy all of b over, if there are any left
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                print('normal merge a runs out')
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
                print('normal merge b runs out')
                return

            # ----------------------------------------------------------
            # Look for the position of A[i] in B
            b_adv = gallop(lst, temp_array[i], j, b[1] + 1, True)
            for y in range(j, b_adv):
                lst[k] = lst[y]
                k += 1

            # Update the counters and check the conditions
            b_count = b_adv - j
            j = b_adv

            # If B runs out
            if j > b[1]:
                while i <= len(temp_array) - 1:
                    lst[k] = temp_array[i]
                    k += 1
                    i += 1
                return

            lst[k] = temp_array[i]
            i += 1
            k += 1

            # If A runs out
            if i > len(temp_array) - 1:
                while j <= b[1]:
                    lst[k] = lst[j]
                    k += 1
                    j += 1
                return

            if a_count < gallop_thresh and b_count < gallop_thresh:
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
        while i >= 0 and j >= a[0]:
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
                break
        gallop_thresh += 1


def merge_collapse(lst, stack):
    # Maintains invariants for length of runs: A > B + C, B > C
    # Translated to stack positions:
    #   stack[-3] > stack[-2] + stack[-1]
    #   stack[-2] > stack[-1]
    # Takes a stack that holds many lists of type [s, e, bool, length]
    # Merges the elements until the invariants hold
    while len(stack) > 1:
        if len(stack) >= 3 and stack[-3][3] <= stack[-2][3] + stack[-1][3]:
            if stack[-3][3] < stack[-1][3]:
                # merge -3 and -2, merge at -3
                merge(lst, stack, -3)
            else:
                # merge -2 and -1, merge at -2
                merge(lst, stack, -2)
        elif stack[-2][3] <= stack[-1][3]:
            # merge -2 and -1, merge at -2
            merge(lst, stack, -2)
        else:
            break


def merge_force_collapse(lst, stack):
    """When the invariant holds, this function finishes the merging"""
    while len(stack) > 1:
        merge(lst, stack, -2)


def timsort(lst):
    s = 0
    e = len(lst) - 1
    stack = []
    min_run = merge_compute_minrun(len(lst))
    while s <= e:

        # Reference to a list [s, e, bool]
        run = count_run(lst, s)

        # If decreasing, reverse
        if run[2] == False:
            reverse(lst, run[0], run[1])
            # Change bool to True
            run[2] = True
        if run[3] < min_run:  # If length of the run is less than min_run
            # The number of indices by which we want to extend the run
            extend = min(min_run - run[3] + 1, e - run[1])
            # Extend the run
            bin_sort(lst, run[0], run[1], extend)
            # Update last index
            run[1] = run[1] + extend
            # Update the run length
            run[3] = run[3] + extend
        # Push the run into the stack
        stack.append(run)
        merge_collapse(lst, stack)
        s = run[1] + 1
    merge_force_collapse(lst, stack)
    return lst


# lst1 = [34, 342, 121, 982, 187, 472, 292, 401, 122, 105, 1000, 165, 265, 886, 663, 155, 14, 833, 409, 591, 87, 387, 588, 281, 988, 699, 302, 704, 390, 911, 957, 959, 345, 5, 881, 985, 641, 200, 585, 444, 100, 289, 291, 302, 555, 490, 444, 290, 549, 989, 741, 267, 153, 896, 599, 129, 931, 746, 390, 234, 838, 538, 173, 86, 197, 879, 662, 199, 521, 179, 151, 59, 206, 471, 468, 873, 486, 189, 546, 443, 316, 271, 967, 816, 328, 996, 506, 734, 589, 989, 320, 687, 136, 784, 721, 668, 568, 575, 459, 686, 14, 797, 125, 565, 399, 870, 387, 346, 385, 380, 365, 196, 697, 44, 166, 174, 60, 625, 294, 45, 366, 490, 488, 913, 27, 70, 622, 568, 225, 694, 385, 601, 700, 27, 229, 497, 709, 161, 313, 244, 794, 652, 400, 17, 127, 902, 582, 168, 981, 713, 161, 661, 719, 903, 13, 875, 151, 746, 594, 443, 283, 768, 630, 710, 81, 728, 150, 409, 987, 36, 377, 192, 205, 461, 185, 457, 512, 337, 545, 894, 915, 781, 722, 969, 447, 150, 574, 611, 315, 761, 24, 514, 396, 760, 730, 743, 143, 363, 656, 677, 671, 562, 413, 4, 509, 540, 773, 883, 970, 464, 629, 867, 593, 496, 21, 652, 806, 451, 247, 743, 82, 540, 106, 695, 531, 50, 960, 115, 58, 636, 600, 867, 324, 835, 33, 65, 301, 182, 213, 506, 437, 240, 161, 105, 648, 148, 861, 648, 126, 57, 518, 891, 329, 529, 68, 846, 785, 886, 463, 737, 382, 944, 520, 528, 69, 106, 132, 424, 355, 804, 848, 940, 277, 490, 955, 854, 702, 803, 206, 246, 917, 807, 177, 231, 828, 370, 460, 459, 240, 782, 69, 104, 672, 515, 394, 300, 147, 432, 336, 913, 200, 679, 377, 688, 304, 176, 449, 801, 642, 805, 628, 79, 577, 88, 59, 667, 260, 412, 708, 989, 363, 255, 485, 988, 826, 650, 670, 923, 437, 690, 892, 93, 537, 581, 882, 338, 432, 457, 294, 946, 304, 353, 800, 522, 688, 149, 481, 992, 945, 22, 11, 64, 389, 195, 612, 804, 194, 876, 887, 220, 383, 140, 483, 916, 668, 718, 623, 445, 610, 742, 565, 64, 159, 713, 889, 100, 131, 6, 164, 99, 947, 354, 248, 421, 916, 756, 372, 372, 932, 900, 394, 916, 255, 442, 284, 642, 664, 242, 736, 235, 361, 662, 132, 798, 189, 616, 377, 222, 53, 228, 666, 967, 493, 32, 902, 325, 837, 619, 720, 166, 183, 269, 815, 481, 212, 958, 408, 474, 838, 329, 663, 320, 59, 274, 599, 627, 618, 241, 959, 628, 9, 875, 112, 855, 442, 353, 951, 732, 104, 724, 496, 350, 816, 971, 249, 26, 59, 469, 586, 792, 5, 457, 154, 241, 659, 62, 63, 332, 399, 866, 675, 551, 69, 676, 630, 765, 779, 302, 709, 352, 305, 93, 57, 687, 885, 334, 502, 6, 875, 233, 93, 172, 275, 212, 836, 698, 993, 135, 588, 726, 17, 697, 293, 930, 108, 786, 381, 523, 922, 166, 829, 791, 370, 171, 852, 71, 694, 490, 829, 43, 947, 860, 334, 929, 294, 976, 390, 252, 95, 18, 927, 638, 412, 558, 727, 306, 536, 470, 853, 394, 967, 571, 956, 131, 173, 517, 627, 79, 793, 745, 854, 523, 847, 125, 864, 115, 10, 38, 139, 384, 526, 692, 405, 984, 567, 815, 474, 249, 67, 55, 27, 625, 52, 201, 30, 973, 725, 333, 742, 428, 623, 860, 875, 107, 418, 289, 430, 886, 218, 836, 770, 312, 711, 794, 218, 788, 848, 857, 259, 465, 348, 414, 788, 893, 781, 850, 18, 828, 150, 755, 117, 428, 948, 38, 654, 810, 10, 2, 403, 946, 704, 251, 206, 652, 153, 170, 471, 512, 946, 941, 228, 986, 93, 916, 243, 81, 299, 731, 786, 857, 866, 468, 353, 585, 812, 39, 185, 421, 641, 900, 342, 579, 437, 754, 651, 318, 73, 905, 953, 392, 101, 716, 586, 948, 701, 509, 615, 781, 822, 197, 360, 575, 883, 30, 174, 433, 774, 887, 226, 340, 191, 897, 371, 982, 58, 228, 994, 846, 526, 346, 420, 287, 938, 708, 219, 380, 554, 844, 261, 155, 49, 6, 709, 661, 738, 349, 861, 559, 616, 910, 982, 735, 192, 367, 510, 763, 482, 89, 889, 978, 95, 34, 220, 357, 891, 956, 427, 561, 356, 412, 266, 775, 745, 30, 619, 271, 341, 184, 996, 77, 870, 912, 753, 853, 986, 540, 339, 386, 297, 548, 485, 658, 165, 157, 654, 754, 760, 310, 216, 475, 830, 993, 531, 590, 22, 270, 288, 698, 211, 293, 1, 46, 77, 172, 284, 663, 592, 467, 772, 511, 72, 852, 0, 321, 73, 554, 749, 647, 802, 942, 870, 536, 107, 384, 591, 275, 398, 498, 260, 928, 304, 193, 996, 631, 350, 863, 813, 634, 372, 708, 247, 760, 40, 258, 590, 829, 687, 124, 376, 527, 312, 766, 521, 557, 114, 897, 502, 14, 251, 85, 185, 194, 168, 349, 628, 814, 303, 402, 407, 578, 302, 620, 324, 132, 878, 848, 795, 812, 138, 78, 319, 40, 237, 651, 438, 16, 182, 721, 328, 164, 177, 161, 371, 577, 72, 391, 519, 658, 614, 356, 15, 702, 148, 782, 751, 727, 78, 381, 812, 291, 207, 912, 431, 566, 484, 59, 418, 532, 908, 492, 715, 473, 680, 775, 440, 739, 919, 164, 904, 651, 760, 470, 801, 168, 745, 895, 639, 540, 71, 164, 839, 373, 302, 759, 190, 248, 853, 554, 177, 306, 825, 691, 467, 301, 278, 321, 589, 335, 917, 350, 670, 372, 622, 191, 843, 144, 352, 35, 328, 975, 622, 661, 597, 818, 702, 280, 88, 945, 915, 549, 428, 523, 499, 245, 812, 334, 441, 4, 844, 528, 790, 676, 566, 269, 660, 233, 84, 478, 436, 384, 32, 715, 983, 696, 365, 609, 5, 887, 569, 258, 725, 716, 696, 305, 84, 335, 197, 478, 175, 724, 208, 33, 810, 33, 372, 366, 994, 811, 188, 416]
# lst2 = [0, 1, 2, 4, 4, 5, 5, 5, 6, 6, 6, 9, 10, 10, 11, 13, 14, 14, 14, 15, 16, 17, 17, 18, 18, 21, 22, 22, 24, 26, 27, 27, 27, 30, 30, 30, 32, 32, 33, 33, 33, 34, 34, 35, 36, 38, 38, 39, 40, 40, 43, 44, 45, 46, 49, 50, 52, 53, 55, 57, 57, 58, 58, 59, 59, 59, 59, 59, 60, 62, 63, 64, 64, 65, 67, 68, 69, 69, 69, 70, 71, 71, 72, 72, 73, 73, 77, 77, 78, 78, 79, 79, 81, 81, 82, 84, 84, 85, 86, 87, 88, 88, 89, 93, 93, 93, 93, 95, 95, 99, 100, 100, 101, 104, 104, 105, 105, 106, 106, 107, 107, 108, 112, 114, 115, 115, 117, 121, 122, 124, 125, 125, 126, 127, 129, 131, 131, 132, 132, 132, 135, 136, 138, 139, 140, 143, 144, 147, 148, 148, 149, 150, 150, 150, 151, 151, 153, 153, 154, 155, 155, 157, 159, 161, 161, 161, 161, 164, 164, 164, 164, 165, 165, 166, 166, 166, 168, 168, 168, 170, 171, 172, 172, 173, 173, 174, 174, 175, 176, 177, 177, 177, 179, 182, 182, 183, 184, 185, 185, 185, 187, 188, 189, 189, 190, 191, 191, 192, 192, 193, 194, 194, 195, 196, 197, 197, 197, 199, 200, 200, 201, 205, 206, 206, 206, 207, 208, 211, 212, 212, 213, 216, 218, 218, 219, 220, 220, 222, 225, 226, 228, 228, 228, 229, 231, 233, 233, 234, 235, 237, 240, 240, 241, 241, 242, 243, 244, 245, 246, 247, 247, 248, 248, 249, 249, 251, 251, 252, 255, 255, 258, 258, 259, 260, 260, 261, 265, 266, 267, 269, 269, 270, 271, 271, 274, 275, 275, 277, 278, 280, 281, 283, 284, 284, 287, 288, 289, 289, 290, 291, 291, 292, 293, 293, 294, 294, 294, 297, 299, 300, 301, 301, 302, 302, 302, 302, 302, 303, 304, 304, 304, 305, 305, 306, 306, 310, 312, 312, 313, 315, 316, 318, 319, 320, 320, 321, 321, 324, 324, 325, 328, 328, 328, 329, 329, 332, 333, 334, 334, 334, 335, 335, 336, 337, 338, 339, 340, 341, 342, 342, 345, 346, 346, 348, 349, 349, 350, 350, 350, 352, 352, 353, 353, 353, 354, 355, 356, 356, 357, 360, 361, 363, 363, 365, 365, 366, 366, 367, 370, 370, 371, 371, 372, 372, 372, 372, 372, 373, 376, 377, 377, 377, 380, 380, 381, 381, 382, 383, 384, 384, 384, 385, 385, 386, 387, 387, 389, 390, 390, 390, 391, 392, 394, 394, 394, 396, 398, 399, 399, 400, 401, 402, 403, 405, 407, 408, 409, 409, 412, 412, 412, 413, 414, 416, 418, 418, 420, 421, 421, 424, 427, 428, 428, 428, 430, 431, 432, 432, 433, 436, 437, 437, 437, 438, 440, 441, 442, 442, 443, 443, 444, 444, 445, 447, 449, 451, 457, 457, 457, 459, 459, 460, 461, 463, 464, 465, 467, 467, 468, 468, 469, 470, 470, 471, 471, 472, 473, 474, 474, 475, 478, 478, 481, 481, 482, 483, 484, 485, 485, 486, 488, 490, 490, 490, 490, 492, 493, 496, 496, 497, 498, 499, 502, 502, 506, 506, 509, 509, 510, 511, 512, 512, 514, 515, 517, 518, 519, 520, 521, 521, 522, 523, 523, 523, 526, 526, 527, 528, 528, 529, 531, 531, 532, 536, 536, 537, 538, 540, 540, 540, 540, 545, 546, 548, 549, 549, 551, 554, 554, 554, 555, 557, 558, 559, 561, 562, 565, 565, 566, 566, 567, 568, 568, 569, 571, 574, 575, 575, 577, 577, 578, 579, 581, 582, 585, 585, 586, 586, 588, 588, 589, 589, 590, 590, 591, 591, 592, 593, 594, 597, 599, 599, 600, 601, 609, 610, 611, 612, 614, 615, 616, 616, 618, 619, 619, 620, 622, 622, 622, 623, 623, 625, 625, 627, 627, 628, 628, 628, 629, 630, 630, 631, 634, 636, 638, 639, 641, 641, 642, 642, 647, 648, 648, 650, 651, 651, 651, 652, 652, 652, 654, 654, 656, 658, 658, 659, 660, 661, 661, 661, 662, 662, 663, 663, 663, 664, 666, 667, 668, 668, 670, 670, 671, 672, 675, 676, 676, 677, 679, 680, 686, 687, 687, 687, 688, 688, 690, 691, 692, 694, 694, 695, 696, 696, 697, 697, 698, 698, 699, 700, 701, 702, 702, 702, 704, 704, 708, 708, 708, 709, 709, 709, 710, 711, 713, 713, 715, 715, 716, 716, 718, 719, 720, 721, 721, 722, 724, 724, 725, 725, 726, 727, 727, 728, 730, 731, 732, 734, 735, 736, 737, 738, 739, 741, 742, 742, 743, 743, 745, 745, 745, 746, 746, 749, 751, 753, 754, 754, 755, 756, 759, 760, 760, 760, 760, 761, 763, 765, 766, 768, 770, 772, 773, 774, 775, 775, 779, 781, 781, 781, 782, 782, 784, 785, 786, 786, 788, 788, 790, 791, 792, 793, 794, 794, 795, 797, 798, 800, 801, 801, 802, 803, 804, 804, 805, 806, 807, 810, 810, 811, 812, 812, 812, 812, 813, 814, 815, 815, 816, 816, 818, 822, 825, 826, 828, 828, 829, 829, 829, 830, 833, 835, 836, 836, 837, 838, 838, 839, 843, 844, 844, 846, 846, 847, 848, 848, 848, 850, 852, 852, 853, 853, 853, 854, 854, 855, 857, 857, 860, 860, 861, 861, 863, 864, 866, 866, 867, 867, 870, 870, 870, 873, 875, 875, 875, 875, 876, 878, 879, 881, 882, 883, 883, 885, 886, 886, 886, 887, 887, 887, 889, 889, 891, 891, 892, 893, 894, 895, 896, 897, 897, 900, 900, 902, 902, 903, 904, 905, 908, 910, 911, 912, 912, 913, 913, 915, 915, 916, 916, 916, 916, 917, 917, 919, 922, 923, 927, 928, 929, 930, 931, 932, 938, 940, 941, 942, 944, 945, 945, 946, 946, 946, 947, 947, 948, 948, 951, 953, 955, 956, 956, 957, 958, 959, 959, 960, 967, 967, 967, 969, 970, 971, 973, 975, 976, 978, 981, 982, 982, 982, 983, 984, 985, 986, 986, 987, 988, 988, 989, 989, 989, 992, 993, 993, 994, 994, 996, 996, 996, 1000]
# lst1.sort()
# print(lst1 == lst2)

lst1 = []
lst2 = [1]
lst3 = [i for i in range(10000)]
lst4 = [i for i in range(10000, -1, -1)]
lst5 = [random.randint(-100000, 100000) for i in range(10000)]
lst6 = [-1,2,-3,4,5]*10000
lst7 = [(i + 0.2) for i in range(100000)]
lst8 = [i for i in range(10000, 2)]
lst9 = [1, 2]
lst10 = [0 for i in range(10000)]
lst11 = [random.random() for i in range(10000)]
lst12 = [10,9,8,7,6,5,4,3,2,1,0,-1,-1]
lst13 = [i for i in range(9999, -1, -2)]

test_cases = [lst1, lst2, lst3, lst4, lst5, lst6, lst7, lst8, lst9, lst10, lst11, lst12, lst13]


def test_sort():
    for lst in test_cases:
        random.shuffle(lst)
        sortable = lst

        sortable_copy = lst
        sorted_copy = timsort(sortable_copy)

        assert sorted_copy is sortable_copy
        assert sorted_copy == sorted(sortable)


def test_sort2(lst):
    copy = lst
    timsort(lst)
    # Compare each element to the next element
    for i in range(len(lst) - 1):
        assert lst[i] <= lst[i + 1]
        i += 1

    # Assure that the lengths are the same
    assert len(copy) == len(lst)

    copy.sort()

    # Every element in copy is in lst
    for i in range(len(lst)):
        assert copy[i] in lst

    # Result of the sorting algorithm is the same as the default sort
    assert lst is copy

test_sort()
for case in test_cases:
    test_sort2(case)