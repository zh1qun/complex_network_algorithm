import networkx as nx
from networkx import community
import numpy as np
import re
from matplotlib import pyplot as plt
import random


def readGraph(filePath):
    fileData = open(file=filePath, mode='r')
    graphPoints = []
    graphEdges = []

    for line in fileData:
        if re.search(r'node', line) is not None:
            while (len(fileData.readline()) <= 1):
                fileData.readline()
            nodeLine = fileData.readline()
            node = int(re.search(r'\d+', nodeLine).group())
            # print(node)
            graphPoints.append(node)
        elif re.search(r'edge', line) is not None:
            while (len(fileData.readline()) <= 1):
                fileData.readline()
            srcLine = fileData.readline()
            dstLine = fileData.readline()
            srcPoint = int(re.search(r'\d+', srcLine).group())
            dstPoint = int(re.search(r'\d+', dstLine).group())
            # print("{} - {}".format(srcPoint, dstPoint))
            graphEdges.append((srcPoint, dstPoint))
    return graphPoints, graphEdges


def mostFreqItem(d: dict):
    counter = {}
    for value in d.values():
        counter[value] = 0
    for item in d.keys():
        counter[d[item]] += 1
    maxValue = max(counter.values())
    retItems = []
    for value in d.values():
        if counter[value] == maxValue:
            retItems.append(value)
    return retItems


def getColorFromDict(nodeDict, seed):
    labelKind = list(nodeDict.values())
    k = len(labelKind)
    nodes = list(nodeDict.keys())
    colors = list(np.random.RandomState(seed).rand(k, 3))
    colorDict = dict(zip(labelKind, colors))

    nodesColor = {}
    for node in nodeDict.keys():
        color = colorDict[nodeDict[node]]
        nodesColor[node] = tuple(color)
    nodesColorList = [nodesColor[v] for v in nodes]
    return nodesColorList


def getCommunity(labelDict: dict):
    communityDict = {}
    for node in labelDict.keys():
        nLabel = labelDict[node]
        if communityDict.get(nLabel) is None:
            communityDict[nLabel] = [node]
        else:
            communityDict[nLabel].append(node)
    return list(communityDict.values())


def showCommunity(graph, communityDict, title):
    plt.figure(figsize=(7.5, 7.5))
    plt.title(title)
    nColor = getColorFromDict(communityDict, 100)
    pos = nx.spring_layout(graph, seed=37)
    nx.draw_networkx(graph, pos, node_color=nColor, label=graph.nodes)
    plt.show()
