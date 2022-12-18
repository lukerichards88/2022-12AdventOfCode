# filename = 'Day18TestTiny.txt'
# filename = 'Day18Test.txt'
filename = 'Day18Input.txt'


# xyz
# yzx
# zxy

# So...
# xy, yz, zx
def parse(fName: str, verbose: bool = False) -> tuple[tuple[int, ...]]:
    with open(fName, 'r') as file:
        cubes = set()
        for line in file:
            cube = line.strip().split(',')
            if verbose:
                print(cube)
            cubes.add(tuple(int(c) for c in cube))
    return tuple(cubes)


def indexCubes(cubes: tuple[tuple[int, ...]]) -> tuple[dict, ...]:
    xy = {}
    yz = {}
    xz = {}
    for cube in cubes:
        x, y, z = cube
        xy.setdefault(x, {}).setdefault(y, set()).add(z)
        yz.setdefault(y, {}).setdefault(z, set()).add(x)
        xz.setdefault(x, {}).setdefault(z, set()).add(y)

    return xy, yz, xz


def CheckForNeighbours(cube: tuple[int, ...], indexes: tuple[dict, ...]) -> int:
    x, y, z = cube
    xy, yz, xz = indexes
    neighbourCount = 0
    for zN in (z + 1, z - 1):
        try:
            neighbourCount += zN in xy[x][y]
        except KeyError:
            pass
    for xN in (x + 1, x - 1):
        try:
            neighbourCount += xN in yz[y][z]
        except KeyError:
            pass
    for yN in (y + 1, y - 1):
        try:
            neighbourCount += yN in xz[x][z]
        except KeyError:
            pass
    return neighbourCount


def FindTotalNeighbours(cubes: tuple[tuple[int, ...], ...], indexes: tuple[dict, ...]) -> int:
    TotalNeighbours = 0
    for cube in cubes:
        TotalNeighbours += CheckForNeighbours(cube, indexes)
    return TotalNeighbours


def main():
    cubes = parse(filename)
    totalCubes = len(cubes)
    indexes = indexCubes(cubes)
    print(6 * totalCubes - FindTotalNeighbours(cubes, indexes))


if __name__ == "__main__":
    main()
