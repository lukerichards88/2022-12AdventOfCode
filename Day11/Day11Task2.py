from math import lcm
filename = 'Day11Input.txt'

class Monkey:
    def __init__(self, items: list, operation: str, test: int, ifTrue: int, ifFalse: int):
        self.Items = items
        self.Operation = self.Parse(operation)
        self.TestDividend = int(test)
        self.IfTrue = ifTrue
        self.IfFalse = ifFalse
        self.Recipients = (ifFalse, ifTrue)
        self.InspectionCount = 0

    # noinspection PyTypeChecker
    @staticmethod
    def Parse(operation: str):
        terms = operation.split()
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
        self.InspectionCount += 1
        return self.Throw(worryScore)

    def Throw(self, worryScore):
        recipient = self.Recipients[self.Test(worryScore)]
        return recipient, worryScore


class Manager:
    def __init__(self, monkeyList: list):
        self.Monkeys = monkeyList
        test = []
        for monkey in monkeyList:
            test.append(monkey.TestDividend)
        self.modulus = lcm(*test)

    def newRound(self):
        for MonkeyNum, MonkeyObj in enumerate(self.Monkeys):
            while len(MonkeyObj.Items) > 0:
                recipient, worryScore = MonkeyObj.Inspect()
                worryScore = worryScore % self.modulus
                recipient = self.Monkeys[recipient]
                recipient.Items.append(worryScore)


class Parser:
    def __init__(self, fName):
        self.Monkeys = []
        self.filename = fName

    def readFile(self):
        with open(self.filename) as file:
            for line in file:
                lineList = line.strip().replace('\n', '').split()
                match lineList:
                    case []:
                        newMonkey = Monkey(items, operation, test, ifTrue, ifFalse)
                        self.Monkeys.append(newMonkey)
                    case ['Starting', 'items:', *values]:
                        items = [int(itm.replace(',', '')) for itm in values]
                    case ['Operation:', *terms]:
                        terms = terms[-3:]
                        match terms:
                            case ['old', '*', 'old']:
                                operation = '^ 2'
                            case ['old', *terms]:
                                operation = ' '.join(terms[-2:])
                    case ['Test:', *terms]:
                        test = int(terms[-1])
                    case ['If', 'true:', *terms]:
                        ifTrue = int(terms[-1])
                    case ['If', 'false:', *terms]:
                        ifFalse = int(terms[-1])
            newMonkey = Monkey(items, operation, test, ifTrue, ifFalse)
            self.Monkeys.append(newMonkey)

def getMonkeys():
    p = Parser(filename)
    p.readFile()
    monkeys = p.Monkeys
    return monkeys

def playGame(manager, iterations):
    for i in range(iterations):
        manager.newRound()
    return manager

def printAnswer(manager):
    inspectionCounts = [0, 0]
    for m in manager.Monkeys:
        inspectionCounts.append(m.InspectionCount)
    topTwo = sorted(inspectionCounts)[-2:]
    total = 1
    for c in topTwo:
        total *= c
    print(total)
def main():
    m = Manager(getMonkeys())
    m = playGame(m, 10000)
    printAnswer(m)

if __name__ == '__main__':
    main()

