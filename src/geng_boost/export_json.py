#!/usr/bin/env python3

import os                   # ファイル操作 / For file and directory handling
import lzma                 # .xz 圧縮ファイルの読み書き / For reading .xz compressed files
import json                 # JSON出力 / For exporting graph structure to JSON
import networkx as nx       # グラフ構造操作ライブラリ / For graph operations with NetworkX

# 入力ディレクトリ名と項点数 n を受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3cpt): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 単一ファイル・分割ファイルのパス
# Construct paths
single_input_path = os.path.join(input_dir, f"n{n}.g6.xz")
chunk_input_dir = os.path.join(input_dir, f"n{n}")

# JSON 出力用ディレクトリ
# Create output directory for JSON
json_dir = os.path.join("json", input_dir, f"n{n}")
os.makedirs(json_dir, exist_ok=True)

# グラフを格納するリスト
#  List to store parsed graphs
graphs = []

# 入力ファイルを読み込む
# Read input graphs
if os.path.exists(single_input_path):
    print(f"Reading from: {single_input_path}")
    with lzma.open(single_input_path, "rt") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                G = nx.from_graph6_bytes(line.encode())
                graphs.append(G)
elif os.path.isdir(chunk_input_dir):
    print(f"Reading from chunked files: {chunk_input_dir}")
    for fname in sorted(os.listdir(chunk_input_dir)):
        if fname.endswith(".g6.xz"):
            with lzma.open(os.path.join(chunk_input_dir, fname), "rt") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        G = nx.from_graph6_bytes(line.encode())
                        graphs.append(G)
else:
    print("Error: No valid input file or chunk directory found.")
    exit(1)

# 各グラフを JSON 形式にエクスポート
# Export each graph as JSON
for i, G in enumerate(graphs):
    data = {
        "nodes": [{"data": {"id": str(v)}} for v in G.nodes()],
        "edges": [{"data": {"source": str(u), "target": str(v)}} for u, v in G.edges()]
    }
    outpath = os.path.join(json_dir, f"{i+1}.json")
    with open(outpath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved: {outpath}")

# 完了メッセージ
# Summary message
print(f"\nDone. {len(graphs)} graphs exported to: {json_dir}")
