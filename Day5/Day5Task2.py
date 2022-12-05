#import pprint
import json
tallestStack = 0
numberOfStacks = 0
boxStacks = []
#filename = 'test.txt'
filename = 'Day5Input.txt'
with open(filename, 'r') as file:
  for line in file:
    if "[" not in line:
      numberOfStacks = int(line.split()[-1])
      break
    tallestStack += 1
stacks = {stackNumber: [] for stackNumber in range(numberOfStacks)}
#print(stacks)
with open(filename, 'r') as file:
  for lineNumber, line in enumerate(file):
    if lineNumber < tallestStack:
      stackLine = [line.replace('\n','')[4*n:4*n+4] for n in range(numberOfStacks)]
      #print(stackLine)
      for stackNumber, box in enumerate(stackLine):
        if "[" in box:
          stacks[stackNumber].append(box.strip())
    elif line[0] == 'm':
      instruction = line.split()
      numberOfMoves, originStack, destinationStack = [int(x) for x in instruction[1:6:2]]
      originStack = int(originStack) - 1
      destinationStack = int(destinationStack) - 1
      stacks[destinationStack], stacks[originStack] = (stacks[originStack][:numberOfMoves] + stacks[destinationStack], stacks[originStack][numberOfMoves:])
      for number, stack in stacks.items():
        print(number, stack)
for number, stack in stacks.items():
  print(stack[0][1], end="")
      