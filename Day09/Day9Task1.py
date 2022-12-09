xDirections = {'L': -1, 'R': 1}
yDirections = {'U': 1, 'D': -1}
import itertools
def XNOR(a, b):
    return not(a ^ b)

def euclideanDistance(dX, dY):
    return (dX ** 2 + dY ** 2) ** 0.5
class Knot:

    def __init__(self, x, y, name="H", hasFollower=True, followerx=None, followery=None):
        self.xPos = x
        self.yPos = y
        self.name = name
        if hasFollower:
            if followerx is None:
                followerx = x
                followery = y
            self.follower = Knot(followerx, followery, name="T", hasFollower=False)
        else:
            self.followerx = self.followery = self.follower = None
        self.visited = {(self.xPos, self.yPos)}

    def move(self, direction):
        self.xPos += xDirections.get(direction, 0)
        self.yPos += yDirections.get(direction, 0)
        if self.follower is not None:
            self.moveFollowerNoArg()

    def moveFollowerNoArg(self):
        selfX, selfY = self.curLoc()
        follX, follY = self.follower.curLoc()
        dX, dY = (selfX - follX), (selfY - follY)
        distance = euclideanDistance(dX, dY)
        if distance <= 2 ** 0.5:
            return
        else:
            directions = (-1,0,1)
            vectors = set(itertools.permutations(directions, 2))
            mindistance = 100
            for vector in vectors:
                vX, vY = vector
                newFX = self.xPos + vX
                newFY = self.yPos + vY
                fDX = follX - newFX
                fDY = follY - newFY
                distance = euclideanDistance(fDX, fDY)
                if distance < mindistance:
                    mindistance = distance
                    candidateX, candidateY = newFX, newFY
            self.follower.moveAbsolute(candidateX, candidateY)


    def moveAbsolute(self, x, y):
        self.xPos, self.yPos = x, y
        self.visited.add((x, y))

    def curLoc(self):
        return (self.xPos, self.yPos)

    def followerMoveVector(self, thisDirection: str):
        this, follower = (self.curLoc(), self.follower.curLoc())
        thisX, thisY = this
        follX, follY = follower
        if this == follower:
            return (0,0)
        if thisDirection in ('U', 'D'):
            if thisX == follX:
                thisIsAbove = (thisY > follY)
                moveUp = (thisDirection == 'U')
                move = XNOR(thisIsAbove, moveUp)
                if not move:
                    return (0,0)
                return (0,yDirections[thisDirection])
            else:
                if thisY == follY:
                    return (0,0)
                xMove = thisX - follX
                yMove = yDirections[thisDirection]
                return (xMove, yMove)
        else:
            if thisY == follY:
                thisIsRight = (thisX > follX)
                moveRight = (thisDirection == 'R')
                move = XNOR(thisIsRight, moveRight)
                if not move:
                    return (0,0)
                return (xDirections[thisDirection], 0)
            else:
                if thisX == follX:
                    return (0,0)
                yMove = thisY - follY
                xMove = xDirections[thisDirection]
                return (xMove, yMove)

    def moveString(self, line: str):
        direction, distance = line.replace('\n','').split(' ')
        distance = int(distance)
        for movement in range(distance):
            self.moveFollower(direction)
            self.xPos += xDirections.get(direction, 0)
            self.yPos += yDirections.get(direction, 0)
            #print("Current Move:",direction)
            #print("H pos", self.curLoc())
            #print("T pos", self.follower.curLoc())
            xA, yA = self.curLoc()
            xB, yB = self.follower.curLoc()
            dX = xA - xB
            dY = yA - yB
            eucLideanDistance = (dX ** 2 + dY ** 2) ** 0.5
            closeEnough = (eucLideanDistance < ((2 ** 0.5) + 0.001))
            self.visited.add((self.xPos, self.yPos))
            #print(eucLideanDistance, closeEnough)
            #approved = input("Check: ") == ""
            if not closeEnough:
                print("ERROR")
                break

    def moveVector(self, direction: tuple):
        xMove, yMove = direction
        self.xPos += xMove
        self.yPos += yMove
        self.visited.add((self.xPos, self.yPos))

    def moveFollower(self, directionString):
        vector = self.followerMoveVector(directionString)
        self.follower.moveVector(vector)

H = Knot(0,0)
filename = 'Day9Input.txt'
with open(filename) as file:
    for line in file:
        direction, number = line.split(' ')
        for move in range(int(number)):
            H.move(direction)

print(len(H.follower.visited))