filename = 'Day14Test.txt'


# filename = 'Day14Input.txt'

def parseInput(filename) -> tuple:
    lines = []
    with open(filename, 'r') as file:
        newCaveLine = []
        for line in file:
            points = line.strip().split(' -> ')
            for point in points:
                a, b = point.split(',')
                newCaveLine.append((int(a), int(b)))
            lines.append(tuple(newCaveLine))
            newCaveLine = []
    return tuple(lines)


def findBlockages(paths: tuple) -> tuple:
    blockages = []
    for lines in paths:
        starts = lines[:-1]
        ends = lines[1:]
        for i, line in enumerate(zip(starts, ends)):
            Xs, Ys = (set(c[d] for c in line) for d in (0, 1))
            Xs, Ys = (tuple(c) for c in (Xs, Ys))
            match (len(Xs), len(Ys)):
                case (1, 2):
                    x = tuple(Xs)[0]
                    for y in range(min(Ys), max(Ys) + 1):
                        blockages.append((x, y))
                case (2, 1):
                    y = Ys[0]
                    for x in range(min(Xs), max(Xs) + 1):
                        blockages.append((x, y))
    return tuple(set(blockages))


class Cave:
    def __init__(self, blockages=None):
        self.blockages = blockages


def main():
    lines = parseInput(filename)
    blockedSpaces = findBlockages(lines)


if __name__ == "__main__":
    main()
