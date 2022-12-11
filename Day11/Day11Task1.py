

class Monkey:
    def __init__(self, items: list, operation: str, test: int, ifTrue: int, ifFalse: int):
        self.Items = items
        self.Operation = self.Parse(operation)
        self.TestDividend = int(test)
        self.IfTrue = ifTrue
        self.IfFalse = ifFalse
        self.Recipients = (ifFalse, ifTrue)
        self.InspectionCount = 0

    def Parse(self, operation: str):
        terms = operation.split()
        print(terms)
        terms[-1] = int(terms[-1])
        match terms:
            case ['+', value]:
                def function(worryScore: int):
                    return worryScore + value
                return function

            case ['*', value]:
                def function(worryScore: int):
                    return worryScore * value
                return function

            case ['^', value]:
                def function(worryScore: int):
                    return worryScore ** value
                return function
    def Test(self, worryScore):
        return worryScore % self.TestDividend == 0
    def Inspect(self):
        worryScore = self.Items.pop(0)
        worryScore = self.Operation(worryScore)
        worryScore = worryScore // 3
        self.InspectionCount += 1
        return self.Throw(worryScore)

    def Throw(self, worryScore):
        recipient = self.Recipients[self.Test(worryScore)]
        return recipient, worryScore



class Manager:
    def __init__(self, monkeys: list):
        self.Monkeys = monkeys

    def newRound(self):
        for MonkeyNum, Monkey in enumerate(self.Monkeys):
            while len(Monkey.Items) > 0:
                recipient, worryScore = Monkey.Inspect()
                recipient = self.Monkeys[recipient]
                recipient.Items.append(worryScore)

class Parser:
    def __init__(self, filename):
        self.Monkeys = []
        self.filename = filename
    def readFile(self):
        with open(self.filename) as file:
            for line in file:
                lineList = line.strip().replace('\n','').split()
                print(lineList)
                match lineList:
                    case []:
                        print(1)
                        newMonkey = Monkey(items, operation, test, ifTrue, ifFalse)
                        self.Monkeys.append(newMonkey)
                    case ['Starting', 'items:', *values]:
                        print(2)
                        items = [int(x.replace(',','')) for x in values]
                    case ['Operation:', *terms]:
                        print(3)
                        terms = terms[-3:]
                        print("terms:",terms)
                        match terms:
                            case ['old', '*', 'old']:
                                operation = '^ 2'
                            case ['old', *terms]:
                                operation = ' '.join(terms[-2:])
                    case ['Test:', *terms]:
                        print(4)
                        test = int(terms[-1])
                    case ['If', 'true:', *terms]:
                        print(5)
                        ifTrue = int(terms[-1])
                    case ['If', 'false:', *terms]:
                        print(6)
                        ifFalse = int(terms[-1])
            newMonkey = Monkey(items, operation, test, ifTrue, ifFalse)
            self.Monkeys.append(newMonkey)

filename = 'Day11Input.txt'
p = Parser(filename)
p.readFile()
monkeys = p.Monkeys
m = Manager(monkeys)
print("Printing Monkeys")
print(m.Monkeys)
for round in range(20):
    m.newRound()
inspectionCounts = [0,0]
for x in m.Monkeys:
    print(x)
    print(x.InspectionCount)
    inspectionCounts.append(x.InspectionCount)
    print(x.Items)
topTwo = sorted(inspectionCounts)[-2:]
total = 1
for c in topTwo:
    total *= c
print(total)