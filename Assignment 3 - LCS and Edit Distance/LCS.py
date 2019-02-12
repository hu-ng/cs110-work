# Length of longest common subsequence algorithm
def len_lcs(x, y): # Inspired by the pseudocode from Introduction to Algorithms, Cormen et al.
    """Returns the length of the two strings"""

    # Protection against bad inputs
    if type(x) != str or type(y) != str:
        raise TypeError('Inputs must be strings')

    # Length of the two strings, used as array dimensions
    m = len(x)
    n = len(y)

    # Setting up the array of size (m+1)(n+1)
    c = [[0 for x in range(n + 1)] for y in range(m + 1)]
    for i in range(m):  # Iterate from x[0] -> x[m - 1]
        for j in range(n):  # Iterate from y[0] -> y[n - 1]
            # If the last elements of the strings are the same
            if x[i] == y[j]:
                c[i + 1][j + 1] = c[i][j] + 1

             # If the last elements of the strings are different, case 1
            elif c[i][j + 1] >= c[i + 1][j]:
                c[i + 1][j + 1] = c[i][j + 1]
            else:  # Case 2
                c[i + 1][j + 1] = c[i + 1][j]
    return c[m][n]  # Return the length of the LCS of the two full strings


# Minimum edit distance algorithm implementation
def edit_dist(x, y):
    """Returns the minimum number of insertions,
        deletions, and substitions needed to turn x -> y"""

    # Protection against bad inputs
    if type(x) != str or type(y) != str:
        raise TypeError('Inputs must be strings')

    # The lengths of the two strings, will be used as array dimensions
    m = len(x)
    n = len(y)

    # Initialize a table, similar to that of the LCS algorithm
    table = [[0 for b in range(n + 1)] for c in range(m + 1)]

    # The nested for-loop traverses the table
    for i in range(m + 1):
        for j in range(n + 1):
            # If x == null, the cost of x -> y is inserting every element of y
            if i == 0:
                table[i][j] = j

            # If y == null, the cost of x -> y is deleting every element of x
            elif j == 0:
                table[i][j] = i
            # If the last elements of x and y are equal,
            # the edit dist is that of table[i - 1][j - 1]
            elif x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            # If the last elements of x and y are different, 3 cases:
                # substituting an element from x
                # inserting an element from x
                # deleting an element from x
            # The minimum of the three is chosen
            else:
                table[i][j] = 1 + min(table[i - 1][j - 1],
                                  table[i][j - 1],
                                  table[i - 1][j])

            # 1 is added because we're making a new move

    # Initializing i and j that points to the bottom-right cell of 'table'
    i = m
    j = n
    ins = 0   # The number of insertions
    dels = 0  # The number of deletions
    subs = 0  # The number of substitutions

    # while loop retraces the path that the algorithm took to turn X into Y
    while i != 0 and j != 0:
        if x[i - 1] == y[j - 1]:
            # Check if the elements of x and y in these indices are equal
            # If they are, then no edits are needed in those elements
            # i and j are decremented
            i -= 1
            j -= 1
        else:  # If the elements are different.
            # The edit distance value prior to making a change
            val = table[i][j] - 1

             # If the algorithm took the substitution route
            if val == table[i - 1][j - 1]:
                subs += 1
                i -= 1
                j -= 1

            # If the algorithm took the insertion route
            elif val == table[i][j - 1]:
                ins += 1
                j -= 1

            # The algorithm took the deletion route/ val == table[i - 1][j]
            else:
                dels += 1
                i -= 1

    return ins, dels, subs
