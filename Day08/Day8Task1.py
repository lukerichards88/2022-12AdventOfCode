width = 0
length = 0
array = ""
filename = 'Day8Input.txt'

def Row(array, position, width):
  rowNum = position // width
  rowStart = rowNum * width
  rowEnd = rowStart + width
  return array[rowStart:rowEnd]

def RowSplit(array, position, width):
  row = Row(array, position, width)
  positionInRow = position % width
  splitLow, splitHigh = row[:positionInRow], row[positionInRow + 1:]
  return splitLow, splitHigh

def Column(array, position, width):
  columnNum = position % width
  return array[columnNum::width]
  
def ColumnSplit(array, position, width):
  column = Column(array, position, width)
  row = position // width
  splitLow = column[:row]
  splitHigh = column[row + 1:]
  return splitLow, splitHigh
  
def checkVisibleOneD(treeHeight, split1, split2):
  if 0 in (len(split1), len(split2)):
    return True
  maxOne = max(split1)
  maxTwo = max(split2)
  if treeHeight > maxOne or treeHeight > maxTwo:
    return True
  return False
  

def checkVisible(array, position, width):
  treeHeight = array[position]
  rowBefore, rowAfter = RowSplit(array, position, width)
  if checkVisibleOneD(treeHeight, rowBefore, rowAfter):
    return True
  if checkVisibleOneD(treeHeight, *ColumnSplit(array, position, width)):
    return True
  return False


with open(filename) as file:
  for line in file:
    line = line.replace('\n','')
    if not width:
      width = len(line)
    length += 1
    array += line
    
if __name__ == "__main__":  
  visibleCount = 0
  for position in range(len(array)):
    if checkVisible(array, position, width):
      visibleCount += 1
  print()
  print(visibleCount)