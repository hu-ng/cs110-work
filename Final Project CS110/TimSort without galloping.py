import random
import numpy
min_gallop = 7

def reverse(lst, s, e):
    """Reverse the order of a list in place
    Input: s = starting index, e = ending index"""
    while s < e and s != e:
        lst[s], lst[e] = lst[e], lst[s]
        s += 1
        e -= 1


def make_temp_array(lst, s, e):
    array = []
    while s <= e:
        array.append(lst[s])
        s += 1
    return array


def merge_compute_minrun(n):
    """Returns the minimum length of a run"""
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r


def count_run(lst, s_run):
    """Count the length of one run, returns starting/ending index
    and a boolean to present increasing/decreasing run
    Input: s_run = Starting index of a run"""
    increasing = True

    # If count_run started at the final position of the array
    if s_run == len(lst) - 1:
        return [s_run, s_run, increasing, 1]
    else:
        e_run = s_run
        # Decreasing run:
        if lst[s_run] > lst[s_run + 1]:
            while lst[e_run] > lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            increasing = False
            return [s_run, e_run, increasing, e_run - s_run + 1]

        # Increasing run:
        else:
            while lst[e_run] <= lst[e_run + 1]:
                e_run += 1
                if e_run == len(lst) - 1:
                    break
            return [s_run, e_run, increasing, e_run - s_run + 1]
        # start, end, bool, length


def bin_sort(lst, s, e, extend):  # might fix into value > last element, continue.
    """Binary insertion sort, assumed that lst[s:e] is sorted.
    Extend the run by the number indicated by 'extend'"""

    # +1 because we are moving three indices to the right
    for i in range(1, extend + 1):
        pos = 0
        start = s
        end = e + i
        value = lst[end]
        while start <= end:
            if start == end:
                if lst[start] > value:
                    pos = start
                else:
                    pos = start + 1
            mid = (start + end) // 2
            if value >= lst[mid]:
                start = mid + 1
            else:
                end = mid - 1

        if start > end:
            pos = start

        if pos > e + i:
            pos -= 1

        for x in range(e + i, pos, - 1):
            lst[x] = lst[x - 1]
        lst[pos] = value


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
        merge_low(lst, run_a, run_b)
    else:
        merge_high(lst, run_a, run_b)


def merge_low(lst, a, b):
    """Merges the two runs quasi in-place if a is the smaller array
    a and b are lists that store data of runs"""
    temp_array = make_temp_array(lst, a[0], a[1])
    k = a[0]
    i = 0

    # Counter for b, starts at the top
    j = b[0]
    while i <= len(temp_array) - 1 and j <= b[1]:
        if temp_array[i] <= lst[j]:
            lst[k] = temp_array[i]
            k += 1
            i += 1
        else:
            lst[k] = lst[j]
            k += 1
            j += 1
    while i <= len(temp_array) - 1:
        lst[k] = temp_array[i]
        k += 1
        i += 1
    while j <= b[1]:
        lst[k] = lst[j]
        k += 1
        j += 1


def merge_high(lst, a, b):
    """Merges the two runs quasi in-place if b is the smaller array
    a and b are lists that store data of runs"""
    temp_array = make_temp_array(lst, b[0], b[1])
    k = b[1]

    # Counter for the temp array
    i = -1

    # Counter for a, starts at the end this time
    j = a[1]
    while i >= -len(temp_array) and j >= a[0]:
        if temp_array[i] > lst[j]:
            lst[k] = temp_array[i]
            k -= 1
            i -= 1
        else:
            lst[k] = lst[j]
            k -= 1
            j -= 1
    while i >= -len(temp_array):
        lst[k] = temp_array[i]
        k -= 1
        i -= 1
    while j >= a[0]:
        lst[k] = lst[j]
        k -= 1
        j -= 1


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
    return stack


