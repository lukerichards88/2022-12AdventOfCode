
filename = "Day12Input.txt"

width = 0
grid = []
markers = {}
with open(filename) as file:
    for line in file:
        grid.append(list(line.strip()))
        for marker in ('S', 'E'):
            if marker in line:
                h = startHeight = len(grid) - 1
                w  = line.index(marker)
                markers[marker] = (h, w)

height = len(grid)
width = len(grid[0])
print(height, width)
h, w = markers['S']
grid[h][w] = 'a'
h, w = markers['E']
grid[h][w] = 'z'
for x in grid:
    print(x)
print(markers)
graph = {}
for h in range(height):
    for w in range(width):
        graph[(h, w)] = []
shortestSteps = graph.copy()
for h, w in graph.keys():
    starth = max(0,h-1)
    endh = min(height, h+2)
    startw = max(0,w-1)
    endw = min(width, w+2)
    char = grid[h][w]
    t = (h, w)
    #print(h, w, starth, endh, startw, endw)
    for walkh in range(starth, endh):
        for walkw in range(startw, endw):
            walkt = (walkh, walkw)
            destchar = grid[walkh][walkw]
            if walkh != h and walkw != w:
                pass
            elif walkt == t:
                pass
            elif ord(char) - ord(destchar) <= 1:
                graph[t].append(walkt)

Visited = []
queue = [markers['E'], 'end']
depth = 0
currentVisit = 0
curr = None
currChar = None
while currChar != 'a' and depth < 600:
    curr = queue.pop(0)
    if curr == 'end':
        depth += 1
        queue.append('end')
        print(f"Queue Length: {len(queue)}")
        print(f"Depth: {depth}")
    elif curr not in Visited:
        for destination in graph[curr]:
            queue.append(destination)
        Visited.append(curr)
        if curr != 'end':
            h, w = curr
            currChar = grid[h][w]

#print(graph)
#print(Visited)
print(depth)
print(queue)