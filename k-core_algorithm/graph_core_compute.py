import re
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# 该文件实现计算图中每个节点的core数，并根据节点的core，生成随机颜色并进行可视化。
def readGraph(filePath):
    fileData = open(file=filePath, mode='r')
    graphPoints = set()
    graphEdges = []
    for line in fileData:
        if re.search(r'edge', line) is not None:
            srcLine = fileData.readline()
            dstLine = fileData.readline()
            srcPoint = int(re.search(r'\d+', srcLine).group())
            dstPoint = int(re.search(r'\d+', dstLine).group())
            # print("{} - {}".format(srcPoint, dstPoint))
            graphPoints.add(srcPoint)
            graphPoints.add(dstPoint)
            graphEdges.append((srcPoint, dstPoint))
    return graphPoints, graphEdges


class GraphCore:
    def __init__(self, graph):
        self.graph = graph.copy()
        self.nodes = list(graph.nodes())
        self.nodesNum = len(self.nodes)
        self.nodesCore = {}
        self.coreUnique = []

    # 第一遍扫描，返回每个节点的度,所有节点最大度数和节点名称，节点索引值的键值对dict
    def _getNodeDegree(self, graph):
        nodesDict = {}
        nodesDegree = []
        maxDegree = 0

        for i in range(0, self.nodesNum):
            nodesDict[self.nodes[i]] = i
            degree = 0
            for j in nx.neighbors(graph, self.nodes[i]):
                degree += 1
            nodesDegree.append(degree)
            if maxDegree < degree:
                maxDegree = degree
        return maxDegree, nodesDegree, nodesDict

    # 构造链式存储节点core结构，返回该结构和每个节点在其中的位置
    def _getDegreeChain(self, maxDegree, nodesDegree):
        degreeChain = []
        nodesPosition = []

        for i in range(0, maxDegree + 1):
            degreeChain.append([])

        for idx in range(0, self.nodesNum):
            degree = nodesDegree[idx]
            nodesPosition.append(len(degreeChain[degree]))
            degreeChain[degree].append(idx)
        return degreeChain, nodesPosition

    # 计算每个节点的core并返回
    def calculateCore(self):
        maxDegree, nodesDegree, nodesDict = self._getNodeDegree(self.graph)
        degreeChain, nodesPosition = self._getDegreeChain(maxDegree, nodesDegree)
        nodesCore = {}

        for degree in range(0, len(degreeChain)):
            nodesList = degreeChain[degree]
            for nodeIdx in nodesList:
                if nodeIdx != -1:
                    for neighborNode in nx.neighbors(self.graph, self.nodes[nodeIdx]):
                        neighborIdx = nodesDict[neighborNode]
                        neighborDegree = nodesDegree[neighborIdx]
                        if neighborDegree > degree:
                            # degreeChain[nodesDegree[neighborIdx]].remove(neighborIdx)
                            neighborPosition = nodesPosition[neighborIdx]
                            degreeChain[neighborDegree][neighborPosition] = -1

                            nodesDegree[neighborIdx] -= 1
                            nodesPosition[neighborIdx] = len(degreeChain[nodesDegree[neighborIdx]])
                            degreeChain[nodesDegree[neighborIdx]].append(neighborIdx)

        for degree in range(0, maxDegree + 1):
            nodesList = degreeChain[degree]
            for nodeIdx in nodesList:
                if nodeIdx != -1:
                    nodesCore[self.nodes[nodeIdx]] = degree
        nodesCore = dict(sorted(nodesCore.items()))

        self.nodesCore = nodesCore
        coreValue = list(self.nodesCore.values())
        self.coreUnique = np.unique(np.array(coreValue))

        return nodesCore

    # 根据随机种子和core，生成每个点的颜色
    def _setColor(self, seed):
        coreColor = list(np.random.RandomState(seed).rand(len(self.coreUnique), 3))
        colorDict = dict(zip(self.coreUnique, coreColor))

        nodesColor = []
        for i in range(0, len(nodesCore)):
            color = colorDict[self.nodesCore[self.nodes[i]]]
            nodesColor.append(tuple(color))
        return nodesColor, coreColor

    # 图的core可视化
    def graphVisualization(self, layoutSeed, colorSeed):

        plt.figure(figsize=(11, 9)).canvas.set_window_title('Core Number Graph')
        nodesColor, coreColor = self._setColor(seed=colorSeed)

        pos = nx.spring_layout(graph, seed=layoutSeed)
        nx.draw_networkx(graph, pos, with_labels=True, node_color=nodesColor, font_size=11, node_size=300)

        labels = ["Core = {}".format(self.coreUnique[i]) for i in range(len(self.coreUnique))]
        patches = [mpatches.Patch(color=coreColor[i], label="{:s}".format(labels[i])) for i in range(len(coreColor))]

        curAxes = plt.gca()
        box = curAxes.get_position()
        curAxes.set_position([box.x0, box.y0, box.width, box.height])
        # bbox_to_anchor指定了图例legend的位置
        curAxes.legend(handles=patches, bbox_to_anchor=(1.0, 1.0), loc="upper right", ncol=2)  # 生成legend

        plt.title("The Core of the Points", fontsize=20)
        # plt.savefig("result.png")
        plt.show()


if __name__ == '__main__':
    # 读入图
    points, edges = readGraph("inputdoc2.gml")
    graph = nx.Graph()
    graph.add_nodes_from(list(points))
    graph.add_edges_from(edges)

    # 计算每个点的core，以字典的形式返回
    g = GraphCore(graph)
    nodesCore = g.calculateCore()
    print("The Core of the Points.")
    print(nodesCore)

    # 调用封装好的图可视化函数
    g.graphVisualization(layoutSeed=188, colorSeed=480)