# lst = [34, 342, 121, 982, 187, 472, 292, 401, 122, 105, 1000, 165, 265, 886, 663, 155, 14, 833, 409, 591, 87, 387, 588, 281, 988, 699, 302, 704, 390, 911, 957, 959, 345, 5, 881, 985, 641, 200, 585, 444, 100, 289, 291, 302, 555, 490, 444, 290, 549, 989, 741, 267, 153, 896, 599, 129, 931, 746, 390, 234, 838, 538, 173, 86, 197, 879, 662, 199, 521, 179, 151, 59, 206, 471, 468, 873, 486, 189, 546, 443, 316, 271, 967, 816, 328, 996, 506, 734, 589, 989, 320, 687, 136, 784, 721, 668, 568, 575, 459, 686, 14, 797, 125, 565, 399, 870, 387, 346, 385, 380, 365, 196, 697, 44, 166, 174, 60, 625, 294, 45, 366, 490, 488, 913, 27, 70, 622, 568, 225, 694, 385, 601, 700, 27, 229, 497, 709, 161, 313, 244, 794, 652, 400, 17, 127, 902, 582, 168, 981, 713, 161, 661, 719, 903, 13, 875, 151, 746, 594, 443, 283, 768, 630, 710, 81, 728, 150, 409, 987, 36, 377, 192, 205, 461, 185, 457, 512, 337, 545, 894, 915, 781, 722, 969, 447, 150, 574, 611, 315, 761, 24, 514, 396, 760, 730, 743, 143, 363, 656, 677, 671, 562, 413, 4, 509, 540, 773, 883, 970, 464, 629, 867, 593, 496, 21, 652, 806, 451, 247, 743, 82, 540, 106, 695, 531, 50, 960, 115, 58, 636, 600, 867, 324, 835, 33, 65, 301, 182, 213, 506, 437, 240, 161, 105, 648, 148, 861, 648, 126, 57, 518, 891, 329, 529, 68, 846, 785, 886, 463, 737, 382, 944, 520, 528, 69, 106, 132, 424, 355, 804, 848, 940, 277, 490, 955, 854, 702, 803, 206, 246, 917, 807, 177, 231, 828, 370, 460, 459, 240, 782, 69, 104, 672, 515, 394, 300, 147, 432, 336, 913, 200, 679, 377, 688, 304, 176, 449, 801, 642, 805, 628, 79, 577, 88, 59, 667, 260, 412, 708, 989, 363, 255, 485, 988, 826, 650, 670, 923, 437, 690, 892, 93, 537, 581, 882, 338, 432, 457, 294, 946, 304, 353, 800, 522, 688, 149, 481, 992, 945, 22, 11, 64, 389, 195, 612, 804, 194, 876, 887, 220, 383, 140, 483, 916, 668, 718, 623, 445, 610, 742, 565, 64, 159, 713, 889, 100, 131, 6, 164, 99, 947, 354, 248, 421, 916, 756, 372, 372, 932, 900, 394, 916, 255, 442, 284, 642, 664, 242, 736, 235, 361, 662, 132, 798, 189, 616, 377, 222, 53, 228, 666, 967, 493, 32, 902, 325, 837, 619, 720, 166, 183, 269, 815, 481, 212, 958, 408, 474, 838, 329, 663, 320, 59, 274, 599, 627, 618, 241, 959, 628, 9, 875, 112, 855, 442, 353, 951, 732, 104, 724, 496, 350, 816, 971, 249, 26, 59, 469, 586, 792, 5, 457, 154, 241, 659, 62, 63, 332, 399, 866, 675, 551, 69, 676, 630, 765, 779, 302, 709, 352, 305, 93, 57, 687, 885, 334, 502, 6, 875, 233, 93, 172, 275, 212, 836, 698, 993, 135, 588, 726, 17, 697, 293, 930, 108, 786, 381, 523, 922, 166, 829, 791, 370, 171, 852, 71, 694, 490, 829, 43, 947, 860, 334, 929, 294, 976, 390, 252, 95, 18, 927, 638, 412, 558, 727, 306, 536, 470, 853, 394, 967, 571, 956, 131, 173, 517, 627, 79, 793, 745, 854, 523, 847, 125, 864, 115, 10, 38, 139, 384, 526, 692, 405, 984, 567, 815, 474, 249, 67, 55, 27, 625, 52, 201, 30, 973, 725, 333, 742, 428, 623, 860, 875, 107, 418, 289, 430, 886, 218, 836, 770, 312, 711, 794, 218, 788, 848, 857, 259, 465, 348, 414, 788, 893, 781, 850, 18, 828, 150, 755, 117, 428, 948, 38, 654, 810, 10, 2, 403, 946, 704, 251, 206, 652, 153, 170, 471, 512, 946, 941, 228, 986, 93, 916, 243, 81, 299, 731, 786, 857, 866, 468, 353, 585, 812, 39, 185, 421, 641, 900, 342, 579, 437, 754, 651, 318, 73, 905, 953, 392, 101, 716, 586, 948, 701, 509, 615, 781, 822, 197, 360, 575, 883, 30, 174, 433, 774, 887, 226, 340, 191, 897, 371, 982, 58, 228, 994, 846, 526, 346, 420, 287, 938, 708, 219, 380, 554, 844, 261, 155, 49, 6, 709, 661, 738, 349, 861, 559, 616, 910, 982, 735, 192, 367, 510, 763, 482, 89, 889, 978, 95, 34, 220, 357, 891, 956, 427, 561, 356, 412, 266, 775, 745, 30, 619, 271, 341, 184, 996, 77, 870, 912, 753, 853, 986, 540, 339, 386, 297, 548, 485, 658, 165, 157, 654, 754, 760, 310, 216, 475, 830, 993, 531, 590, 22, 270, 288, 698, 211, 293, 1, 46, 77, 172, 284, 663, 592, 467, 772, 511, 72, 852, 0, 321, 73, 554, 749, 647, 802, 942, 870, 536, 107, 384, 591, 275, 398, 498, 260, 928, 304, 193, 996, 631, 350, 863, 813, 634, 372, 708, 247, 760, 40, 258, 590, 829, 687, 124, 376, 527, 312, 766, 521, 557, 114, 897, 502, 14, 251, 85, 185, 194, 168, 349, 628, 814, 303, 402, 407, 578, 302, 620, 324, 132, 878, 848, 795, 812, 138, 78, 319, 40, 237, 651, 438, 16, 182, 721, 328, 164, 177, 161, 371, 577, 72, 391, 519, 658, 614, 356, 15, 702, 148, 782, 751, 727, 78, 381, 812, 291, 207, 912, 431, 566, 484, 59, 418, 532, 908, 492, 715, 473, 680, 775, 440, 739, 919, 164, 904, 651, 760, 470, 801, 168, 745, 895, 639, 540, 71, 164, 839, 373, 302, 759, 190, 248, 853, 554, 177, 306, 825, 691, 467, 301, 278, 321, 589, 335, 917, 350, 670, 372, 622, 191, 843, 144, 352, 35, 328, 975, 622, 661, 597, 818, 702, 280, 88, 945, 915, 549, 428, 523, 499, 245, 812, 334, 441, 4, 844, 528, 790, 676, 566, 269, 660, 233, 84, 478, 436, 384, 32, 715, 983, 696, 365, 609, 5, 887, 569, 258, 725, 716, 696, 305, 84, 335, 197, 478, 175, 724, 208, 33, 810, 33, 372, 366, 994, 811, 188, 416]
# lst2 = [34, 342, 121, 982, 187, 472, 292, 401, 122, 105, 1000, 165, 265, 886, 663, 155, 14, 833, 409, 591, 87, 387, 588, 281, 988, 699, 302, 704, 390, 911, 957, 959, 345, 5, 881, 985, 641, 200, 585, 444, 100, 289, 291, 302, 555, 490, 444, 290, 549, 989, 741, 267, 153, 896, 599, 129, 931, 746, 390, 234, 838, 538, 173, 86, 197, 879, 662, 199, 521, 179, 151, 59, 206, 471, 468, 873, 486, 189, 546, 443, 316, 271, 967, 816, 328, 996, 506, 734, 589, 989, 320, 687, 136, 784, 721, 668, 568, 575, 459, 686, 14, 797, 125, 565, 399, 870, 387, 346, 385, 380, 365, 196, 697, 44, 166, 174, 60, 625, 294, 45, 366, 490, 488, 913, 27, 70, 622, 568, 225, 694, 385, 601, 700, 27, 229, 497, 709, 161, 313, 244, 794, 652, 400, 17, 127, 902, 582, 168, 981, 713, 161, 661, 719, 903, 13, 875, 151, 746, 594, 443, 283, 768, 630, 710, 81, 728, 150, 409, 987, 36, 377, 192, 205, 461, 185, 457, 512, 337, 545, 894, 915, 781, 722, 969, 447, 150, 574, 611, 315, 761, 24, 514, 396, 760, 730, 743, 143, 363, 656, 677, 671, 562, 413, 4, 509, 540, 773, 883, 970, 464, 629, 867, 593, 496, 21, 652, 806, 451, 247, 743, 82, 540, 106, 695, 531, 50, 960, 115, 58, 636, 600, 867, 324, 835, 33, 65, 301, 182, 213, 506, 437, 240, 161, 105, 648, 148, 861, 648, 126, 57, 518, 891, 329, 529, 68, 846, 785, 886, 463, 737, 382, 944, 520, 528, 69, 106, 132, 424, 355, 804, 848, 940, 277, 490, 955, 854, 702, 803, 206, 246, 917, 807, 177, 231, 828, 370, 460, 459, 240, 782, 69, 104, 672, 515, 394, 300, 147, 432, 336, 913, 200, 679, 377, 688, 304, 176, 449, 801, 642, 805, 628, 79, 577, 88, 59, 667, 260, 412, 708, 989, 363, 255, 485, 988, 826, 650, 670, 923, 437, 690, 892, 93, 537, 581, 882, 338, 432, 457, 294, 946, 304, 353, 800, 522, 688, 149, 481, 992, 945, 22, 11, 64, 389, 195, 612, 804, 194, 876, 887, 220, 383, 140, 483, 916, 668, 718, 623, 445, 610, 742, 565, 64, 159, 713, 889, 100, 131, 6, 164, 99, 947, 354, 248, 421, 916, 756, 372, 372, 932, 900, 394, 916, 255, 442, 284, 642, 664, 242, 736, 235, 361, 662, 132, 798, 189, 616, 377, 222, 53, 228, 666, 967, 493, 32, 902, 325, 837, 619, 720, 166, 183, 269, 815, 481, 212, 958, 408, 474, 838, 329, 663, 320, 59, 274, 599, 627, 618, 241, 959, 628, 9, 875, 112, 855, 442, 353, 951, 732, 104, 724, 496, 350, 816, 971, 249, 26, 59, 469, 586, 792, 5, 457, 154, 241, 659, 62, 63, 332, 399, 866, 675, 551, 69, 676, 630, 765, 779, 302, 709, 352, 305, 93, 57, 687, 885, 334, 502, 6, 875, 233, 93, 172, 275, 212, 836, 698, 993, 135, 588, 726, 17, 697, 293, 930, 108, 786, 381, 523, 922, 166, 829, 791, 370, 171, 852, 71, 694, 490, 829, 43, 947, 860, 334, 929, 294, 976, 390, 252, 95, 18, 927, 638, 412, 558, 727, 306, 536, 470, 853, 394, 967, 571, 956, 131, 173, 517, 627, 79, 793, 745, 854, 523, 847, 125, 864, 115, 10, 38, 139, 384, 526, 692, 405, 984, 567, 815, 474, 249, 67, 55, 27, 625, 52, 201, 30, 973, 725, 333, 742, 428, 623, 860, 875, 107, 418, 289, 430, 886, 218, 836, 770, 312, 711, 794, 218, 788, 848, 857, 259, 465, 348, 414, 788, 893, 781, 850, 18, 828, 150, 755, 117, 428, 948, 38, 654, 810, 10, 2, 403, 946, 704, 251, 206, 652, 153, 170, 471, 512, 946, 941, 228, 986, 93, 916, 243, 81, 299, 731, 786, 857, 866, 468, 353, 585, 812, 39, 185, 421, 641, 900, 342, 579, 437, 754, 651, 318, 73, 905, 953, 392, 101, 716, 586, 948, 701, 509, 615, 781, 822, 197, 360, 575, 883, 30, 174, 433, 774, 887, 226, 340, 191, 897, 371, 982, 58, 228, 994, 846, 526, 346, 420, 287, 938, 708, 219, 380, 554, 844, 261, 155, 49, 6, 709, 661, 738, 349, 861, 559, 616, 910, 982, 735, 192, 367, 510, 763, 482, 89, 889, 978, 95, 34, 220, 357, 891, 956, 427, 561, 356, 412, 266, 775, 745, 30, 619, 271, 341, 184, 996, 77, 870, 912, 753, 853, 986, 540, 339, 386, 297, 548, 485, 658, 165, 157, 654, 754, 760, 310, 216, 475, 830, 993, 531, 590, 22, 270, 288, 698, 211, 293, 1, 46, 77, 172, 284, 663, 592, 467, 772, 511, 72, 852, 0, 321, 73, 554, 749, 647, 802, 942, 870, 536, 107, 384, 591, 275, 398, 498, 260, 928, 304, 193, 996, 631, 350, 863, 813, 634, 372, 708, 247, 760, 40, 258, 590, 829, 687, 124, 376, 527, 312, 766, 521, 557, 114, 897, 502, 14, 251, 85, 185, 194, 168, 349, 628, 814, 303, 402, 407, 578, 302, 620, 324, 132, 878, 848, 795, 812, 138, 78, 319, 40, 237, 651, 438, 16, 182, 721, 328, 164, 177, 161, 371, 577, 72, 391, 519, 658, 614, 356, 15, 702, 148, 782, 751, 727, 78, 381, 812, 291, 207, 912, 431, 566, 484, 59, 418, 532, 908, 492, 715, 473, 680, 775, 440, 739, 919, 164, 904, 651, 760, 470, 801, 168, 745, 895, 639, 540, 71, 164, 839, 373, 302, 759, 190, 248, 853, 554, 177, 306, 825, 691, 467, 301, 278, 321, 589, 335, 917, 350, 670, 372, 622, 191, 843, 144, 352, 35, 328, 975, 622, 661, 597, 818, 702, 280, 88, 945, 915, 549, 428, 523, 499, 245, 812, 334, 441, 4, 844, 528, 790, 676, 566, 269, 660, 233, 84, 478, 436, 384, 32, 715, 983, 696, 365, 609, 5, 887, 569, 258, 725, 716, 696, 305, 84, 335, 197, 478, 175, 724, 208, 33, 810, 33, 372, 366, 994, 811, 188, 416]
# lst_partial = [4, 5, 5, 6, 6, 9, 11, 13, 14, 14, 17, 17, 21, 22, 24, 26, 27, 27, 32, 33, 34, 36, 44, 45, 50, 53, 57, 57, 58, 59, 59, 59, 59, 60, 62, 63, 64, 64, 65, 68, 69, 69, 69, 70, 79, 81, 82, 86, 87, 88, 93, 93, 93, 99, 100, 100, 104, 104, 105, 105, 106, 106, 108, 112, 115, 121, 122, 125, 126, 127, 129, 131, 132, 132, 135, 136, 140, 143, 147, 148, 149, 150, 150, 151, 151, 153, 154, 155, 159, 161, 161, 161, 164, 165, 166, 166, 166, 168, 172, 173, 174, 176, 177, 179, 182, 183, 185, 187, 189, 189, 192, 194, 195, 196, 197, 199, 200, 200, 205, 206, 206, 212, 212, 213, 220, 222, 225, 228, 229, 231, 233, 234, 235, 240, 240, 241, 241, 242, 244, 246, 247, 248, 249, 255, 255, 260, 265, 267, 269, 271, 274, 275, 277, 281, 283, 284, 289, 290, 291, 292, 293, 294, 294, 300, 301, 302, 302, 302, 304, 304, 305, 313, 315, 316, 320, 320, 324, 325, 328, 329, 329, 332, 334, 336, 337, 338, 342, 345, 346, 350, 352, 353, 353, 354, 355, 361, 363, 363, 365, 366, 370, 372, 372, 377, 377, 377, 380, 381, 382, 383, 385, 385, 387, 387, 389, 390, 390, 394, 394, 396, 399, 399, 400, 401, 408, 409, 409, 412, 413, 421, 424, 432, 432, 437, 437, 442, 442, 443, 443, 444, 444, 445, 447, 449, 451, 457, 457, 457, 459, 459, 460, 461, 463, 464, 468, 469, 471, 472, 474, 481, 481, 483, 485, 486, 488, 490, 490, 490, 493, 496, 496, 497, 502, 506, 506, 509, 512, 514, 515, 518, 520, 521, 522, 523, 528, 529, 531, 537, 538, 540, 540, 545, 546, 549, 551, 555, 562, 565, 565, 568, 568, 574, 575, 577, 581, 582, 585, 586, 588, 588, 589, 591, 593, 594, 599, 599, 600, 601, 610, 611, 612, 616, 618, 619, 622, 623, 625, 627, 628, 628, 629, 630, 630, 636, 641, 642, 642, 648, 648, 650, 652, 652, 656, 659, 661, 662, 662, 663, 663, 664, 666, 667, 668, 668, 670, 671, 672, 675, 676, 677, 679, 686, 687, 687, 688, 688, 690, 694, 695, 697, 697, 698, 699, 700, 702, 704, 708, 709, 709, 710, 713, 713, 718, 719, 720, 721, 722, 724, 726, 728, 730, 732, 734, 736, 737, 741, 742, 743, 743, 746, 746, 756, 760, 761, 765, 768, 773, 779, 781, 782, 784, 785, 786, 791, 792, 794, 797, 798, 800, 801, 803, 804, 804, 805, 806, 807, 815, 816, 816, 826, 828, 829, 833, 835, 836, 837, 838, 838, 846, 848, 854, 855, 861, 866, 867, 867, 870, 873, 875, 875, 875, 876, 879, 881, 882, 883, 885, 886, 886, 887, 889, 891, 892, 894, 896, 900, 902, 902, 903, 911, 913, 913, 915, 916, 916, 916, 917, 922, 923, 930, 931, 932, 940, 944, 945, 946, 947, 951, 955, 957, 958, 959, 959, 960, 967, 967, 969, 970, 971, 981, 982, 985, 987, 988, 988, 989, 989, 989, 992, 993, 996, 1000, 2, 6, 10, 10, 18, 18, 22, 27, 30, 30, 30, 34, 38, 38, 39, 43, 49, 52, 55, 58, 67, 71, 73, 77, 79, 81, 89, 93, 95, 95, 101, 107, 115, 117, 125, 131, 139, 150, 153, 155, 157, 165, 170, 171, 173, 174, 184, 185, 191, 192, 197, 201, 206, 216, 218, 218, 219, 220, 226, 228, 228, 243, 249, 251, 252, 259, 261, 266, 270, 271, 287, 288, 289, 294, 297, 299, 306, 310, 312, 318, 333, 334, 339, 340, 341, 342, 346, 348, 349, 353, 356, 357, 360, 367, 370, 371, 380, 384, 386, 390, 392, 394, 403, 405, 412, 412, 414, 418, 420, 421, 427, 428, 428, 430, 433, 437, 465, 468, 470, 471, 474, 475, 482, 485, 490, 509, 510, 512, 517, 523, 526, 526, 531, 536, 540, 548, 554, 558, 559, 561, 567, 571, 575, 579, 585, 586, 590, 615, 616, 619, 623, 625, 627, 638, 641, 651, 652, 654, 654, 658, 661, 692, 694, 698, 701, 704, 708, 709, 711, 716, 725, 727, 731, 735, 738, 742, 745, 745, 753, 754, 754, 755, 760, 763, 770, 774, 775, 781, 781, 786, 788, 788, 793, 794, 810, 812, 815, 822, 828, 829, 830, 836, 844, 846, 847, 848, 850, 852, 853, 853, 854, 857, 857, 860, 860, 861, 864, 866, 870, 875, 883, 886, 887, 889, 891, 893, 897, 900, 905, 910, 912, 916, 927, 929, 938, 941, 946, 946, 947, 948, 948, 953, 956, 956, 967, 973, 976, 978, 982, 982, 984, 986, 986, 993, 994, 996, 0, 1, 14, 15, 16, 40, 40, 46, 59, 72, 72, 73, 77, 78, 78, 85, 107, 114, 124, 132, 138, 148, 161, 164, 168, 172, 177, 182, 185, 193, 194, 207, 211, 237, 247, 251, 258, 260, 275, 284, 291, 293, 302, 303, 304, 312, 319, 321, 324, 328, 349, 350, 356, 371, 372, 376, 381, 384, 391, 398, 402, 407, 418, 431, 438, 440, 467, 473, 484, 492, 498, 502, 511, 519, 521, 527, 532, 536, 554, 557, 566, 577, 578, 590, 591, 592, 614, 620, 628, 631, 634, 647, 651, 658, 663, 680, 687, 702, 708, 715, 721, 727, 739, 749, 751, 760, 766, 772, 775, 782, 795, 802, 812, 812, 813, 814, 829, 848, 852, 863, 870, 878, 897, 908, 912, 928, 942, 996, 4, 35, 71, 88, 144, 164, 164, 168, 177, 190, 191, 245, 248, 278, 280, 301, 302, 306, 321, 328, 334, 335, 350, 352, 372, 373, 428, 441, 467, 470, 499, 523, 528, 540, 549, 554, 589, 597, 622, 622, 639, 651, 661, 670, 691, 702, 745, 759, 760, 801, 812, 818, 825, 839, 843, 844, 853, 895, 904, 915, 917, 919, 945, 975, 5, 32, 33, 33, 84, 84, 175, 188, 197, 208, 233, 258, 269, 305, 335, 365, 366, 372, 384, 416, 436, 478, 478, 566, 569, 609, 660, 676, 696, 696, 715, 716, 724, 725, 790, 810, 811, 887, 983, 994]
#
# stack = [[0, 511, True, 512], [512, 767, True, 256], [768, 895, True, 128], [896, 959, True, 64], [960, 999, True, 40]]
# stack_res = timsort(lst)
#
# lst_4 = []
# for i in stack:
#     stuff = lst_partial[i[0]:i[1] + 1]
#     lst_4 = lst_4 + stuff
# if lst_4.sort() == lst2.sort():
#     print(True)
#
# lst2.sort()
# if lst == lst2:
#     print(True)