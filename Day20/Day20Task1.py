filename = 'Day20Test.txt'
filename = 'Day20Input.txt'

solutions = """2, 1, -3, 3, -2, 0, 4
1, -3, 2, 3, -2, 0, 4
1, 2, 3, -2, -3, 0, 4
1, 2, -2, -3, 0, 3, 4
1, 2, -3, 0, 3, 4, -2
1, 2, -3, 0, 3, 4, -2
1, 2, -3, 4, 0, 3, -2"""
solns = []
for line in solutions.split('\n'):
    solns.append([int(x) for x in line.split(',')])
#print(solns)
def parse(fName: str):
    with open(fName) as file:
        return tuple(int(x) for x in file.read().split('\n'))

def printNew(code, locations):
    newIndexes = {value: key for key, value in locations.items()}
    print(newIndexes.keys())
def mix(code: tuple[int, ...]):
    #print(*code)
    locations = [x for x in range(len(code))]
    count = 0
    for originalLocation, value in enumerate(code):
        currentLocation = locations.index(originalLocation)
        newLocation = currentLocation + value
        #print(f"{locations}\nvalue: {value}, currentLocation: {currentLocation}, newLocation: {newLocation}, locations: {locations}")
        if newLocation == currentLocation:
            pass
        elif newLocation % len(code) == 0:
            v = locations.pop(currentLocation)
            locations = locations + [v]
        elif newLocation < 0:
            newLocation = newLocation % len(code) - 1
            v = locations.pop(currentLocation)
            locations.insert(newLocation, v)
        elif newLocation < currentLocation:
            locations.insert(newLocation, locations.pop(currentLocation))
        elif len(code) - 1 > newLocation > currentLocation:
            locations.insert(newLocation, locations.pop(currentLocation))
        elif newLocation > len(code):
            locations.insert(newLocation % len(code) + 1, locations.pop(currentLocation))



        view = [code[x] for x in locations]
        #print(view, view==solns[count], solns[count])
        count += 1
    return tuple(code[x] for x in locations)

def main():
    # main function goes here
    code = parse(filename)
    mixed = mix(code)
    #print(mixed)
    zeroIndex = mixed.index(0)
    solution = 0
    for x in range(1, 4):
        position = x * 1000
        distance = position % len(mixed)
        index = distance + zeroIndex
        print(interim := mixed[index % len(mixed)])
        solution += interim
    print(solution)


if __name__ == "__main__":
    main()
