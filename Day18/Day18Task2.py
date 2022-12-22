
from Day18Task1 import *
filename = 'Day18Test.txt'
filename = 'Day18Input.txt'

class Cube:
    def __init__(self, x: int, y: int, z: int, substance: str = 'air', status: 'str'=None):
        self.x = x
        self.y = y
        self.z = z
        self.position = (x, y, z)
        self.substance = substance
        self.status = status


class SystemManager:
    def __init__(self, indexes):
        (
            (self.xMin, self.xMax),
            (self.yMin, self.yMax),
            (self.zMin, self.zMax)
        ) = self.findBoundary(indexes)
        self.indexes = indexes
        self.boundary = self.findBoundary(indexes)
        self.cubes = {}
        for x in range(self.xMin, self.xMax + 1):
            for y in range(self.yMin, self.yMax + 1):
                for z in range(self.zMin, self.zMax + 1):
                    if x in self.boundary[0] or y in self.boundary[1] or z in self.boundary[2]:
                        self.cubes.setdefault(x, {}).setdefault(y, {}).setdefault(z, Cube(x, y, z, 'air', 'outside'))
                    self.cubes.setdefault(x, {}).setdefault(y, {}).setdefault(z, Cube(x, y, z, 'air'))

    def findBoundary(self, indexes):
        xy, yz, xz = indexes
        minX = min(*xy.keys())
        maxX = max(*xy.keys())
        minY = min(*yz.keys())
        maxY = max(*yz.keys())
        yDicts = tuple(xy.values())
        zValues = set()
        for yDict in yDicts:
            zValues.update(*yDict.values())
        minZ = min(zValues)
        maxZ = max(zValues)
        return (
            (minX-1, maxX+1),
            (minY-1, maxY+1),
            (minZ-1, maxZ+1)
        )

    def addCube(self, x, y, z, substance, neighbours):
        status = (None, 'encased')[neighbours == 6]
        self.cubes[x][y][z] = Cube(x, y, z, substance, status)
    def findCube(self, x, y, z):
        return self.cubes[x][y][z]

    def airNeighbours(self, x, y, z):
        xOptions = []
        yOptions = []
        zOptions = []
        cube = x, y, z
        if x - 1 >= self.xMin: xOptions.append(x - 1)
        if x + 1 <= self.xMax: xOptions.append(x + 1)
        if y - 1 >= self.yMin: yOptions.append(y - 1)
        if y + 1 <= self.yMax: yOptions.append(y + 1)
        if z - 1 >= self.zMin: zOptions.append(z - 1)
        if z + 1 <= self.zMax: zOptions.append(z + 1)
        options = []
        for xOpt in xOptions:
            options.append((xOpt, y, z))
        for yOpt in yOptions:
            options.append((x,yOpt, z))
        for zOpt in zOptions:
            options.append((x, y, zOpt))
        outputOptions = []
        for option in options:
            if self.findCube(*option).substance == 'air' and self.findCube(*option).status != 'addedtoqueue':
                outputOptions.append(option)
        return outputOptions
        

    def breadthSearch(self):
        totalContactFaces = 0
        (x, _), (y, _), (z, _) = self.boundary
        queue = self.airNeighbours(x, y, z)
        nextCube = x, y, z
        while len(queue) > 0:
            for cube in self.airNeighbours(*nextCube):
                if self.findCube(*cube).status != "addedtoqueue":
                    queue.append(cube)
                    self.findCube(*cube).status = "addedtoqueue"
            totalContactFaces += CheckForNeighbours(nextCube, self.indexes)

            nextCube = queue.pop(0)
        return totalContactFaces

def main():
    cubes = parse(filename)
    indexes = indexCubes(cubes)
    xy, yz, xz = indexes
    yDicts = tuple(xy.values())
    zValues = set()
    for yDict in yDicts:
        zValues.update(*yDict.values())
    system = SystemManager(indexes)
    for cube in cubes:
        system.addCube(*cube, 'lava', CheckForNeighbours(cube, indexes))
    #print(system.breadthSearch())

if __name__ == "__main__":
    from timeit import timeit
    main()
    setup = "from Day18Task1 import parse, CheckForNeighbours, indexCubes; from __main__ import main; filename='Day18Input.txt'"
    time = timeit('main()', setup=setup, number=1000)
    print("Average time per iteration:", time, "ms.")
