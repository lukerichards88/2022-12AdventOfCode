class File:

    def __init__(self, fName, fSize):
        self.name = fName
        self.fileSize = fSize
        self.isDir = False

    def size(self):
        return int(self.fileSize)


class Directory:

    def __init__(self, fName):
        self.name = fName
        self.contents = {}
        self.isDir = True

    def size(self):
        s = 0
        for fName, item in self.contents.items():
            s += item.size()
        return s

    def add(self, item):
        if item.name in self.contents.keys():
            return
        self.contents[item.name] = item
        return

    def access(self, itemName):
        return self.contents[itemName]

    def hasDirs(self):
        for item in self.contents:
            if isinstance(item, Directory):
                return True
        return False

    def listDirs(self):
        listOfDirs = []
        for iName, item in self.contents.items():
            if item.isDir:
                listOfDirs.append(item)
        return listOfDirs

    def scanDirs(self):
        yield self.name, self.size()
        listOfDirs = self.listDirs()
        for d in listOfDirs:
            for iteration in d.scanDirs():
                yield iteration


class Reader:

    def __init__(self, filename):
        self.filename = filename
        self.currentDir = None
        self.root = Directory('/')

    @staticmethod
    def findFiles(sourceFile, folder):
        notStarted = True
        lastPos = sourceFile.tell()
        line = sourceFile.readline()
        while line != '':
            if notStarted and line[0] == "$":
                notStarted = False
            elif line[0] == "$":
                sourceFile.seek(lastPos)
                return sourceFile
            elif line[:3] == "dir":
                folder.add(Directory(line.replace('\n', '').split(' ')[-1]))
            else:
                fSize, filename = line.replace('\n', '').split(' ')
                folder.add(File(filename, int(fSize)))
            notStarted = False
            lastPos = sourceFile.tell()
            line = sourceFile.readline()
        return sourceFile

    def readDirs(self):
        with open(self.filename) as file:
            lastPos = file.tell()
            line = file.readline()
            while line != '':
                if line[:4] == "$ cd":
                    instructions = line.replace('\n', '').split(' ')
                    newDir = instructions[2]
                    if newDir == "/":
                        self.currentDir = []
                    else:
                        newDirs = newDir.split('/')
                        for d in newDirs:
                            if d == "..":
                                self.currentDir = self.currentDir[:-1]
                            else:
                                self.currentDir.append(d)
                    workingDirectory = self.root
                    for d in self.currentDir:
                        workingDirectory.add(Directory(d))
                        workingDirectory = workingDirectory.access(d)
                elif line[:4] == "$ ls":
                    file.seek(lastPos)
                    file = self.findFiles(file, workingDirectory)
                lastPos = file.tell()
                line = file.readline()


r = Reader('Day7Input.txt')
r.readDirs()
totalUsed = totalFree = minimumDeletion = 0
smallestFound = 10 ** 20
for name, size in r.root.scanDirs():
    if name == "/":
        totalUsed = size
        totalFree = 70000000 - size
        minimumDeletion = 30000000 - totalFree
    if size == minimumDeletion:
        print(size)
        break
    elif minimumDeletion < size < smallestFound:
        smallestFound = size
print("Done")
print(minimumDeletion, smallestFound)
