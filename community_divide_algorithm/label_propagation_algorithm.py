import networkx as nx
import community_divide_algorithm.common as common


# 根据Label Propagation Algorithm 标签传播算法进行社区划分
class LPA(object):
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    # 收敛：当本轮传播没有节点更新其标签时，达到收敛。
    def _isCoverage(self, lastFreqColor: dict, nodesColor: dict):
        coverage = 1
        for node in nodesColor.keys():
            nodeColor = nodesColor.get(node)
            if nodeColor not in lastFreqColor[node]:
                coverage = 0
                break
        return coverage

    # 返回该node的所有邻居节点的标签信息
    def _neighborLabelCount(self, node, nodesLabel):
        neighborsLabel = {}
        neighbors = nx.neighbors(self.graph, node)
        for neighbor in neighbors:
            neighborsLabel[neighbor] = nodesLabel[neighbor]
        return neighborsLabel

    # 标签传播流程
    def labelPropagation(self):
        nodesLabel = {v: k for k, v in enumerate(self.graph)}
        nodesMostFreqLabel = {}
        lastRoundLabel = {}
        nodes = list(self.graph.nodes)

        for node in nodes:
            lastRoundLabel[node] = []

        while self._isCoverage(lastRoundLabel, nodesLabel) != 1:
            lastRoundLabel = nodesMostFreqLabel
            for node in nodes:
                neighborsLabel = self._neighborLabelCount(node, nodesLabel)
                freqLabels = common.mostFreqItem(neighborsLabel)
                nodesMostFreqLabel[node] = freqLabels
                if nodesLabel[node] not in freqLabels:
                    nodesLabel[node] = freqLabels[0]
        return nodesLabel


if __name__ == '__main__':
    points, edges = common.readGraph("data/input_graph.txt")
    graph = nx.Graph()
    graph.add_nodes_from(points)
    graph.add_edges_from(edges)

    lpaObj = LPA(graph)
    communityDict = lpaObj.labelPropagation()
    # print(communityDict)
    community = common.getCommunity(communityDict)
    print("Communities is :", community)
    common.showCommunity(graph, communityDict, "Label Propagation Algorithm")
