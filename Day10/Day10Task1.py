filename = 'Day10Input.txt'
actions = (None, 'noop', 'addx')
class Action:
    def __init__(self, instruction=None, value=0):
        self.remainingClicks = actions.index(instruction)
        self.addXvalue = value

    def click(self):
        self.remainingClicks -= 1
        return self.remainingClicks
class Clock:
    def __init__(self):
        self.clock = 1
        self.X = 1
        self.Action = Action()
    def spritePos(self):
        return (self.X + x - 1 for x in range(3))
    def start(self, instruction=None):
        if not instruction:
            pass
        else:
            match instruction.strip().split():
                case [noop]:
                    self.Action = Action(noop)
                case [addx, value]:
                    value = int(value)
                    self.Action = Action(addx, value=value)

    def end(self):
        self.clock += 1
        self.Action.click()
        if not self.Action.remainingClicks:
            self.X += self.Action.addXvalue

    def strength(self):
        return self.clock * self.X

class Manager:
    def __init__(self):
        self.Clock = Clock()
        self.strengths = []
        self.CRT = ""

    def receiveInstruction(self, instruction=None):
        instruction = instruction.replace('\n','')
        self.start(instruction)
        while self.Clock.Action.remainingClicks > 0:
            self.CRT += (' ','#')[(self.Clock.clock - 1) % 40 in self.Clock.spritePos()]
            self.end()
            self.start()


    def start(self, instruction=None):
        self.Clock.start(instruction)
    def end(self):
        if self.Clock.clock % 40 == 20:
            self.strengths.append(self.Clock.strength())
        self.Clock.end()

with open(filename) as file:
    line = file.readline()
    linecounter = 0
    Manager = Manager()
    while line != '':
        Manager.receiveInstruction(line)
        line = file.readline()
        linecounter += 1
S = Manager.strengths
print(sum(S))

for x in range(len(Manager.CRT)//40):
    print(Manager.CRT[40 * x:40*(x + 1)])