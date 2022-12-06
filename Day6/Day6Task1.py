def getMarkerPos(stream: str, streamLength: int):
    end = len(stream)
    start = streamLength
    for position in range(start, end):
        marker = stream[position - streamLength: position]
        marker = set(marker)
        if len(marker) == streamLength:
            return position

filename = 'Day6Input.txt'
with open(filename) as file:
    for line in file:
        line = line.replace('\n','')
        print(getMarkerPos(line, 4))