dirName = "Day{}"
Task1 = "{}Task1.py"
Task2 = "{}Task2.py"
Test = "{}Test.txt"
Input = "{}Input.txt"
filenames = [Task1, Task2, Test, Input]
StartDay = 14
FinishDay = 25
templateFilename = 'template.py'

def getFilenames(directory: str) -> tuple:
    return tuple(f"{directory}/{filename.format(directory)}" for filename in filenames)

def setTaskTemplates(day: int, *filenames: str) -> bool:
    for filename in filenames:
        with open(templateFilename, 'r') as template:
            with open(filename, 'w') as newFile:
                newFile.write("filename = 'Day{}Test.txt'\n".format(day))
                newFile.write("# filename = 'Day{}Input.txt'\n".format(day))
                if filename[-4] == "2": newFile.write("from Day{}Task1 import *\n".format(day))
                newFile.write("\n")
                for line in template: newFile.write(line)
    return True

def makeEmptyTXTfiles(*filenames: str) -> bool:
    for filename in filenames:
        with open(filename, 'w') as file:
            file.write('')
    return True
def main():
    for day in range(StartDay, FinishDay+1):
        dir = dirName.format(day)
        Task1, Task2, Test, Input = getFilenames(dir)
        setTaskTemplates(day, Task1, Task2)
        makeEmptyTXTfiles(Test, Input)




if __name__ == "__main__":
    main()
