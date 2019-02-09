# 1. Length of longest common subsequence
def len_lcs(x, y):

    if type(x) != str or type(y) != str:
        raise ValueError('Inputs must be strings')

    m = len(x)  # Length of the first string
    n = len(y)  # Length of the second string
    c = [[0 for x in range(n + 1)] for y in range(m + 1)]  # Setting up the matrix size (m+1)(n+1)
    for i in range(m):  # Iterate from x[0] -> x[m - 1]
        for j in range(n):  # Iterate from y[0] -> y[n - 1]
            if x[i] == y[j]:  # If the last elements of the strings are the same
                c[i + 1][j + 1] = c[i][j] + 1
            elif c[i][j + 1] >= c[i + 1][j]:  # If the last elements of the strings are different, case 1
                c[i + 1][j + 1] = c[i][j + 1]
            else:  # Case 2
                c[i + 1][j + 1] = c[i + 1][j]
    # common_sub = ''
    # while i != -1 and j != -1:
    #     if c[i + 1][j + 1] == c[i][j] + 1:
    #         common_sub = common_sub + x[i]
    #         i -= 1
    #         j -= 1
    #     elif c[i][j + 1] >= c[i + 1][j]:
    #         i -= 1
    #     else:
    #         j -= 1
    # common_sub = common_sub[::-1]
    return c[m][n]  # Return the length of the LCS of the two full strings


str1 = 'CAGCGGGTGCGTAATTTGGAGAAGTTATTCTGCAACGAAATCAATCCTGTTTCGTTAGCTTACGGACTACGACGAGAGGGTACTTCCCTGATATAGTCAC'
str2 = 'CAAGTCGGGCGTATTGGAGAATATTTAAATCGGAAGATCATGTTACTATGCGTTAGCTCACGGACTGAAGAGGATTCTCTCTTAATGCAA'
str3 = 'CATGGGTGCGTCGATTTTGGCAGTAAAGTGGAATCGTCAGATATCAATCCTGTTTCGTAGAAAGGAGCTACCTAGAGAGGATTACTCTCACATAGTA'
str4 = 'CAAGTCCGCGATAAATTGGAATATTTGTCAATCGGAATAGTCAACTTAGCTGGCGTTAGCTTTACGACTGACAGAGAGAAACCTGTCCATCACACA'
str5 = 'CAAGTCCGGCGTAATTGGAGAATATTTTGCAATCGGAAGATCAATCTTGTTAGCGTTAGCTTACGACTGACGAGAGGGATACTCTCTCTAATACAA'
str6 = 'CACGGGCTCCGCAATTTTGGGTCAAGTTGCATATCAGTCATCGACAATCAAACACTGTTTTGCGGTAGATAAGATACGACTGAGAGAGGACGTTCGCTCGAATATAGTTAC'
str7 = 'CACGGGTCCGTCAATTTTGGAGTAAGTTGATATCGTCACGAAATCAATCCTGTTTCGGTAGTATAGGACTACGACGAGAGAGGACGTTCCTCTGATATAGTTAC'
genes = [str1, str2, str3, str4, str5, str6, str7]


def print_table(lst):
    data = []
    data.append(['Gene', 1,2,3,4,5,6,7])
    for i in range(len(lst)):
        result_lst = []
        for j in range(len(lst)):
            result_lst.append(len_lcs(lst[i], lst[j]))
        result_lst.insert(0, i + 1)
        data.append(result_lst)
    lens = [max(len(str(col)) for col in row) for row in data]
    for row in zip(*data):
        # Pass the column widths dynamically.
        print('{:>{lens[0]}} {:>{lens[1]}} {:>{lens[2]}} {:>{lens[3]}} {:>{lens[4]}} {:>{lens[5]}} {:>{lens[6]}} {:>{lens[7]}}'.format(*row, lens=lens))


def edit_dist(x, y):  # Returns the minimum number of edits needed to turn x -> y
    m = len(x)
    n = len(y)
    table = [[0 for b in range(n + 1)] for c in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                # If x is null, then the cost of x -> y is inserting every element of y
                table[i][j] = j
            elif j == 0:
                # If y is null, then the cost of x -> y is deleting every element of x
                table[i][j] = i
            elif x[i - 1] == y[j - 1]:
                # If the last elements of x and y are the same, then the edit dist is that of table[i - 1][j - 1]
                table[i][j] = table[i - 1][j - 1]
            else:  # If the last elements of x and y are different, then
                table[i][j] = 1 + min(table[i - 1][j - 1],  # The cost of substituting an element from x
                                  table[i][j - 1],  # The cost of inserting an element from x
                                  table[i - 1][j])  # The cost of deleting an element from x

                # 1 is added to this cost because we are making a new move in addition to this prior cost

    # Initializing i and j to point to the bottom-right cell of 'table'
    i = m
    j = n
    ins = 0   # The number of insertions
    dels = 0  # The number of deletions
    subs = 0  # The number of substitutions
    while i != 0 and j != 0:
        if x[i - 1] == y[j - 1]:
            # Check if the elements of x and y corresponding to the indices are equal
            # If they are, then no change is needed in those elements
            # i and j are decremented
            i -= 1
            j -= 1
        else:  # If the elements are different.
            val = table[i][j] - 1  # The value prior to making a change
            if val == table[i - 1][j - 1]:  # If the algorithm took the substitution route
                subs += 1
                i -= 1
                j -= 1
            elif val == table[i][j - 1]:  # If the algorithm took the insertion route
                ins += 1
                j -= 1
            else:  # The algorithm took the deletion route
                dels += 1
                i -= 1

    return ins, dels, subs  # Return the minimum number of insertions, deletions, and substitutions in a tuple


def prob():
    result_lst = [edit_dist(str1, str5), edit_dist(str1, str7),
                  edit_dist(str5, str2), edit_dist(str5, str4),
                  edit_dist(str7, str6), edit_dist(str7, str3)]
    prob_ins = []
    prob_dels = []
    prob_subs = []

    for i in result_lst:
        for j in range(len(i)):
            if j == 0:
                prob_ins.append(i[j]/sum(i))
            elif j == 1:
                prob_dels.append(i[j]/sum(i))
            else:
                prob_subs.append(i[j]/sum(i))
    avg_ins = sum(prob_ins)/len(prob_ins)
    avg_dels = sum(prob_dels)/len(prob_dels)
    avg_subs = sum(prob_subs)/len(prob_subs)

    print('The average probability of an insertion happening if a mutation happens is', avg_ins)
    print('The average probability of a deletion happening if a mutation happens is', avg_dels)
    print('The average probability of a substitution happening if a mutation happens is', avg_subs)


def rlts(lst):  # Takes an array of genes (strings)
    pairs = []  # Contains pairs of genes in 2-element tuples
    for i in range(len(lst)):  # Essentially creating a table row-wise as in part 2
        max_lcs = 0  # Initiate a variable to hold the maximum LCS value
        match = None  # Initiate a variable to reference to the gene with which the current gene has the highest LCS
        for j in range(len(lst)):
            if lst[i] == lst[j]:  # Avoid comparing with itself
                continue
            lcs = len_lcs(lst[i], lst[j])  # Uses the len_lcs function in part 1
            if lcs > max_lcs:  # Checks if the current LCS is the largest
                max_lcs = lcs
                match = j
        pairs.append((i + 1, match + 1))  # Appends the pair after going through a row in the table
        # To match the output with the tree above, 'i' and 'match' are incremented by 1 before being appended
        # The relationships are still the same.
    return pairs

test = 'c'
test2 = 'b'
print(edit_dist(test, test2))





