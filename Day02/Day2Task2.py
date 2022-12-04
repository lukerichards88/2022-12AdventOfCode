# X - Lose
# Y - Draw
# Z - Win

scores = {
    'A': 1,
    'B': 2,
    'C': 3
}

results = {
    'X': (0, 1, 0),
    'Y': (0, 0, 1),
    'Z': (1, 0, 0)
}

win = {
    'A': 'B',
    'B': 'C',
    'C': 'A'
}

lose = {v[1]: v[0] for v in win.items()}


def w(p1):
    return win[p1]


def l(p1):
    return lose[p1]


def d(p1):
    return p1


print(lose)


def yourMove(p1, result):
    W, L, D = result
    if W: return w(p1)
    if L: return l(p1)
    if D: return d(p1)


def score(p2, result):
    W, L, D = result
    score = scores[p2]
    score += (6 * W) + (3 * D)
    return score


total = 0
lines = 0
with open('221202Advent2.txt') as file:
    for line in file:
        x = line.replace('\n', '')
        p1, r = x.split(' ')
        result = results[r]
        p2 = yourMove(p1, result)
        total += score(p2, result)
    # print(lines + 1, total)
    # total = 0
    # lines += 1
    # if lines > 20: break

print(total)
