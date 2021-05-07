def s(x, y, i, j):
    if x[i] != y[j]:
        return MISSMATCH
    else:
        return MATCH

def way( TABLE, m, n):
    if m == 0 and n == 0:
        return
    if n != 0:
        insert = TABLE[m][n - 1] + GAP
    else:
        insert = -10**9
    if m != 0 and n != 0:
        align = TABLE[m - 1][n - 1] + s(x, y, m - 1, n - 1)
    else:
        align = -10**9
    if m != 0:
        delete = TABLE[m - 1][n] + GAP
    else:
        delete = -10**9

    choosen = max(insert, align, delete)

    if choosen == insert:
        sequence2.append(str(y[n - 1]))
        sequence1.append('_')
        palki.append(' ')
        return way(TABLE, m, n - 1)

    elif choosen == align:
        sequence2.append(str(y[n - 1]))
        sequence1.append(str(x[m - 1]))
        if str(y[n - 1])==str(x[m - 1]):
            palki.append('|')
        else:
            palki.append(' ')

        return way(TABLE, m - 1, n - 1)

    elif choosen == delete:
        sequence2.append("_")
        sequence1.append(str(x[m - 1]))
        palki.append(' ')

        return way(TABLE, m - 1, n)

def alignment(x,y):
    m = len(x)
    n = len(y)
    TABLE = [[0 for r in range(n + 1)] for jy in range(m + 1)]

    for i in range(1, m+1):
        TABLE[i][0] = i*GAP
    for j in range(1,n + 1):
        TABLE[0][j] = j*GAP
    for i in range(1, m+1):
        for j in range(1, n+1):
            TABLE[i][j] = max(
                TABLE[i - 1][j - 1] + s(x, y, i - 1, j - 1),
                TABLE[i - 1][j] + GAP,
                TABLE[i][j - 1] + GAP,
            )
    way(TABLE, m, n)
    return (sequence1[::-1],sequence2[::-1],palki[::-1])

file = open('filename', 'r')
x=0
y=0
for line in file:
    if x=='':
        x = line.upper().strip()
    elif y=='':
        y = line.upper().strip()
    if line.startswith('>') and x==0:
        x = ''
    elif line.startswith('>') and y==0:
        y = ''
file.close()

alignment_sequence1 = []
alignment_sequence2 = []
palki=[]
MATCH = 1
MISSMATCH = -1
GAP = -2
steps,steps2,palki = alignment(x,y)
alignment_file = open('alignment.txt','w')

alignment_file.write(''.join(steps)+'\n')
alignment_file.write(''.join(palki)+'\n')
alignment_file.write(''.join(steps2)+'\n')
alignment_file.close()
#print(''.join(steps))
#print(''.join(palki))
#print(''.join(steps2))
