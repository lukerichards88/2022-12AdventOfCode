with open('Day13Input.txt') as file:
    filestring = ""
    for line in file:
        filestring += line
file = filestring.split('\n\n')
output = [[line.split('\n')[0], line.split('\n')[1]] for line in file]
pairs = []
A = None
B = None
for a, b in output:
    strA = f"A = {a}"
    strB = f"B = {b}"
    exec(strA)
    exec(strB)
    pairs.append((A, B))
#print(pairs)
a, b = pairs[0]
def test(a, b, firstLayer=False):
    a = [a] if isinstance(a, int) else a
    b = [b] if isinstance(b, int) else b
    lengthTest = (len(a) < len(b))
    lengthTestB = (len(a) > len(b))
    #print(f"Input: {a} {b}")
    for c, d in zip(a, b):
        #print(c, d)
        if isinstance(c, int) and isinstance(d, int):
            if c < d:
                return True
            if c > d:
                return False
        elif isinstance(c, list) and isinstance(d, list):
            result = test(c, d)
            if result:
                return True
            if result == None:
                pass
            if result == False:
                return False

        elif [type(c), type(d)] == [list, int]:
            try:
                if c[0] < d:
                    return True
                return False
            except (TypeError, IndexError):
                result = test(c, d)
                if result:
                    return True
                if result == None:
                    pass
                if result == False:
                    return False
        elif [type(c), type(d)] == [int, list]:
            try:
                if c < d[0]:
                    return True
                return False
            except (IndexError, TypeError):
                result = test(c, d)
                if result:
                    return True
                if result == None:
                    pass
                if result == False:
                    return False
        else:
            raise TypeError
            #print(4)
    if lengthTest:
        return True
    #print(a, b, lengthTestB)
    if lengthTestB:
        return False
    if firstLayer: print("Returning None")
results = []
index = 1
total = 0
completeList = []
for a, b in pairs:
    completeList.append(a)
    completeList.append(b)
    ##print(a, b)
    ##print(test(a, b))
    results.append(test(a, b, True))
    #print(results[-1])
    if results[-1]:
        total += index
    index += 1
#print(*results)
#print(total)

class Signal:
    def __init__(self, signal: list):
        self.signal = signal

    def __gt__(self, other):
        return (not test(self.signal, other.signal)) and (self.signal != other.signal)

    def __lt__(self, other):
        return test(self.signal, other.signal)

    def __eq__(self, *others):
        for other in others:
            if self.signal != other.signal:
                return False
        return True

testSignalA = [[2]]
testSignalB = [[6]]
completeList.append(testSignalA)
completeList.append(testSignalB)
completeList = [Signal(x) for x in completeList]
completeList.sort()
swaps = 1
while swaps > 0:
    swaps = 0
    for i in range(len(completeList)-1):
        if completeList[i + 1] < completeList[i]:
            completeList[i], completeList[i + 1] = completeList[i + 1], completeList[i]
            swaps += 1

solution = 1
for index, value in enumerate(completeList):
    ##print(index, value.signal)
    if value.signal in (testSignalA, testSignalB):
        print(index + 1)
        solution *= (index + 1)
print(solution)