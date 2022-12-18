from Day16Task1 import *

filename = 'Day16Test.txt'
filename = 'Day16Input.txt'


class Status:
    def __init__(self):
        self.ReadyToUnlock = "ReadyToUnlock"
        self.NeedsNewLocation = "NeedsNewLocation"
        self.EnRoute = "EnRoute"
        self.Unlocking = "Unlocking"
        self.WaitingToLeave = "WaitingToLeave"
        self.GotLocationWaitingForNextSecond = "GotLocationWaitingForNextSecond"
        self.Arrived = "Arrived"
        self.Finished = "Finished"


class Manager:
    def __init__(self, NodesToVisit, Distances, flowRates):
        self.elephant = Mover('AA', 'elephant')
        self.person = Mover('AA', 'person')
        self.remainingSeconds = 26
        self.movers: tuple[Mover, ...] = (self.elephant, self.person)
        self.unvisitedNodes: list = list(NodesToVisit)
        self.distances = Distances
        self.flows = flowRates
        self.status = Status()
        self.valves: Valves = Valves()
        self.statusesHad = set()

    def unlockValves(self):
        for mover in self.movers:
            if mover.status == self.status.ReadyToUnlock:
                mover.status = self.status.Unlocking
                valveName = mover.currentLocation
                valveValue = self.flows[valveName]
                self.valves.CurrentFlowRate += valveValue
                mover.status = self.status.NeedsNewLocation

    def SetNewDestinations(self):
        status = self.status
        for mover in self.movers:
            if mover.status == status.NeedsNewLocation:
                PossibleLocations = self.unvisitedNodes
                LocationScores = tuple((10 * random()) ** 2 * self.flows[location] / self.distances[mover.currentLocation][location] for location in PossibleLocations)
                try:
                    WinningIndex = LocationScores.index(max(LocationScores))
                except ValueError as e:
                    mover.status = status.Finished
                    WinningIndex = 0
                if mover.status != status.Finished:
                    NextDestination = PossibleLocations[WinningIndex]
                    mover.nextLocation = NextDestination
                    if mover.currentLocation != 'AA':
                        mover.status = status.WaitingToLeave
                    else:
                        mover.status = status.WaitingToLeave
                    self.unvisitedNodes.remove(mover.nextLocation)

    def MoveOneStep(self):
        status = self.status
        for mover in self.movers:
            if mover.status == status.WaitingToLeave:
                mover.RemainingTravel = self.distances[mover.currentLocation][mover.nextLocation]
                mover.status = status.EnRoute
            if mover.status == status.EnRoute:
                mover.RemainingTravel -= 1
                mover.status = (status.EnRoute, status.Arrived)[mover.RemainingTravel == 0]

    def StartNewSecond(self):
        status = self.status
        self.remainingSeconds -= 1
        for mover in self.movers:
            if mover.status == status.Arrived:
                mover.status = status.ReadyToUnlock
                mover.currentLocation = mover.nextLocation
            elif mover.status == status.GotLocationWaitingForNextSecond:
                mover.status = status.WaitingToLeave

    def ReleasePressure(self):
        self.valves.PressureReleased += self.valves.CurrentFlowRate

    def Score(self):
        return self.valves.PressureReleased, self.valves.CurrentFlowRate


class Valves:
    def __init__(self):
        self.CurrentFlowRate = 0
        self.PressureReleased = 0

class Mover:
    ReadyToUnlock = "ReadyToUnlock"
    NeedsNewLocation = "NeedsNewLocation"
    EnRoute = "EnRoute"
    Unlocking = "Unlocking"
    WaitingToLeave = "WaitingToLeave"
    GotLocationWaitingForNextSecond = "GotLocationWaitingForNextSecond"
    Arrived = "Arrived"

    def __init__(self, startLocation, name=None):
        self.currentLocation = startLocation
        self.nextLocation = None
        self.name = name
        self.status = self.NeedsNewLocation


def RunInfiniteTests(distances, flowRates):
    bestScore = -1
    epoch = 0
    while True:
        if epoch % 10 ** 6 == 0:
            print(f"Current best is {bestScore}. Epoch {epoch} starting...")
        NodesToVisit = (node for node in distances.keys() if node != 'AA')
        Distances = distances.copy()
        flows = flowRates.copy()
        score = 0
        manager = Manager(NodesToVisit, Distances, flows)
        while manager.remainingSeconds > 0:
            manager.StartNewSecond()
            manager.ReleasePressure()
            score = manager.Score()
            manager.SetNewDestinations()
            manager.MoveOneStep()
            manager.unlockValves()
            # End of epoch 26 loop

        if score[0] > bestScore:
            print("**** Epoch {}: {}".format(epoch, score))
            bestScore = score[0]
        epoch += 1
        # end of while True loop


def main():
    graph, flowRates = parse(filename)
    distances = FW(graph)
    RunInfiniteTests(distances, flowRates)


if __name__ == "__main__":
    main()
