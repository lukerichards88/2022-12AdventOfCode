from Day8Task1 import *
filename = 'Day8Test.txt'
def checkVisibility(treeHeight, directionTuple, verbose=False):
  if len(directionTuple) == 0:
    return 0
  if max((int(x) for x in directionTuple)) < treeHeight:
    if verbose: print("full visibility", len(directionTuple))
    return len(directionTuple) 
  for distance, tree in enumerate(directionTuple, start=1):
    if int(tree) >= treeHeight:
      if verbose: print(directionTuple, tree, "less visibility", distance)
      return distance

def getScenicScore(treeHeight, directionTuples, verbose=False):
  scenicScore = 1
  for directionTuple in directionTuples:
    if verbose: print(directionTuple)
    visibility = checkVisibility(treeHeight, directionTuple, verbose)
    if visibility:
      scenicScore *= visibility
    else:
      return 0
  return scenicScore

def evaluate(array, position, width, verbose=False):
  rowLow, rowHigh = RowSplit(array, position, width)
  colLow, colHigh = ColumnSplit(array, position, width)
  rowLow, colLow = (x[::-1] for x in (rowLow, colLow))
  treeHeight = int(array[position])
  return getScenicScore(treeHeight, (rowLow, rowHigh, colLow, colHigh), verbose)

bestFound = 0
for treePosition in range(len(array)):
  score = evaluate(array, treePosition, width)
  if score > bestFound:
    bestFound = score
    print(treePosition, width, treePosition % width, treePosition // width, score, *RowSplit(array, treePosition, width))
    #evaluate(array, treePosition, width, True)
print(bestFound)

