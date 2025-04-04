#! /usr/bin/env python

from graphillion import GraphSet

def print_universe():
    # 設定されたエッジ集合を出力する
    # Print the universe of edges
    print("Edges in the universe:")
    for edge in GraphSet.universe():
        print(edge)

def main():
    # 頂点数をユーザー入力で受け取る
    # Get the number of vertices from user input
    n = int(input("Enter the number of vertices (>= 4): "))

    # 全ての頂点に次数 3 以上を課すためには、頂点数は少なくとも 4 以上である必要がある
    # n must be at least 4 to enforce a minimum degree of 3 on every vertex
    if n < 4:
        print("Number of vertices must be at least 4 for degree >= 3 constraint.")
        return

    # 頂点集合を定義する
    # Define the set of vertices
    vertices = list(range(1, n + 1))

    # 完全グラフの辺集合を定義する
    # Define the set of edges (complete graph)
    edges = [(i, j) for i in vertices for j in vertices if i < j]

    # 各辺 (i, j) に一意の番号を割り当てる
    # Assign a unique index to each edge (i, j)
    edge_to_index = {edge: idx + 1 for idx, edge in enumerate(edges)}

    # Graphillion にエッジ集合を設定する
    # Set the universe of edges for Graphillion
    GraphSet.set_universe(edges)

    # エッジ集合を出力する（デバッグ用）
    # Print the universe of edges (for debugging)
    # print_universe()

    # 全ての頂点の次数が少なくとも 3 以上になるように次数制約を定義する
    # 各頂点で許可される次数は、3, 4, ..., (n-1)
    # Define degree constraints so that every vertex has degree at least 3.
    # Allowed degrees for each vertex: 3, 4, ..., (n-1)
    degree_constraints = {v: range(3, n) for v in vertices}

    # 次数制約を満たすグラフを列挙する
    # Enumerate graphs satisfying the degree constraints
    graphs = GraphSet.graphs(degree_constraints=degree_constraints)

    # 次数制約を満たすグラフの結果を出力する（デバッグ用）
    # Output the graphs satisfying the degree constraints (for debugging)
    print("Graphs with all vertices having degree >= 3:")
    for graph in graphs:
        # (i, j) の頂点ペアとしてグラフをそのまま出力する
        # Output the graph directly as (i, j) vertex pairs
        # print(graph)

        # 辺 (i, j) を対応する番号に変換して出力する
        # Translate each edge (i, j) into its corresponding index and output
        translated_graph = [edge_to_index[e] for e in graph]
        print(translated_graph)

####################
if __name__ == "__main__":
    main()
