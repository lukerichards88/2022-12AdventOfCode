def priority(char: str):
    # return the priority for the first character of the string
    ordOfChar = ord(char[:1]) - 96
    adjustment = 0 if ordOfChar > 0 else 58
    return ordOfChar + adjustment


total = 0
backpacks = [line.replace('\n', '') for line in open('20221203.txt', 'r')]
groups = len(backpacks) // 3
for groupNumber in range(groups):
    groupBackpacks = [backpacks[3 * groupNumber + elfNumber] for elfNumber in range(3)]
    for item in groupBackpacks[0]:
        if item in groupBackpacks[1] and item in groupBackpacks[2]:
            total += priority(item)
            print(item)
            print(groupBackpacks)
            break
    print(total)
# break
