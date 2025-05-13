#!/usr/bin/env python3

import os                   # ファイル操作 / For file and directory handling
import lzma                 # .xz 圧縮ファイルの読み書き / For reading and writing .xz compressed files
import subprocess           # 外部 C++ プログラムの実行 / For invoking external C++ program
import networkx as nx       # グラフ構造操作ライブラリ / For graph operations with NetworkX

# 入力ディレクトリ名と、頂点数 n をユーザー入力から受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3c): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 出力ディレクトリは、入力ディレクトリ名に 'p' を付けた名前（例: d3cp）
# The output directory is named by appending 'p' to the input directory (e.g., d3cp)
output_dir = input_dir + "p"

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

# 指定された .g6.xz ファイルまたはチャンクファイルを処理して平面グラフのみを出力する関数
# This function processes the specified .g6.xz file and writes only planar graphs to the output
def process_file(input_path, output_path, n):
    with lzma.open(input_path, "rt") as f_in, lzma.open(output_path, "wt") as f_out:
        # Boost による平面性判定を行う C++ バイナリを起動
        # Launch the Boost-based C++ binary for planarity checking
        proc = subprocess.Popen(
            ["./planar"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        count = 0  # 平面グラフの個数をカウント / Counter for planar graphs

        # 入力ファイルを 1 行ずつ読み取りながら処理
        # Process each line (graph) from the input file
        for line in f_in:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # graph6 文字列を NetworkX グラフに変換
            # Convert the graph6 string to a NetworkX graph
            G = nx.from_graph6_bytes(line.encode())
            edges = list(G.edges())

            # エッジリストとともに、C++ 側にグラフ情報を送信
            # Send the graph info and edge list to the C++ process
            proc.stdin.write(f"# {n} {len(edges)}\n")
            for u, v in edges:
                proc.stdin.write(f"{u} {v}\n")
            proc.stdin.write(f"{line}\n")
            proc.stdin.write("\n")

        # 入力が終了したことを C++ 側に伝える
        # Close the input stream to signal end of input
        proc.stdin.close()

        # 出力を受け取りながら、平面なグラフだけを書き出す
        # Receive and write back the planar graphs only
        for result_line in proc.stdout:
            f_out.write(result_line)
            count += 1

        proc.stdout.close()
        proc.wait()

        # 結果を表示
        # Print result summary
        print(f"  -> {count} planar graphs saved to {output_path}")

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
