#!/usr/bin/env python3

import networkx as nx       # グラフ構造操作ライブラリ / Graph library
import lzma                 # .xz 圧縮ファイルの読み書き / For handling .xz compressed files

# 最大頂点数をユーザー入力から受け取る
# Prompt user to enter the maximum number of vertices
max_n = int(input("Enter the maximum number of vertices (>= 4): "))

for n in range(4, max_n + 1):
    print(f"Filtering 3-connected planar graphs for n = {n} ...")

    # 入出力ファイルのパス（.xz 圧縮された graph6 形式）
    # Define input/output paths for .xz compressed graph6 files
    input_path = f"d3cp/n{n}.g6.xz"     # 入力：平面かつ非同型なグラフ / Input: planar, non-isomorphic graphs
    output_path = f"d3cpt/n{n}.g6.xz"   # 出力：その中で 3-連結なもの / Output: 3-connected subset

    count = 0  # 3-連結なグラフの個数をカウント / Counter for 3-connected graphs

    # 圧縮ファイルを読み書き（1 行ずつ）
    # Open and process the compressed file line by line
    with lzma.open(input_path, mode="rt") as f_in, lzma.open(output_path, mode="wt") as f_out:
        for line in f_in:
            line = line.strip()

            # 空行やコメント行はスキップ
            # Skip blank lines or comments
            if not line or line.startswith('#'):
                continue

            # graph6 文字列 → NetworkX グラフに変換
            # Convert graph6 string to a NetworkX graph
            G = nx.from_graph6_bytes(line.encode())

            # 3-連結性の確認（頂点連結度 ≥ 3）
            # Check 3-connectivity (node connectivity ≥ 3)
            if nx.node_connectivity(G) >= 3:
                f_out.write(line + '\n')
                count += 1

    # 結果を出力
    # Print results
    print(f"  -> {count} 3-connected planar graphs saved to {output_path}")
