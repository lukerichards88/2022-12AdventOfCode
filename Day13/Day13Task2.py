class Signal:
    def __init__(self, s):
        if isinstance(s, list):
            self.signal = s
        else:
            self.signal = [s]
    @staticmethod
    def test(a, b):
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
            aLonger = (len(a) > len(b))
            bLonger = (len(b) > len(a))
            for pair in zip(a, b):
                match pair:
                    case ([*c], [*d]):
                        result = Signal.test(list(c), list(d))
                        if result != None:
                            return result
                    case (c, [*d]):
                        result = Signal.test(list(c), d)
                        if result != None:
                            return result
                    case ([*c], d):
                        result = Signal.test(c, list(d))
                        if result != None:
                            return result
                    case (c, d):
                        if c < d:
                            return True
            if bLonger:
                return True
            if aLonger:
                print(a, b)
                return False

    def __lt__(self, *others):
        first = self.signal
        for other in others:
            second = other.signal
            print(first, second)
            if not Signal.test(a=first, b=second):
                return False
        return True

    def __eq__(self, *others):
        a = self.signal
        for other in others:
            b = other.signal
            if not (a == b):
                return False
        return True

    def __gt__(self, *others):
        a = self.signal
        for other in others:
            b = other.signal
            l = Signal.test(a, b)
            e = (a == b)
            r = (l or e)
            return not r











with open('Day13Test.txt') as file:
    filestring = ""
    for line in file:
        filestring += line
file = filestring.split('\n\n')
output = [[line.split('\n')[0], line.split('\n')[1]] for line in file]
pairs = []
A = None
B = None
for a, b in output:
    strA = f"A = Signal({a})"
    strB = f"B = Signal({b})"
    exec(strA)
    exec(strB)
    pairs.append((A, B))
for x, y in pairs:
    print(x < y)