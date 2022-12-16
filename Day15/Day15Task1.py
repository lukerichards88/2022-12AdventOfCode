#from itertools import product
#filename = 'Day15Test.txt'


filename = 'Day15Input.txt'
def manhatten(p1: tuple, p2: tuple) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def parse(filename: str) -> tuple:
    sensors = []
    with open(filename) as file:
        for line in file:
            tokens = line.replace(',', '').replace(':', '').split()
            coOrds = (tokens[x] for x in [2, 3, -2, -1])
            coOrds = tuple(int(x.split('=')[-1]) for x in coOrds)
            sensor = tuple(coOrds[x] for x in (0, 1))
            beacon = tuple(coOrds[x] for x in (2, 3))
            sensors.append((sensor, beacon))
    return tuple(sensors)


def getDistances(sensors: tuple) -> dict:
    distances = {}
    for sensor in sensors:
        sensorLocation = sensor[0]
        manhattenDistance = manhatten(*sensor)
        distances[sensorLocation] = manhattenDistance
    return distances

def Overlaps(t: tuple, u: tuple) -> bool:
    tMin, tMax = t
    uMin, uMax = u
    if tMax < uMin:
        return False
    if tMin > uMax:
        return False
    return True
def getBlocked(distances: dict, y: int, xRangeToCheck=None) -> tuple:
    sensors = distances.keys()
    blocked = []
    for sensor in sensors:
        distance = distances[sensor]
        SensorEmptySpaceRange = GetEmptySpaceRange(sensor, distance, y)
        if xRangeToCheck and Overlaps(SensorEmptySpaceRange, xRangeToCheck):
            blocked.append(SensorEmptySpaceRange)
        elif xRangeToCheck is None:
            blocked.append(SensorEmptySpaceRange)
    return tuple(blocked)


def GetEmptySpaceRange(sensor: tuple, distance: int, y: int) -> tuple:
    sensorX, sensorY = sensor
    yMin, yMax = (sensorY - distance, sensorY + distance)
    if yMin <= y <= yMax:
        dY = abs(y - sensorY)
        dX = distance - dY
        xMin = sensorX - dX
        xMax = sensorX + dX
        return (xMin, xMax)
    return (sensorX, sensorX)


def getBeacons(sensors):
    beacons = {}
    for sensor in sensors:
        _, beacon = sensor
        beaconX, beaconY = beacon
        beacons.setdefault(beaconY, set()).add(beaconX)
    return beacons

def intersection(t: tuple, u: tuple):
    if not Overlaps(t, u):
        return None
    if t == u:
        return u
    tRange = t[1] - t[0]
    uRange = u[1] - u[0]
    if t[0] > u[0] and t[1] < u[1]:
        return t
    if t[0] < u[0] and t[1] > u[1]:
        return u
    return (max(t[0], u[0]), min(t[1], u[1]))
def getNoBeaconNumber(yBlockedRanges: tuple, beacons: dict, y: int, xRangeToCheck=None) -> int:
    if xRangeToCheck is not None:
        xAllowedMin, xAllowedMax = xRangeToCheck
    else:
        xAllowedMin, xAllowedMax = (float('-inf'), float('inf'))
    yBlocked = set()
    for yBlockedRange in yBlockedRanges:
        xMin, xMax = yBlockedRange
        if Overlaps(yBlockedRange, (xAllowedMin, xAllowedMax)):
            xMin, xMax = intersection(yBlockedRange, (xAllowedMin, xAllowedMax))
            print(xMin, xMax)
            yBlocked.update((x for x in range(xMin, xMax + 1)))
    yBeacons = list(beacons.get(y, set()))
    yBeaconsToRemove = 0
    for index, beacon in enumerate(yBeacons):
        if beacon in yBlocked:
            yBeaconsToRemove += 1
    yBlocked = len(yBlocked)
    return max((yBlocked - yBeaconsToRemove), 0)
def Union(t, u):
    return (min(t[0], u[0]), max(t[1],u[1]))
def findAvailableSpaces(yBlockedRanges: tuple, beacons: dict, y: int, xRangeToCheck=None) -> int:
    xRangeToCheck = (0, 3156346)
    currentrange = False
    rangesAdded = []
    twoCount = 0
    diff = 0
    while len(yBlockedRanges) - len(rangesAdded) > 1:
        for yBlockedRange in yBlockedRanges:
            if not currentrange:
                currentrange = yBlockedRange
            if Overlaps(currentrange, yBlockedRange) and yBlockedRange not in rangesAdded:
                currentrange = Union(currentrange, yBlockedRange)
                rangesAdded.append(yBlockedRange)
                break
            if yBlockedRange[0] == currentrange[1] + 2:
                solution = 4000000 * (yBlockedRange[0] - 1) + y
        lasdiff = diff
        diff = len(yBlockedRanges) - len(rangesAdded)
        if diff == lasdiff:
            twoCount += 1
        if twoCount == 10:
            print(f"The solution is {solution}")
            return True
    for yBlockedRange in yBlockedRanges:
        if yBlockedRange not in rangesAdded:
            return not Overlaps(currentrange, yBlockedRange)

def main():
    y = 2000000
    sensors = parse(filename)
    beacons = getBeacons(sensors)
    distances = getDistances(sensors)
    blockedRanges = getBlocked(distances, y)
    print(getNoBeaconNumber(blockedRanges, beacons, y))


if __name__ == "__main__":
    main()
