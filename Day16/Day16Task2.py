from Day16Task1 import *

# filename = 'Day16Test.txt'
filename = 'Day16Input.txt'


class Valves:
    def __init__(self, flowRates, distances):
        self.valveNames = tuple(flowRates.keys())
        self.unvisited = {valve: True for valve in flowRates.keys() if flowRates[valve] != 0}
        self.flowRates = flowRates
        self.distances = distances
        self.currentFlow = 0
        self.totalPressure = 0

    def openValve(self, valve: str):
        valveFlowRate = self.flowRates[valve]
        self.currentFlow += valveFlowRate


class ValveTurner:
    def __init__(self, start, distances):
        self.currentPosition = start
        self.distances = distances
        self.moving = False
        self.stepsLeft = 0
        self.opening = False
        self.destination = None

    def move(self, destination=None, valves=None):
        #self.opening = False
        if destination is not None:
            self.destination = destination
            self.stepsLeft = valves.distances[self.currentPosition][destination]
            del valves.unvisited[destination]
            print(valves.unvisited)
            #del valves.distances[destination]
            #for valveName, neighbours in valves.distances.items():
            #    del valves.distances[valveName][destination]
        self.stepsLeft -= 1
        if self.stepsLeft == 0:
            self.currentPosition = self.destination
            self.moving = False
        return valves

    def open(self):
        if self.moving:
            raise AttributeError("Cannot open valve while on the move.")
        self.opening = True


def runInfOptimisedTestsWithElephant(timeallowed, distancesOriginal, flowRatesOriginal):
    bestScore = float('-inf')
    epoch = 0
    while True:
        flowRates = flowRatesOriginal.copy()
        distances = distancesOriginal.copy()
        valves: Valves = Valves(flowRates, distances)
        Me: ValveTurner = ValveTurner('AA', distances)
        El: ValveTurner = ValveTurner('AA', distances)
        timeRemaining = timeallowed
        while timeRemaining > 0:
            valves.totalPressure += valves.currentFlow
            print(valves.totalPressure)
            for turner in (Me, El):
                #print(turner.opening)
                if turner.opening:
                    print("opening: ",turner.currentPosition)
                    valves.openValve(turner.currentPosition)
                    turner.opening = False
                elif turner.moving:
                    turner.move()
                else:
                    nextOptions = tuple(option for option in valves.unvisited.keys())
                    optionScores = tuple(random() for _ in nextOptions)
                    winningIndex = optionScores.index(max(optionScores))
                    nextDestination = nextOptions[winningIndex]
                    turner.open()
                    valves = turner.move(nextDestination, valves)
            timeRemaining -= 1
        if valves.totalPressure > bestScore:
            print("***", epoch, valves.totalPressure)
            bestScore = valves.totalPressure
        epoch += 1


def main():
    graph, flowRates = parse(filename)
    distances = FW(graph)


if __name__ == "__main__":
    main()
