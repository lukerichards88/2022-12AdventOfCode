def priority(char: str):
    # return the priority for the first character of the string
    ordOfChar = ord(char[:1]) - 96
    adjustment = 0 if ordOfChar > 0 else 58
    return ordOfChar + adjustment


total = 0
backpacks = [(line[:len(line) // 2], line[len(line) // 2:]) for line in open('20221203.txt', 'r')]
print(len(backpacks) % 3)
for compartment1, compartment2 in backpacks:
    checked = []
    for item in compartment1:
        if item in compartment2 and item not in checked:
            print(item, priority(item))
            total += priority(item)
            checked.append(item)
print(total)
