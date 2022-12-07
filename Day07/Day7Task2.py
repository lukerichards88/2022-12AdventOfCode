class File:
    # An object representing a non-directory file.
    # Constructed really to only hold its name and size

    def __init__(self, fName, fSize):
        self.name = fName
        self.fileSize = fSize
        self.isDir = False # for checking later

    def size(self):
        return int(self.fileSize) # self.fileSize might be saved as a string from parsing text file


class Directory:
    # An object representing a directory
    # Can contain other objects.
    # Strictly, as written, the other objects can be of any type
    # However in practice only Directories and Files should be stored

    def __init__(self, fName):
        self.name = fName
        self.contents = {} # Use name as key and object (Directory or File) as value
        self.isDir = True

    def size(self):
        s = 0 # Initialise size counter
        for fName, item in self.contents.items(): # Iterate through all items within directory
            s += item.size()    # add the size of each item to the counter.
                                # NB If the object is a directory, this call will iterate over
                                # the new directory using its own method recursively.
                                # If the object is a file, the mirror method will simply return
                                # its size attribute.
        return s

    def add(self, item):
        if item.name in self.contents.keys():
            return # Do nothing if the item already exists. Could be expanded in future to prompt
        self.contents[item.name] = item # Adds the item to the contents of the current directory.
        return

    def access(self, itemName):
        return self.contents[itemName] # Allows the user to access individual objects in the directory

    def hasDirs(self): # Checks to see if the current directory has sub-directories. Returns True if so. 
        for item in self.contents:
            if isinstance(item, Directory): # If an item in the directory is found to be a Directory, return True
                return True
        return False

    def listDirs(self):         # Create a list containing all directory objects from the filesystem, 
                                # including within subdirectories 
        listOfDirs = []
        for iName, item in self.contents.items():
            if item.isDir:      # if the item itself is a directory, then call this function recursively 
                                # onto that directory itself
                listOfDirs.append(item)
        return listOfDirs

    def scanDirs(self):     # a generator to produce all of the directories and their sizes, which can be 
                            # iterated over
        yield self.name, self.size()
        listOfDirs = self.listDirs()
        for d in listOfDirs:    # recursively call this generator on each sub-directory and yield the  
                                # result back to the caller
            for iteration in d.scanDirs():
                yield iteration


class Reader:
    # Reads an input file, parses all of the lines from a terminal output and reconstructs the filesystem from 
    # available information. 
    # Is able to read directories within the filesystem, create them as Directory objects using the class
    # above and then populate these directories with files also found. 

    def __init__(self, filename):
        self.filename = filename
        self.currentDir = None
        self.root = Directory('/') #create the root directory using the class above

    @staticmethod
    def findFiles(sourceFile, folder):  # sourceFile is a file object, created with open()
                                        # folder is an instance of the Directory class
        notStarted = True               # used to skip the first line, if passed
        lastPos = sourceFile.tell()     # lastPos and .readline() used over for line in file
        line = sourceFile.readline()    # because need to rewind back when returning file object
        while line != '':
            if notStarted and line[0] == "$":   # check haven't been given file 1 line too early
                notStarted = False              # Next time a $ appears, it's the end of the ls call
            elif line[0] == "$":                # Should pass when not notStarted
                sourceFile.seek(lastPos)        # Rewind back to the last line ready to pass back
                return sourceFile               # Pass file object back to caller
            elif line[:3] == "dir":             # If ls returns a directory
                folder.add(Directory(line.replace('\n', '').split(' ')[-1]))    # Create new Directory and
                                                                                # add it to the current Directory
            else:                               # All remaining cases should be File instances
                fSize, filename = line.replace('\n', '').split(' ')     # Parse line to extract size and filename
                folder.add(File(filename, int(fSize)))                  # Creat new File instance and add to current folder
            notStarted = False                  # To make sure that next $ is signalled as end of ls output 
            lastPos = sourceFile.tell()         # update latest position in case rewind needed
            line = sourceFile.readline()        # find next line
        return sourceFile                       # Shouldn't be called but just in case anything weird happens

    def readDirs(self):
        # The main parsing function. Opens the root directory and starts to recurse through
        with open(self.filename) as file:
            lastPos = file.tell()               # See above - needed to rewind between method calls
            line = file.readline()
            while line != '':                   # '' indicates EOF
                if line[:4] == "$ cd":          # If changing directory
                    instructions = line.replace('\n', '').split(' ') #split the line into ['$', 'cd', 'newDir']
                    newDir = instructions[2]    # find the name of the new dir
                    if newDir == "/":           # if asked to return to root
                        self.currentDir = []    # empty list signals root directory
                    else:
                        newDirs = newDir.split('/') # if changing multiple dirs at once, treat them seperately
                        for d in newDirs:           # iterate through each new directory
                            if d == "..":           # handle moving back a level
                                self.currentDir = self.currentDir[:-1] # handle this by slicing the currentDir list to remove latest
                            else:
                                self.currentDir.append(d)   # otherwise add newDir to current path
                    workingDirectory = self.root            # starting at the root, go through every directory
                    for d in self.currentDir:               # in the currentDir and 
                        workingDirectory.add(Directory(d))  # make sure that it is added to its parent Directory
                        workingDirectory = workingDirectory.access(d)   # then open that directory and move into it
                elif line[:4] == "$ ls":                    # if the current line is issuing an ls command
                    file.seek(lastPos)                      # rewind back a line, ready to pass file off to method
                    file = self.findFiles(file, workingDirectory)   # find all the files listed in the file and resume where that
                                                                    # method finishes.
                lastPos = file.tell()
                line = file.readline()


r = Reader('Day7Input.txt')         # Initialise Reader class with filename
r.readDirs()                        # read the directories within the root
totalUsed = totalFree = minimumDeletion = 0 
smallestFound = 10 ** 20            # large value chosen to be greater than size of any folder
for name, size in r.root.scanDirs(): # scanDirs yields every directory within root as a tuple (name, size)
    if name == "/":                 # initialise the parameters from the root directory
        totalUsed = size            
        totalFree = 70000000 - size
        minimumDeletion = 30000000 - totalFree
    if size == minimumDeletion:     # if a Directory is found with the exact size needed, stop here as none smaller will be found
        print(size)
        break
    elif minimumDeletion < size < smallestFound: #if = then this will be caught above. Update smallestFound if this is smaller
        smallestFound = size
print("Done")
print(minimumDeletion, smallestFound)
