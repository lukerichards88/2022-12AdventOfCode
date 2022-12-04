# Day1Task1 was overwritten when I did Task 2 but this provides the answers to both.

with open('Day01Input.txt') as file:
    elves = []
    calories = 0
    for line in file:
        if line == "\n":
            elves.append(calories)
            calories = 0
        else:
            calories += int(line)
# Task 1 Answer
print(max(elves))
elves.sort()
# Task 2 Answer
print(elves[-3:])
print(sum(elves[-3:]))
