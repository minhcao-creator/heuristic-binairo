import io
from Cell import Cell
import json
from timeit import default_timer
import psutil
import os


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


start = default_timer()
memBefore = process_memory()

mypuzzle = []
mygraph = dict()
unique_r = dict()
unique_c = dict()
steps = []
startPuzzle = []


address = ".\puzzles\puzzle10.txt"
with open(address) as reader:
    myinput = reader.read()


buf = io.StringIO(myinput)
n, m = map(int, buf.readlines(1)[0].replace(
    "\t", " ").replace("\n", "").split(" "))

for i in range(n):
    buffread = buf.readlines(1)[0].replace(
        "\t", " ").replace("\n", "").split(" ")
    mynd = []
    for ii in range(m):
        mynd.append(buffread[ii])
    mypuzzle.append(mynd)

for i in range(n):
    for ii in range(m):
        if (mypuzzle[i][ii] == '-'):
            mygraph[(i, ii)] = Cell(-1)
        else:
            mygraph[(i, ii)] = Cell(int(mypuzzle[i][ii]))

for i in range(n):
    unique_r[i] = None
    unique_c[i] = None


def updatestr(graph, n, row=None, column=None):

    mystr = ''

    if (row == None and column == None):

        for i in range(n):
            mystr = ''
            for ii in range(n):
                if (mygraph[(i, ii)].value == -1):
                    break
                mystr += str(mygraph[(i, ii)].value)
            if (len(mystr) == n):
                unique_r[i] = mystr

        for ii in range(n):
            mystr = ''
            for i in range(n):
                if (mygraph[(i, ii)].value == -1):
                    break
                mystr += str(mygraph[(i, ii)].value)
            if (len(mystr) == n):
                unique_c[i] = mystr
    else:

        mystr = ''
        for ii in range(n):
            if (mygraph[(row, ii)].value == -1):
                break
            mystr += str(mygraph[(row, ii)].value)

        if (len(mystr) == n):
            unique_r[row] = mystr
        else:
            unique_r[row] = None

        mystr = ''
        for i in range(n):
            if (mygraph[(i, column)].value == -1):
                break
            mystr += str(mygraph[(i, column)].value)

        if (len(mystr) == n):
            unique_c[column] = mystr
        else:
            unique_c[column] = None


def check_uniqe(n, x, y):
    rowstring = unique_r[x]
    columstring = unique_c[y]

    if rowstring == None and columstring == None:
        return True

    for i in range(n):
        if i == x:
            continue
        if (rowstring == unique_r[i] and rowstring != None):
            return False

    for i in range(n):
        if i == y:
            continue
        if (columstring == unique_c[i] and columstring != None):
            return False

    return True


updatestr(mygraph, n)


def backtracking(graph, n, cp):

    if isComplete(graph, n):
        return graph

    (x, y) = MRV(graph, n)
    for d in graph[(x, y)].domain:
        graph[(x, y)].value = d
        steps.append([x, y, d])
        satisfied = forward_checking(graph, x, y, n)
        if satisfied:
            done = backtracking(graph, n, cp)
            if done:
                return graph

        removeConstraints(graph, x, y, n)

        graph[(x, y)].value = -1
        updatestr(graph, n, x, y)
        steps.append([x, y, -1])


def forward_checking(graph, x, y, n):
    onesCol = 0
    zerosCol = 0
    onesRow = 0
    zerosRow = 0
    for i in range(n):
        if graph[(i, y)].value == 1:
            onesCol += 1
        elif graph[(i, y)].value == 0:
            zerosCol += 1
        if graph[(x, i)].value == 1:
            onesRow += 1
        elif graph[(x, i)].value == 0:
            zerosRow += 1

    checklist = []

    # check number of 0's and 1's
    for i in range(n):
        if graph[(i, y)].value == -1:
            if onesCol >= n/2:
                if 1 in graph[(i, y)].domain:
                    graph[(i, y)].domain.remove(1)
                    if len(graph[(i, y)].domain) == 0:
                        return False, checklist
            if zerosCol >= n/2:
                if 0 in graph[(i, y)].domain:
                    graph[(i, y)].domain.remove(0)
                    if len(graph[(i, y)].domain) == 0:
                        return False, checklist

        if graph[(x, i)].value == -1:
            if onesRow >= n/2:
                if 1 in graph[(x, i)].domain:
                    graph[(x, i)].domain.remove(1)
                    if len(graph[(x, i)].domain) == 0:
                        return False, checklist

            if zerosRow >= n/2:
                if 0 in graph[(x, i)].domain:
                    graph[(x, i)].domain.remove(0)
                    if len(graph[(x, i)].domain) == 0:
                        return False, checklist

    value = graph[(x, y)].value
    #  check in row
    for i in range(-1, 2, 2):

        # x 0 0 x
        if validIndex(x + i, n) and graph[(x + i, y)].value == value:
            if validIndex(x + 2 * i, n) and graph[(x + 2 * i, y)].value == -1:
                if value in graph[(x + 2 * i, y)].domain:
                    graph[(x + 2 * i, y)].domain.remove(value)
                    if len(graph[(x + 2 * i,  y)].domain) == 0:
                        return False, checklist
            if validIndex(x - i, n) and graph[(x - i, y)].value == -1:
                if value in graph[(x - i, y)].domain:
                    graph[(x - i, y)].domain.remove(value)
                    if len(graph[(x - i,  y)].domain) == 0:
                        return False, checklist

        if validIndex(x + i*2, n) and graph[(x + i*2, y)].value == value:
            if validIndex(x + i, n) and graph[(x + i, y)].value == -1:
                if value in graph[(x + i, y)].domain:
                    graph[(x + i, y)].domain.remove(value)
                    if len(graph[(x + i, y)].domain) == 0:
                        return False, checklist

        if validIndex(y + i, n) and graph[(x, y + i)].value == value:
            if validIndex(y + 2 * i, n) and graph[(x, y + 2 * i)].value == -1:
                if value in graph[(x, y + 2 * i)].domain:
                    graph[(x, y + 2 * i)].domain.remove(value)
                    if len(graph[(x, y + 2 * i)].domain) == 0:
                        return False, checklist
            if validIndex(y - i, n) and graph[(x, y - i)].value == -1:
                if value in graph[(x, y - i)].domain:
                    graph[(x, y - i)].domain.remove(value)
                    if len(graph[(x,  y - i)].domain) == 0:
                        return False, checklist

        if validIndex(y + i*2, n) and graph[(x, i*2 + y)].value == value:
            if validIndex(y + i, n) and graph[(x, y + i)].value == -1:
                if value in graph[(x, y + i)].domain:
                    graph[(x, y + i)].domain.remove(value)
                    if len(graph[(x, y + i)].domain) == 0:
                        return False, checklist

    updatestr(graph, n, x, y)
    if (not check_uniqe(n, x, y)):
        return False, checklist

    return True, checklist


