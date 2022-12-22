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
inventoryItems = (ore, clay, obsidian, geode, oreRobots, clayRobots, obsidianRobots, geodeRobots)


def parse(filename: str):
    costs = []
    with open(filename) as file:
        for line in file:
            line.strip()
            line = line.replace(':', '').split()
            costs.append(tuple(int(line[x]) for x in (1, 6, 12, 18, 21, 27, 30)))
    return costs


class Blueprint:
    def __init__(self, costs):
        (
            self.name,
            oreCost,
            clayCost,
            obsidianCostOre,
            obsidianCostClay,
            geodeCostOre,
            geodeCostObsidian
        ) = costs
        self.costs = {
            ore: (oreCost, 0, 0),
            clay: (clayCost, 0, 0),
            obsidian: (obsidianCostOre, obsidianCostClay, 0),
            geode: (geodeCostOre, 0, geodeCostObsidian)
        }
        self.inventory = {itemType: 0 for itemType in inventoryItems}
        self.inventory[oreRobots] = 1
        self.maxNeeded = (
            max(oreCost, clayCost, obsidianCostOre, geodeCostObsidian),
            obsidianCostClay,
            geodeCostObsidian
                          )
    def inventoryCurrency(self):
        return (self.inventory[itemType] for itemType in (ore, clay, obsidian))

    def inventoryRobots(self):
        return (self.inventory[robotType] for robotType in (oreRobots, clayRobots, obsidianRobots, geodeRobots))
    def canAfford(self, robotName):
        robotCosts = self.costs[robotName]
        currency = self.inventoryCurrency()
        for price, held in zip(robotCosts, currency):
            if price > held:
                return False
        return True

    def shouldBuy(self, robotName):
        robots = (ore, clay, obsidian)
        index = robots.index(robotName)
        maxNeeded = self.maxNeeded
        currentRobots = self.inventoryRobots()

    def buy(self, robotName):
        for currency, price in zip(inventoryItems, self.costs[robotName]):
            self.inventory[currency] -= price
        return self




def DFS(blueprint):
    minute = 1
    tracebacks = []
    notStarted = True
    while len(tracebacks) > 0 or notStarted:
        notStarted = False
        if blueprint.canAfford(geode):
            tracebacks.insert(0, blueprint)


def main():
    blueprints = parse(filename)
    blueprints = (Blueprint(parameters) for parameters in blueprints)
    for blueprint in blueprints:
        best = DFS(blueprint)
        print(blueprint.name, best)


if __name__ == "__main__":
    main()
