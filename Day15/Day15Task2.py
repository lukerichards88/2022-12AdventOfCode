filename = 'Day15Test.txt'
# filename = 'Day15Input.txt'
from Day15Task1 import *

def main():
    OrdMin = 0
    OrdMax = 4000000
    xRangeToCheck = (OrdMin, OrdMax)
    sensors = parse(filename)
    beacons = getBeacons(sensors)
    distances = getDistances(sensors)
    for y in range(OrdMin, OrdMax + 1):
        blockedRanges = getBlocked(distances, y, xRangeToCheck)
        if findAvailableSpaces(blockedRanges, beacons, y, xRangeToCheck):
            break
        if y % 40000 == 0:
            print(y, f"{100 * y/OrdMax}%")




if __name__ == "__main__":
    main()
