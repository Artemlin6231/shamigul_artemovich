import telegram
import config
TOKEN = config.token
bot = telegram.Bot(TOKEN)
import numpy as np
import matplotlib.pyplot as plt
from Bio.SeqIO import parse
from Bio.SeqRecord import SeqRecord
from Bio import pairwise2
def get_last_update_id(updates):
    """Возвращает ID последнего апдейта"""
    id_list = list()  # пустой список ID апдейтов
    for update in updates:  # для каждого апдейта
        id_list.append(update["update_id"])  # заносим в список его ID
    return (max(id_list))  # возвращаем последний


def allalignment(X, Y):
    '''Выравнивание сшитой послеовательности со старой
    '''
    alignments = pairwise2.align.globalms(X, Y, 1, -0.1, -0.2, -0.2)
    MISSMATCH = pairwise2.align.globalms(X, Y, 0, -1, 0, 0)[0].score
    GAP = pairwise2.align.globalms(X, Y, 0, 0, -1, -1)[0].score
    bot.sendMessage(last_chat_id,print('миссматчей = ' + str(abs(int(MISSMATCH))), 'разрывов = ' + str(abs(int(GAP))))
    return alignments[0]


def compare(R1, R2, C1, C2):
    '''выбор наилучшего выравнивания более подходящего для последовательности сравнения
    выравнивание концов прочтений, для получения области их перекрывания
    сшивание ридов в полную последовательность секвенированной кДНК
    '''
    if R1[0] > C1[0]:
        X = [READ1, R1[0], R1[1], R1[2]]
    else:
        X = [READ_CMP1, C1[0], C1[1], C1[2]]
    if R2[0] > C2[0]:
        Y = [READ2, R2[0], R2[1], R2[2]]
    else:
        Y = [READ_CMP2, C2[0], C2[1], C2[2]]
    A = alignment(X[0], Y[0])[0]
    if X[2] < Y[2]:
        Z = str(X[0][X[2]:int(A[3])]) + str(Y[0][:Y[3] + 1])
    else:
        Z = str(Y[0][Y[2]:Y[3]]) + str(X[0][:X[3] + 1])
    ANS = allalignment(Z, GEN)

    '''построение графика выравнивания в стадии разроботки
    '''
    LEN = len(ANS[0])
    ANS1 = ANS[0]
    ANS2 = ANS[1]
    t = np.arange(0, LEN, 1)
    x = []
    for i in range(LEN):
        if ANS1[int(i)] == ANS2[int(i)]:
            x.append(1)
        else:
            x.append(np.nan)
    plt.plot(t, t * x, )
    plt.grid(True)
    plt.show()
    return Z, ANS, LEN


def complement(X):
    '''
    замена рида на обратный коплиментарный для сравнения
    '''
    Y = ''
    for char in X:
        ID = X.index(char)
        if X[ID] == 'A':
            Y += 'T'
        if X[ID] == 'T':
            Y += 'A'
        if X[ID] == 'C':
            Y += 'G'
        if X[ID] == 'G':
            Y += 'C'
    return Y[::-1]


def alignment(X, Y):
    '''
    локальное выравнивание ридов по последовательности сравнения
    в случае отсутсявия выравнивания возвращает массив из -1 для предотвращения ошибки
    '''
    alignments = pairwise2.align.localms(X, Y, 1, -1, -5, -1)
    if alignments != []:
        return alignments
    else:
        return [[-1, -1, -1, -1, -1, -1]]

last_update_id = None
while True:
    updates = bot.getUpdates(last_update_id, timeout=100)
    if len(updates) > 0:
        last_update_id = get_last_update_id(updates) + 1
        for update in updates:  # сообщения могут приходить быстро, быстрее, чем работает код
            last_message = update["message"]  # взяли из него сообщен
            last_chat_id = last_message['chat']['id']
            fid = last_message.document.file_id
            inpfile = bot.getFile(fid)
            inpfile.download('filename')
            f=open('filename','r')
            mas = [line.strip() for line in f]
            f.close()
            gen_number=mas.index('GEN')+1
            GEN=mas[gen_number].upper()
            read1_number=mas.index('READ1')+1
            read2_number = mas.index('READ2') + 1
            READ1=mas[read1_number].upper()
            READ2 = mas[read2_number].upper()
            GL = len(GEN)
            RL1 = len(READ1)
            RL2 = len(READ2)
            # print(GL, RL1, RL2)

            READ_CMP1 = complement(READ1)
            READ_CMP2 = complement(READ2)

            R1 = alignment(READ1, GEN)[0][2:5]
            R2 = alignment(READ2, GEN)[0][2:5]
            C1 = alignment(READ_CMP1, GEN)[0][2:5]
            C2 = alignment(READ_CMP2, GEN)[0][2:5]

            Z, ANS, LEN = compare(R1, R2, C1, C2)
            for i in range(LEN):
                if ANS[0][i] == '-':
                    bot.sendMessage(last_chat_id,'Делеция в ' + str(i))
                elif ANS[1][i] == '-':
                    bot.sendMessage(last_chat_id,'Инсерция в ' + str(i))
                elif ANS[0][i] != ANS[1][i]:
                    bot.sendMessage(last_chat_id,'МиссМатч в ' + str(i))
            bot.sendMessage(last_chat_id,Z)
