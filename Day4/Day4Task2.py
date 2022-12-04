def checkContained(pair):
    elfOne, elfTwo = [(int(elf[0]), int(elf[1])) for elf in pair]
    return (elfOne[0] <= elfTwo[0] <= elfOne[1]) or (elfOne[0] <= elfTwo[1] <= elfOne[1]) or (elfTwo[0] < elfOne[0] and elfTwo[1] > elfOne[1])
contained = 0
allocations = [[pair[0].split('-'), pair[1].split('-')] for pair in [line.replace('\n','').split(',') for line in open('Day4Input.txt')]]
for pair in allocations:
    contained += checkContained(pair)
print(contained)
