import networkx as nx
import community_divide_algorithm.common as common


class GNGraph(object):
    def __init__(self, graph):
        self.graph = graph

    def _getMaxBetweenness(self, betweenness: dict):
        maxBetweenness = 0
        edgeRmv = (0, 0)
        for edge in betweenness.keys():
            if maxBetweenness < betweenness[edge]:
                maxBetweenness = betweenness[edge]
                edgeRmv = edge
        return edgeRmv

    # Girvan and Newman Algorithm执行，不断移除Betweenness最大的边，直至收敛
    def getCommunity(self, k):
        graph = nx.Graph()
        graph.add_nodes_from(self.graph.nodes)
        graph.add_edges_from(self.graph.edges)
        communities = [self.graph.nodes]
        while len(communities) < k:
            edgeRmv = self._getMaxBetweenness(nx.edge_betweenness_centrality(graph))
            graph.remove_edge(edgeRmv[0], edgeRmv[1])
            communities = [list(c) for c in list(nx.connected_components(graph))]
        communityDict = {}

        for i in range(0, k):
            for node in communities[i]:
                communityDict[node] = i

        # 把结果按照节点编号排序
        return dict(sorted(communityDict.items(), key=lambda v: v[0]))


if __name__ == '__main__':
    points, edges = common.readGraph("data/input_graph.txt")
    graph = nx.Graph()
    graph.add_nodes_from(points)
    graph.add_edges_from(edges)

    gnObj = GNGraph(graph)
    communityDict = gnObj.getCommunity(5)
    community = common.getCommunity(communityDict)
    print("Communities is :", community)
    common.showCommunity(graph, communityDict, "Girvan and Newman Algorithm")
