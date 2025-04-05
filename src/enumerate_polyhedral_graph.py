#! /usr/bin/env python

from graphillion import GraphSet
import networkx as nx


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

        # 初期状態ではすべての部分グラフを保持する
        # Initialize with all subgraphs (full universe)
        self.base_graph = self
        self.graphs = GraphSet.universe()

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
    def __init__(self, prev):
        # 前段のグラフ情報を受け取る
        # Receive the graph information from the previous class
        self.base_graph = prev.base_graph
        self.graphs = prev.graphs

        # 各頂点の次数を 3 以上 (最大 n-1) に制限する制約を定義する
        # Define degree constraints to restrict each vertex to degree 3 or higher (up to n-1)
        self.degree_constraints = {v: range(3, self.base_graph.n) for v in self.base_graph.vertices}

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
    def __init__(self, prev):
        # 前段のグラフ情報を受け取る
        # Receive the graph information from the previous class
        self.base_graph = prev.base_graph
        self.graphs = prev.graphs

        # 頂点集合を取得する
        # Get the set of vertices
        vertices = self.base_graph.vertices

        # 連結なグラフだけを抽出する
        # Filter graphs that are connected
        self.graphs = self.graphs.including(GraphSet.connected_components(vertices))

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


class IsomorphismRemoval:
    """
    同型なものを取り除くクラス
    A class to remove isomorphic graphs.
    """
    def __init__(self, prev):
        # 前段のグラフ情報を受け取る
        # Receive the graph information from the previous class
        self.base_graph = prev.base_graph
        self.graphs = prev.graphs

        # 同型性除去後のグラフリストを格納
        # Store unique graphs after isomorphism filtering
        self.unique_graphs = []

        # すべてのグラフに対して同型判定を行う
        # Check all graphs for isomorphism
        for edge_list in self.graphs:
            # networkx のグラフオブジェクトを作成
            # Create a networkx Graph object
            G = nx.Graph()
            G.add_edges_from(edge_list)

            # 既存の unique_graphs に含まれるグラフと同型かどうかをチェック
            # Check if G is isomorphic to any graph already in unique_graphs
            is_new = True
            for H in self.unique_graphs:
                if nx.is_isomorphic(G, H):
                    is_new = False
                    break

            # 同型でなければ追加
            # If not isomorphic to any existing graph, add G to unique_graphs
            if is_new:
                self.unique_graphs.append(G)

    def output_graphs(self):
        # 同型性除去後のグラフを出力する（デバッグ用）
        # Output the graphs after isomorphism removal (for debugging)
        print("Non-isomorphic graphs:")
        for graph in self.unique_graphs:
            print(graph.edges())


class PlanarityRemoval:
    """
    平面でないグラフを取り除くクラス
    A class to remove non-planar graphs.
    """
    def __init__(self, prev):
        # 前段のグラフ情報を受け取る
        # Receive the graph information from the previous class
        self.base_graph = prev.base_graph
        self.graphs = []

        # もともとのグラフリストを取得
        # Get the original list of graphs
        original_graphs = prev.unique_graphs

        for G in original_graphs:
            # すでに networkx.Graph 型なのでそのまま平面性をチェック
            # Check planarity directly (already networkx.Graph)
            is_planar, _ = nx.check_planarity(G)
            if is_planar:
                # planar なものだけ保存
                # Save only planar graphs
                self.graphs.append(G)


def main():
    # 頂点数をユーザー入力で受け取る
    # Get the number of vertices from user input
    n = int(input("Enter the number of vertices (>= 4): "))

    # 全ての頂点に次数 3 以上を課すためには、頂点数は少なくとも 4 以上である必要がある
    # n must be at least 4 to enforce a minimum degree of 3 on every vertex
    if n < 4:
        print("Number of vertices must be at least 4 for degree >= 3 constraint.")
        return

    # 元グラフを作成
    # Create the base graph
    base_graph = BaseGraph(n)

    # 必要ならエッジ集合を出力する（デバッグ用）
    # Print the universe of edges (for debugging)
    # base_graph.print_universe()

    # 制約を順に適用
    # Apply constraints sequentially
    constrained_graph = base_graph

    # 次数制約を適用
    # Apply the degree constraint
    constrained_graph = DegreeConstraint(constrained_graph)
    print(f"Number of graphs after degree constraint: {len(constrained_graph.graphs)}")

    # 連結制約を適用
    # Apply the connectivity constraint
    constrained_graph = ConnectedConstraint(constrained_graph)
    print(f"Number of graphs after connected constraint: {len(constrained_graph.graphs)}")

    # 同型なものを取り除く
    # Remove isomorphic graphs
    constrained_graph = IsomorphismRemoval(constrained_graph)
    print(f"Number of non-isomorphic graphs: {len(constrained_graph.unique_graphs)}")

    # 平面グラフでないものを取り除く
    # Remove non-planar graphs
    constrained_graph = PlanarityRemoval(constrained_graph)
    print(f"Number of planar graphs: {len(constrained_graph.graphs)}")

    # グラフを出力する（デバッグ用）
    # Output the graphs (for debugging)
    # constrained_graph.output_graphs()

####################
if __name__ == "__main__":
    main()