def validIndex(x, n):
    if x < n and x >= 0:
        return True
    return False


def MRV(graph, n):
    x = -1
    y = -1
    lenDomain = 3
    for i in range(n):
        for j in range(n):
            if graph[(i, j)].value == -1:
                if len(graph[(i, j)].domain) == 1:
                    return i, j
                if len(graph[(i, j)].domain) < lenDomain:
                    lenDomain = len(graph[(i, j)].domain)
                    x = i
                    y = j

    return x, y


def isComplete(graph, n):
    for i in range(n):
        for j in range(n):
            if graph[(i, j)].value == -1:
                return False

    return True


def init(graph, n):
    for i in range(n):
        for j in range(n):
            if graph[(i, j)].value != -1:
                startPuzzle.append([i, j, graph[(i, j)].value])
                check = forward_checking(graph, i, j, n)
                if check == False:
                    return False
    return True


def removeConstraints(graph, x, y, n):
    onesCol = 0
    zerosCol = 0
    onesRow = 0
    zerosRow = 0
    for i in range(n):
        if graph[(i, y)].value == 1:
            onesCol += 1
        elif graph[(i, y)].value == 0:
            zerosCol += 1
        if graph[(x, i)].value == 1:
            onesRow += 1
        elif graph[(x, i)].value == 0:
            zerosRow += 1

    value = graph[(x, y)].value
    if value == 1:
        onesCol -= 1
        onesRow -= 1
    else:
        zerosCol -= 1
        zerosRow -= 1

    #  check in row
    for i in range(-1, 2, 2):

        # x 0 0 x
        if validIndex(x + i, n) and graph[(x + i, y)].value == value:
            if validIndex(x + 2 * i, n) and graph[(x + 2 * i, y)].value == -1:
                if value not in graph[(x + 2 * i, y)].domain:
                    graph[(x + 2 * i, y)].domain.append(value)

            if validIndex(x - i, n) and graph[(x - i, y)].value == -1:
                if value not in graph[(x - i, y)].domain:
                    graph[(x - i, y)].domain.append(value)

        if validIndex(x + i*2, n) and graph[(x + i*2, y)].value == value:
            if validIndex(x + i, n) and graph[(x + i, y)].value == -1:
                if value not in graph[(x + i, y)].domain:
                    graph[(x + i, y)].domain.append(value)

        if validIndex(y + i, n) and graph[(x, y + i)].value == value:
            if validIndex(y + 2 * i, n) and graph[(x, y + 2 * i)].value == -1:
                if value not in graph[(x, y + 2 * i)].domain:
                    graph[(x, y + 2 * i)].domain.append(value)

            if validIndex(y - i, n) and graph[(x, y - i)].value == -1:
                if value not in graph[(x, y - i)].domain:
                    graph[(x, y - i)].domain.append(value)

        if validIndex(y + i*2, n) and graph[(x, i*2 + y)].value == value:
            if validIndex(y + i, n) and graph[(x, y + i)].value == -1:
                if value not in graph[(x, y + i)].domain:
                    graph[(x, y + i)].domain.append(value)

    # check number of 0's and 1's
    for i in range(n):
        if graph[(i, y)].value == -1:
            if onesCol < n/2:
                if 1 not in graph[(i, y)].domain:
                    graph[(i, y)].domain.append(1)

            if zerosCol < n/2:
                if 0 not in graph[(i, y)].domain:
                    graph[(i, y)].domain.append(0)

        if graph[(x, i)].value == -1:
            if onesRow < n/2:
                if 1 not in graph[(x, i)].domain:
                    graph[(x, i)].domain.append(1)

            if zerosRow < n/2:
                if 0 not in graph[(x, i)].domain:
                    graph[(x, i)].domain.append(0)


def get_json_result(results):
    return json.dumps(results)


init(mygraph, n)
g = backtracking(mygraph, n, "forward")
hasAnswer = True
if g == None:
    hasAnswer = False
    print("The Puzzle does'nt have any solution!")
else:
    for i in range(n):
        for j in range(n):
            print(g[(i, j)].value, end=" ")
        print()
# print(steps)

memAfter = process_memory()
stop = default_timer()


print('Usage Memory:', memAfter - memBefore, 'bytes')
print('Time To Run: ', stop - start)
