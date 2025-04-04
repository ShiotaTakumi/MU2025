#! /usr/bin/env python

from graphillion import GraphSet


class BaseGraph:
    """
    完全グラフ（頂点ペアの集合）を構成するクラス
    A class to generate the complete graph (as a set of vertex pairs).
    """

    def __init__(self, n):
        # 頂点数 n を使って初期化する
        # Initialize using the number of vertices n
        self.n = n

        # 頂点集合を定義する
        # Define the set of vertices
        self.vertices = list(range(1, n + 1))

        # 完全グラフの辺集合を定義する
        # Define the set of edges (complete graph)
        self.edges = [(i, j) for i in self.vertices for j in self.vertices if i < j]

        # 各辺 (i, j) に一意の番号を割り当てる
        # Assign a unique index to each edge (i, j)
        self.edge_to_index = {edge: idx + 1 for idx, edge in enumerate(self.edges)}

        # Graphillion にエッジ集合を設定する
        # Set the universe of edges for Graphillion
        GraphSet.set_universe(self.edges)

    def print_universe(self):
        # エッジ集合を出力する
        # Print the universe of edges
        print("Edges in the universe:")
        for edge in GraphSet.universe():
            print(edge)


class DegreeConstraint:
    """
    次数制約を満たすグラフを列挙するクラス
    A class to enumerate graphs satisfying the degree constraints.
    """

    def __init__(self, base_graph):
        # 元となる完全グラフの情報を受け取る
        # Receive the complete graph information from a BaseGraph instance
        self.base_graph = base_graph

        # 各頂点の次数を 3 以上 (最大 n-1) に制限する制約を定義する
        # Define degree constraints to restrict each vertex to degree 3 or higher (up to n-1)
        self.degree_constraints = {v: range(3, base_graph.n) for v in base_graph.vertices}

        # 次数制約を満たすグラフを列挙する
        # Enumerate graphs satisfying the degree constraints
        self.graphs = GraphSet.graphs(degree_constraints=self.degree_constraints)

    def output_graphs(self):
        # 次数制約を満たすグラフの結果を出力する（デバッグ用）
        # Output the graphs satisfying the degree constraints (for debugging)
        print("Graphs with all vertices having degree >= 3:")
        for graph in self.graphs:
            # (i, j) の頂点ペアとしてグラフをそのまま出力する
            # Output the graph directly as (i, j) vertex pairs
            # print(graph)

            # 辺 (i, j) を対応する番号に変換して出力する
            # Translate each edge (i, j) into its corresponding index and output
            translated_graph = [self.base_graph.edge_to_index[e] for e in graph]
            print(translated_graph)


class ConnectedConstraint:
    """
    連結制約を満たすグラフを抽出するクラス
    A class to filter graphs satisfying the connected constraint.
    """

    def __init__(self, deg_const_graph):
        # DegreeConstraint クラスのインスタンスからグラフ集合を受け取る
        # Receive the graph set from a DegreeConstraint instance
        self.base_graph = deg_const_graph.base_graph

        # 頂点集合を取得する
        # Get the set of vertices
        vertices = self.base_graph.vertices

        # 連結なグラフだけを抽出する
        # Filter graphs that are connected
        self.graphs = deg_const_graph.graphs.including(GraphSet.connected_components(vertices))

    def output_graphs(self):
        # 連結制約を満たすグラフの結果を出力する（デバッグ用）
        # Output the graphs satisfying the connected constraint (for debugging)
        print("Graphs that are connected:")
        for graph in self.graphs:
            # (i, j) の頂点ペアとしてグラフをそのまま出力する
            # Output the graph directly as (i, j) vertex pairs
            # print(graph)
    
            # 辺 (i, j) を対応する番号に変換して出力する
            # Translate each edge (i, j) into its corresponding index and output
            translated_graph = [self.base_graph.edge_to_index[e] for e in graph]
            print(translated_graph)


def main():
    # 頂点数をユーザー入力で受け取る
    # Get the number of vertices from user input
    n = int(input("Enter the number of vertices (>= 4): "))

    # 全ての頂点に次数 3 以上を課すためには、頂点数は少なくとも 4 以上である必要がある
    # n must be at least 4 to enforce a minimum degree of 3 on every vertex
    if n < 4:
        print("Number of vertices must be at least 4 for degree >= 3 constraint.")
        return

    # BaseGraph クラスを用いて元グラフを作成する
    # Use the BaseGraph class to construct the base graph
    base_graph = BaseGraph(n)

    # 必要ならエッジ集合を出力する（デバッグ用）
    # Print the universe of edges (for debugging)
    # base_graph.print_universe()

    # DegreeConstraint クラスを用いて次数制約を満たすグラフを列挙する
    # Use the DegreeConstraint class to enumerate graphs satisfying the degree constraints
    deg_const_graph = DegreeConstraint(base_graph)

    # 次数制約を満たすグラフの結果を出力する（デバッグ用）
    # Output the graphs satisfying the degree constraints (for debugging)
    # deg_const_graph.output_graphs()

    # 次数制約を満たすグラフの個数を出力する（デバッグ用）
    # Output the number of graphs satisfying the degree constraints (for debugging)
    print(len(deg_const_graph.graphs))

    # ConnectedConstraint クラスを用いて連結制約を満たすグラフを抽出する
    # Use the ConnectedConstraint class to filter graphs satisfying the connected constraint
    connected_graph = ConnectedConstraint(deg_const_graph)

    # 連結制約を満たすグラフの結果を出力する（デバッグ用）
    # Output the graphs satisfying the connected constraint (for debugging)
    # connected_graph.output_graphs()

    # 連結制約を満たすグラフの個数を出力する（デバッグ用）
    # Output the number of graphs satisfying the connected constraint (for debugging)
    print(len(connected_graph.graphs))


####################
if __name__ == "__main__":
    main()
