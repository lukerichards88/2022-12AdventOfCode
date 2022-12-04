def checkContained(pair):
    elfOne, elfTwo = [(int(elf[0]), int(elf[1])) for elf in pair]
    return (elfOne[0] <= elfTwo[0] and elfOne[1] >= elfTwo[1]) or (elfOne[0] >= elfTwo[0] and elfOne[1] <= elfTwo[1])
contained = 0
lines = 0
allocations = [[pair[0].split('-'), pair[1].split('-')] for pair in [line.replace('\n','').split(',') for line in open('Day4Input.txt')]]
for pair in allocations:
    contained += checkContained(pair)
    lines += 1
print(contained)
print(lines)