#!/usr/bin/env python3

import os                   # ファイル操作 / For file and directory handling
import lzma                 # .xz 圧縮ファイルの読み書き / For reading and writing .xz compressed files
import networkx as nx       # グラフ構造操作ライブラリ / For graph operations with NetworkX

# 入力ディレクトリ名と、頂点数 n をユーザー入力から受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3cp): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 出力ディレクトリは、入力ディレクトリ名に 't' を付けた名前（例: d3cpt）
# The output directory is named by appending 't' to the input directory (e.g., d3cpt)
output_dir = input_dir + "t"

# 単一の .g6.xz ファイルのパス（ファイルが分割されていない場合）
# Path for the single .g6.xz file if not split
single_input_path = os.path.join(input_dir, f"n{n}.g6.xz")
single_output_path = os.path.join(output_dir, f"n{n}.g6.xz")

# 分割されたファイルが格納されたディレクトリ（大規模な入力時）
# Directory containing split chunk files (used when the input is large)
chunk_input_dir = os.path.join(input_dir, f"n{n}")
chunk_output_dir = os.path.join(output_dir, f"n{n}")

# 出力ディレクトリが存在しなければ作成する
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# 指定された .g6.xz ファイルまたはチャンクファイルを処理して3連結なグラフのみを出力する関数
# This function processes the specified .g6.xz file and writes only 3-connected graphs to the output
def process_file(input_path, output_path, n):
    with lzma.open(input_path, "rt") as f_in, lzma.open(output_path, "wt") as f_out:
        count = 0  # 3-連結なグラフの個数をカウント / Counter for 3-connected graphs

        # 入力ファイルを 1 行ずつ読み取りながら処理
        # Process each line (graph) from the input file
        for line in f_in:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # graph6 文字列を NetworkX グラフに変換
            # Convert the graph6 string to a NetworkX graph
            G = nx.from_graph6_bytes(line.encode())

            # 3-連結性の確認（頂点連結度 ≥ 3）
            # Check 3-connectivity (node connectivity ≥ 3)
            if nx.node_connectivity(G) >= 3:
                f_out.write(line + '\n')
                count += 1

        # 結果を表示
        # Print result summary
        print(f"  -> {count} 3-connected planar graphs saved to {output_path}")


# 単一ファイルが存在すれば、それを処理
# If the single file exists, process it
if os.path.exists(single_input_path):
    print(f"Processing: {single_input_path}")
    process_file(single_input_path, single_output_path, n)

# それ以外の場合、チャンクされたファイル群が存在するか確認し、すべて処理する
# Otherwise, if chunked files exist, process each one
elif os.path.isdir(chunk_input_dir):
    os.makedirs(chunk_output_dir, exist_ok=True)
    for fname in sorted(os.listdir(chunk_input_dir)):
        if not fname.endswith(".g6.xz"):
            continue
        input_path = os.path.join(chunk_input_dir, fname)
        output_path = os.path.join(chunk_output_dir, fname)
        print(f"Processing chunk: {input_path}")
        process_file(input_path, output_path, n)

# 入力ファイルもチャンクも存在しない場合はエラー
# If neither a file nor a chunk directory exists, show an error
else:
    print("Error: No valid input file or chunk directory found.")
