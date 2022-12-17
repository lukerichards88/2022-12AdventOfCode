filename = 'Day16Test.txt'
filename = 'Day16Input.txt'

from random import random
def parse(filename):
    graph = {}
    flowRates = {}
    with open(filename) as file:
        for line in file:
            tokens = line.strip().split(' ')
            valveOrigin = tokens[1]
            flowRate = int(tokens[4].split('=')[-1].replace(';',''))
            valveDestinations = tuple(token.replace(',','') for token in tokens[9:])
            graph.setdefault(valveOrigin, set()).update(valveDestinations)
            flowRates[valveOrigin] = flowRate
    return graph, flowRates

def runRandomTest(inputGraph, flowRates, seconds, elephant=False):
    inputGraph = dict(inputGraph)
    flowRates = dict(flowRates)
    TotalPressure = 0
    LossRateCurrent = 0
    ElephantCurrent = 'AA'
    NodeCurrent = 'AA'
    NodeLast = 'AA'
    justOpened = False
    justOpenedElephant = False
    addFlowRate = 0
    addFlowRateElephant = 0
    while seconds >= 1:
        if justOpened:
            LossRateCurrent += addFlowRate
            justOpened = False
            addFlowRate = 0
        if justOpenedElephant:
            LossRateCurrent += addFlowRateElephant
            addFlowRateElephant = 0
            justOpenedElephant = False
        if flowRates[NodeCurrent] > 0 and random() > 0.2:
            addFlowRate += flowRates[NodeCurrent]
            flowRates[NodeCurrent] = 0
            justOpened = True
        else:
            r = [random() * flowRates[key] + random() for key in inputGraph[NodeCurrent]]
            i = r.index(max(r))
            destination = tuple(inputGraph[NodeCurrent])[i]
            NodeLast = NodeCurrent
            NodeCurrent = destination
        if elephant and flowRates[ElephantCurrent] > 0 and random() > 0.2:
            addFlowRateElephant += flowRates[ElephantCurrent]
            flowRates[ElephantCurrent] = 0
            justOpenedElephant = True
        elif elephant:
            r = [random() * flowRates[key] + random() for key in inputGraph[ElephantCurrent]]
            i = r.index(max(r))
            ElephantDestination = tuple(inputGraph[ElephantCurrent])[i]
            ElephantCurrent = ElephantDestination
        seconds -= 1
        TotalPressure += LossRateCurrent
    return TotalPressure

def runNtests(n, graph, flowRates, secondsPerTest, elephant=False):
    x = 0
    bestScore = float('-inf')
    while True:
        testScore = runRandomTest(graph, flowRates, secondsPerTest, elephant=elephant)
        if testScore > bestScore:
            print("*****", x, testScore)
            bestScore = testScore
        x += 1
    print(bestScore)

def FW(graph):
    output = {note: {} for note in graph.keys()}
    for node in graph.keys():
        for node2 in graph.keys():
            if node == node2:
                output[node][node2] = 0
                output[node2][node] = 0
            else:
                output[node][node2] = float('inf')
                output[node2][node] = float('inf')
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            output[node][neighbour] = 1
            output[neighbour][node] = 1
    nodes = output.keys()
    for node1 in nodes:
        for node2 in nodes:
            for node3 in nodes:
                output[node1][node3] = min(output[node1][node3], output[node1][node2] + output[node2][node3])
                output[node3][node1] = output[node1][node3]
                #print(node1, node2, node3, output[node1][node3])
    return output

def main():
    graph, flowRates = parse(filename)
    runNtests(100000000, graph, flowRates, 30)


if __name__ == "__main__":
    main()
