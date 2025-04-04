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
    n = int(input("Enter the number of vertices: "))

    # 頂点集合を定義する
    # Define the set of vertices
    vertices = list(range(1, n + 1))

    # 完全グラフの辺集合を定義する
    # Define the set of edges (complete graph)
    edges = [(i, j) for i in vertices for j in vertices if i < j]

    # Graphillion にエッジ集合を設定する
    # Set the universe of edges for Graphillion
    GraphSet.set_universe(edges)

    # エッジ集合を出力する
    # Print the universe of edges
    # print_universe()

####################
if __name__ == "__main__":
    main()
