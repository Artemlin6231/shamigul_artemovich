def f(x, y, i, j):
    if x[i] != y[j]:
        return 1
    else:
        return 0

def way( TABLE, m, n):
    if m == 0 and n == 0:
        return
    if n != 0:
        insert = TABLE[m][n - 1] + 1
    else:
        insert = 10**9
    if m != 0 and n != 0:
        align = TABLE[m - 1][n - 1] + f(x, y, m - 1, n - 1)
    else:
        align = 10**9
    if m != 0:
        delete = TABLE[m - 1][n] + 1
    else:
        delete = 10**9

    choosen = min(insert, align, delete)

    if choosen == insert:
        alignment_sequence2.append(str(y[n - 1]))
        alignment_sequence1.append('_')
        palki.append(' ')
        return way(TABLE, m, n - 1)

    elif choosen == align:
        alignment_sequence2.append(str(y[n - 1]))
        alignment_sequence1.append(str(x[m - 1]))
        if str(y[n - 1])==str(x[m - 1]):
            palki.append('|')
        else:
            palki.append(' ')

        return way(TABLE, m - 1, n - 1)

    elif choosen== delete:
        alignment_sequence2.append("_")
        alignment_sequence1.append(str(x[m - 1]))
        palki.append(' ')

        return way(TABLE, m - 1, n)

def alignment(x,y):
    m = len(x)
    print(m)
    n = len(y)
    print(n)
    TABLE = [[0 for r in range(n + 1)] for jy in range(m + 1)]

    for i in range(1, m+1):
        TABLE[i][0] = i
    for j in range(1,n + 1):
        TABLE[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            TABLE[i][j] = min(
                TABLE[i - 1][j - 1] + f(x, y, i - 1, j - 1),
                TABLE[i - 1][j] + 1,
                TABLE[i][j - 1] + 1,
            )
    for i in range(m + 1):
        print(TABLE[i])
    way(TABLE, m, n)
    return (TABLE[m][n],alignment_sequence1[::-1],alignment_sequence2[::-1],palki[::-1])


x ='TTAGCTGCTTAGA'.upper()#input('Введите последователльность:')
y ='AGCTAGTTgaT'.upper()#input('Введите вторую последователльность:')
alignment_sequence1=[]
alignment_sequence2 = []
palki=[]
min_edit, steps,steps2,palki = alignment(x,y)
print(''.join(steps))
print(''.join(palki))
print(''.join(steps2))
