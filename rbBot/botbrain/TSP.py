import tsp
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

def namesToNums(args):
    nameToNumMap = {}
    numToNameMap = {}
    counter = 0
    for ls in args:
        for i in range(2):
            if ls[i] not in nameToNumMap:
                nameToNumMap[ls[i]] = counter
                numToNameMap[counter] = ls[i]
                counter += 1
    return nameToNumMap, numToNameMap

def edgesToAdjMatrix(tup):
    nameToNumMap = tup[0]
    edges = tup[1]
    nodes = int(len(edges)/2)
    res = np.zeros((nodes, nodes))

    for edge in edges:
        res[nameToNumMap[edge[0]], nameToNumMap[edge[1]]] = edge[2]

    return res

def numsToNodes(route, numToNameMap):
    res = []
    for node in route:
        res.append(numToNameMap[node])
    return res

def TSPSolver(*argv):
    nameToNumMap, numToNameMap = namesToNums(argv)
    adjMatrixInput = edgesToAdjMatrix((nameToNumMap, argv))
    route, totalDistance = solve_tsp_dynamic_programming(adjMatrixInput)
    return numsToNodes(route, numToNameMap)
