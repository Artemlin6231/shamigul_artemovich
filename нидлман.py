def s(x, y, i, j):
    '''

    '''
    if x[i] != y[j]:
        return 1
    else:
        return 0
#
def find_solution( TABLE, m, n):
    if m == 0 and n == 0:
        return
    if n != 0:
        insert = TABLE[m][n - 1] + 1
    else:
        insert = float("inf")
    if m != 0 and n != 0:
        align = TABLE[m - 1][n - 1] + s(x, y, m - 1, n - 1)
    else:
        align = float("inf")
    if m != 0:
        delete = TABLE[m - 1][n] + 1
    else:
    delete = float("inf")

    choosen = min(insert, align, delete)

    if choosen == insert:
        solution.append("insert_" + str(y[n - 1]))
        return find_solution(TABLE, m, n - 1)

    elif choosen == align:
        solution.append("align_" + str(y[n - 1]))
        return find_solution(TABLE, m - 1, n - 1)

    elif choosen== delete:
        solution.append("remove_" + str(x[m - 1]))
        return find_solution(TABLE, m - 1, n)

def alignment(x,y):
    n = len(y)
    m = len(x)
    OPT = [[0 for r in range(n + 1)] for jy in range(m + 1)]

    for i in range(1, m + 1):
        OPT[i][0] = i

    for j in range(1, n + 1):
        OPT[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            OPT[i][j] = min(
                OPT[i - 1][j - 1] + s(x, y, i - 1, j - 1),
                OPT[i - 1][j] + 1,
                OPT[i][j - 1] + 1,
            )

    find_solution(OPT, m, n)

    return (OPT[m][n],solution[::-1])
x = 'TGACGTGC'
y = 'TCGACGTCA'
solution = []
print('We we want to transform: ' + x + ' to: ' + y)
min_edit, steps = alignment(x,y)
print('Minimum amount of edit steps are: ' + str(min_edit))
print('And the way to do it is: ' + str(steps))
