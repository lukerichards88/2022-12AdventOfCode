scores = {
    'X': 1,
    'Y': 2,
    'Z': 3
}


def remap(p1):
    if p1 == 'A': return 'X'
    if p1 == 'B': return 'Y'
    if p1 == "C": return 'Z'


def result(p1, p2):
    draw = (p1 == p2)
    lose = (p1 == 'X' and p2 == 'Z') or (p1 == 'Y' and p2 == 'X') or (p1 == 'Z' and p2 == 'Y')
    win = not (lose or draw)
    return win, lose, draw


def score(p1, p2):
    score = scores[p2]
    win, lose, draw = result(p1, p2)
    if win: return score + 6
    if lose: return score
    if draw: return score + 3


total = 0
with open('Day2Input.txt') as file:
    lines = 0
    for line in file:
        p1, p2 = line.replace('\n', '').split(' ')
        p1 = remap(p1)
        total += score(p1, p2)
print(total)