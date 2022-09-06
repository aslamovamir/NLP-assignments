def problem2(s1, s2):
    # first let's define a table that would represent all the possible
    # Lavenstain distances between characters of two strings
    num_rows = len(s1) + 1
    num_cols = len(s2) + 1
    # now, let's initialize all entries to zero
    table = []
    row = []
    for i in range(num_rows):
        for j in range(num_cols):
            row.append(0)
        table.append(row)
        row = []

    # now we know that source prefixes can be replaced by empty strings using DELETION operation
    for i in range(1, num_rows):
        table[i][0] = i

    # we also know that target prefixes can be created using INSERTION operation
    for i in range(1, num_cols):
        table[0][i] = i

    # now we loop through the table and see which operation would iteratively result in
    # the minimum number of costs of operations
    for col in range(1, num_cols):
        for row in range(1, num_rows):
            # if characters are equal, we need no operation at all
            if s1[row-1] == s2[col-1]:
                cost = 0
            else:
                # otherwise we need an operation with cost of 2 - SUBSTITUTION
                cost = 2
            table[row][col] = min(table[row-1][col] + 1,
                                  table[row][col-1] + 1,
                                  table[row-1][col-1] + cost)

    return table[row][col]
