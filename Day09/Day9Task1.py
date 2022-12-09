def euclideanDistance(*args):
    total = 0
    for arg in args:
        a, b = arg
        d = a - b
        total += d ** 2
    return total ** 0.5


class Knot:
    def __init__(self, hasFollower=1):
        self.X = 0
        self.Y = 0
        self.numberOfFollowers = hasFollower
        self.visited = {(0, 0)}

        if hasFollower:
            self.F = Knot(hasFollower=hasFollower - 1)
        else:
            self.F = None

    def moveAbsolute(self, newPos):
        newX, newY = newPos
        self.X = newX
        self.Y = newY
        self.visited.add((newX, newY))

    def curPos(self):
        return self.X, self.Y

    def move(self, vector):
        dX, dY = vector
        self.X += dX
        self.Y += dY
        self.visited.add((self.X, self.Y))
        if self.F:
            self.moveFollower()

    def moveFollower(self):
        sX, sY = self.curPos()
        fX, fY = self.F.curPos()
        if (sX, sY) == (fX, fY):
            return
        if euclideanDistance((sX, fX), (sY, fY)) in (1, 2 ** 0.5):
            return
        if sX == fX and abs(sY - fY) == 2:
            newY = (sY + fY) / 2
            newX = fX
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        if sY == fY and abs(sX - fX) == 2:
            newX = (sX + fX) / 2
            newY = fY
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        if euclideanDistance((sX, fX), (sY, fY)) == 5 ** 0.5:
            if abs(sY - fY) == 2:
                newY = (sY + fY) / 2
                newX = sX
                fVector = (newX - fX, newY - fY)
                self.F.move(fVector)
                return
            if abs(sX - fX) == 2:
                newX = (sX + fX) / 2
                newY = sY
                fVector = (newX - fX, newY - fY)
                self.F.move(fVector)
                return
        if euclideanDistance((sX, fX), (sY, fY)) == 8 ** 0.5:
            newX = (sX + fX) / 2
            newY = (sY + fY) / 2
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        print(sX, sY, fX, fY)
        raise ValueError('WTF')


vectors = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}

H = Knot(hasFollower=9)
# filename = "Day9Test.txt"
filename = "Day9Input.txt"
with open(filename) as file:
    for line in file:
        direction, distance = [line.split()[0], int(line.split()[1])]
        for m in range(distance):
            H.move(vectors[direction])
F = H.F
visited = F.visited
print("Task 1")
print(len(visited))
print("Task 2")
for x in range(9):
    visited = len(F.visited)
    F = F.F
print(visited)