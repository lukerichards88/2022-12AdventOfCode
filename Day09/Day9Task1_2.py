import timeit
def euclideanDistance(*args):
    """ n = len(args)
    Function finds ED of 2 points in n-Dimensional Space
    Point0 = (arg[0] for arg in args)
    Point1 = (arg[1] for arg in args)
    Each arg should be a 2-Tuple
    Each tuple is a pair of values on the same dimension
    Function iterates over every dimension and finds the
    distance between the two points."""
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
        # Moves self to an absolute co-ordinate
        newX, newY = newPos
        self.X = newX
        self.Y = newY
        self.visited.add((newX, newY))

    def curPos(self):  # Returns the current position of self
        return self.X, self.Y

    def move(self, vector):  # Moves self based on an (x, y) vector passed as a tuple
        dX, dY = vector
        self.X += dX
        self.Y += dY
        self.visited.add((self.X, self.Y))
        if self.F:
            # Update the follower, if exists and needs moving
            self.moveFollower()

    def moveFollower(self):  # Assesses current position of follower and moves where necessary
        sX, sY = self.curPos()
        fX, fY = self.F.curPos()
        if (sX, sY) == (fX, fY):  # F and S are now overlapping. Do not move F.
            return
        if euclideanDistance((sX, fX), (sY, fY)) in (1, 2 ** 0.5):
            # F and S are now 1 space away, U, D, L, R or diagonal. Do not move F.
            return
        if sX == fX and abs(sY - fY) == 2:
            # F and S are on the same x= line, 2 spaces apart on y=
            newY = (sY + fY) / 2  # Move F 1 space towards S
            newX = fX
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        if sY == fY and abs(sX - fX) == 2:
            newX = (sX + fX) / 2  # Same as above but on other axis
            newY = fY
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        if euclideanDistance((sX, fX), (sY, fY)) == 5 ** 0.5:   # S, F are (2,1) apart (or equiv)
            if abs(sY - fY) == 2:   # If 2 apart vertically
                newY = (sY + fY) / 2
                newX = sX
                fVector = (newX - fX, newY - fY)
                self.F.move(fVector)
                return
            if abs(sX - fX) == 2:   # If 2 apart horizontally
                newX = (sX + fX) / 2
                newY = sY
                fVector = (newX - fX, newY - fY)
                self.F.move(fVector)
                return
        if euclideanDistance((sX, fX), (sY, fY)) == 8 ** 0.5:
            # Double Diagonal. Move F to the mean of its current pos and S pos
            newX = (sX + fX) / 2
            newY = (sY + fY) / 2
            fVector = (newX - fX, newY - fY)
            self.F.move(fVector)
            return
        print(sX, sY, fX, fY)
        raise ValueError('WTF')


vectors = {     # Give U, D, L, R as unit vectors
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}
def main():
    H = Knot(hasFollower=9)     # Initialise H with 9 followers
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
if __name__ == "__main__":
    main()
