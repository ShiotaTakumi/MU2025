#!/usr/bin/env python3

import networkx as nx       # グラフ構造操作ライブラリ / Graph library
import os                   # ファイル・ディレクトリ操作 / For file and directory operations

# 頂点数 n をユーザー入力から受け取る
# Prompt user to enter the number of vertices
n = int(input("Enter the number of vertices (>= 4): "))

# 入力・出力ディレクトリのパスを構成
# Construct input and output directory paths
input_dir = f"d3cp/n{n}"      # 入力：平面かつ非同型なグラフ / Input: planar, non-isomorphic graphs
output_dir = f"d3cpt/n{n}"    # 出力：その中で 3-連結なもの / Output: 3-connected subset

# 出力ディレクトリが存在しなければ作成
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# 入力ディレクトリ内のすべての .g6 ファイルをソート順に処理
# Process all .g6 files in the input directory in sorted order
for filename in sorted(os.listdir(input_dir)):
    if not filename.endswith(".g6"):
        continue

    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    print(f"Filtering 3-connected planar graphs in: {input_path}")

    count = 0  # 3-連結なグラフの個数をカウント / Counter for 3-connected graphs

    # 入力ファイルを 1 行ずつ読み書き処理
    # Open and process the input file line-by-line
    with open(input_path, mode="rt") as f_in, open(output_path, mode="wt") as f_out:
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

    # 処理結果の要約を表示
    # Print summary of how many graphs were saved
    print(f"  -> {count} 3-connected planar graphs saved to {output_path}")
