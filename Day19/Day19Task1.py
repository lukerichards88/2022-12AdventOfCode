filename = 'Day19Test.txt'
# filename = 'Day19Input.txt'

ore = 'ore'
clay = 'clay'
obsidian = 'obsidian'
geode = 'geode'
oreRobots = 'oreRobots'
clayRobots = 'clayRobots'
obsidianRobots = 'obsidianRobots'
geodeRobots = 'geodeRobots'


class Universe:
    def __init__(self, parameters: tuple, inventory: tuple[int, ...], minutes):
        self.parameters = parameters
        (
            self.number,
            self.oreCost,
            self.clayCost,
            self.obsidianOreCost,
            self.obsidianClayCost,
            self.geodeOreCost,
            self.geodeObsidianCost
        ) = parameters
        (
            self.ore,
            self.clay,
            self.obsidian,
            self.geode,
            self.oreRobots,
            self.clayRobots,
            self.obsidianRobots,
            self.geodeRobots
        ) = inventory
        self.minutes = minutes
        costsKeys = (
            ore,
            clay,
            obsidian,
            geode
        )
        self.inventory = {
            ore: self.ore,
            clay: self.clay,
            obsidian: self.obsidian,
            geode: self.geode,
            oreRobots: self.oreRobots,
            clayRobots: self.clayRobots,
            obsidianRobots: self.obsidianRobots,
            geodeRobots: self.geodeRobots
        }
        oreCosts = (self.oreCost, 0, 0, 0)
        self.oreCosts = {a: b for a, b in zip(costsKeys, oreCosts)}
        clayCosts = (self.clayCost, 0, 0, 0)
        del oreCosts
        self.clayCosts = {a: b for a, b in zip(costsKeys, clayCosts)}
        del clayCosts
        obsidianCosts = (self.obsidianOreCost, self.obsidianClayCost, 0, 0)
        self.obsidianCosts = {a: b for a, b in zip(costsKeys, obsidianCosts)}
        del obsidianCosts
        geodeCosts = (self.geodeOreCost, 0, self.geodeObsidianCost, 0)
        self.geodeCosts = {a: b for a, b in zip(costsKeys, geodeCosts)}
        del geodeCosts
        self.costs = {ore: self.oreCosts, clay: self.clayCosts, obsidian: self.obsidianCosts, geode: self.geodeCosts}
        maxNeeded = {costType: max((self.costs[robotType][costType] for robotType in self.costs.keys())) for costType in self.costs.keys()}
        maxNeeded[geode] = 10 ** 6
        self.MaxNeeded = maxNeeded
    def possible(self):
        newOre = self.ore + self.oreRobots
        newClay = self.clay + self.clayRobots
        newObsidian = self.obsidian + self.obsidianRobots
        newGeode = self.geode + self.geodeRobots
        newInventory = (newOre, newClay, newObsidian, newGeode, self.oreRobots, self.clayRobots, self.obsidianRobots, self.geodeRobots)
        possibles = []
        robotType = geode
        for costType in (ore, clay, obsidian, geode):
            if self.inventory[robotType] >= self.MaxNeeded[robotType]:
                # print(f"Already have enough {robotType} robots. Not adding more. ")
                break
            ##print(self.costs)
            ##print(costType, robotType, self.inventory[costType], self.costs[robotType][costType])
            if self.inventory[costType] < self.costs[robotType][costType]:
                ##print(f"Cannot afford {robotType} because insufficient {costType}")
                break
        else:
            newOreRobots = self.oreRobots + (robotType == ore)
            newClayRobots = self.clayRobots + (robotType == clay)
            newObsidianRobots = self.obsidianRobots + (robotType == obsidian)
            newGeodeRobots = self.geodeRobots + (robotType == geode)
            newOre -= self.costs[robotType][ore]
            newClay -= self.costs[robotType][clay]
            newObsidian -= self.costs[robotType][obsidian]
            # newInventory = {thingType: self.inventory[thingType] - self.costs[robotType][thingType] for thingType in (ore, clay, obsidian, geode)}
            t = (self.parameters, (
            newOre, newClay, newObsidian, newGeode, newOreRobots, newClayRobots, newObsidianRobots, newGeodeRobots))
            possibles.append(t)
        if len(possibles) == 1:
            for robotType in (geode, ore, clay, obsidian):
                for costType in (ore, clay, obsidian, geode):
                    if self.inventory[robotType] >= self.MaxNeeded[robotType]:
                        #print(f"Already have enough {robotType} robots. Not adding more. ")
                        break
                    ##print(self.costs)
                    ##print(costType, robotType, self.inventory[costType], self.costs[robotType][costType])
                    if self.inventory[costType] < self.costs[robotType][costType]:
                        ##print(f"Cannot afford {robotType} because insufficient {costType}")
                        break
                else:
                    newOreRobots = self.oreRobots + (robotType == ore)
                    newClayRobots = self.clayRobots + (robotType == clay)
                    newObsidianRobots = self.obsidianRobots + (robotType == obsidian)
                    newGeodeRobots = self.geodeRobots + (robotType == geode)
                    newOre -= self.costs[robotType][ore]
                    newClay -= self.costs[robotType][clay]
                    newObsidian -= self.costs[robotType][obsidian]
                    #newInventory = {thingType: self.inventory[thingType] - self.costs[robotType][thingType] for thingType in (ore, clay, obsidian, geode)}
                    t = (self.parameters, (newOre, newClay, newObsidian, newGeode, newOreRobots, newClayRobots, newObsidianRobots, newGeodeRobots))
                    possibles.append(t)
                    #print(t)
        if self.minutes <= 1:
            possibles = []
        possibles.append((self.parameters, newInventory))
        return possibles



def parse(filename: str):
    universes = []
    with open(filename) as file:
        for line in file:
            line.strip()
            line = line.replace(':','').split()
            universes.append(Universe(tuple(int(line[x]) for x in (1, 6, 12, 18, 21, 27, 30)), (0, 0, 0, 0, 1, 0, 0, 0), 24))
            ##print(universes[-1].costs)
    return universes


def main():
    queue = [parse(filename)[1]]
    #print(queue)
    best = 0
    count = 0
    lengths = []
    DLs = []
    length = None
    oldLength = None
    while len(queue) > 0:
        count += 1
        universe = queue.pop(0)
        if count % 100000 == 0:
            length = len(queue)
            if oldLength is not None:
                DLs.append(length - oldLength)
                oldLength = length
            else:
                oldLength = length
            if len(DLs) > 0:
                if universe.minutes == 0:
                    remainingThisMinute = len(queue)
                else:
                    remainingThisMinute = sum((u.minutes == universe.minutes for u in queue))
                print(count, len(queue), DLs.pop(0), best, universe.minutes, remainingThisMinute)
        ##print("*******", universe.inventory, universe.possible(), universe.costs, "******", sep="\n")
        if universe.minutes == 0 and universe.geode > best:
            best = universe.geode
            print("*" * 20)
            print(best)
            print(universe.parameters, universe.inventory, universe.minutes - 1, universe.geode)
            print("*" * 20)
        elif universe.minutes > 0:
            #print(len(universe.possible()), len(queue))
            for possibleUniverse in universe.possible():
                par, inv = possibleUniverse
                #print(par, inv, universe.minutes - 1, universe.inventory)
                queue.append(Universe(par, inv, universe.minutes - 1))
    #print(best, count)

if __name__ == "__main__":
    main()
