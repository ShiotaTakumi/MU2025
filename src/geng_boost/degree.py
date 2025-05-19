#!/usr/bin/env python3

import os                   # ファイル操作 / For file and directory handling
import lzma                 # .xz 圧縮ファイルの読み書き / For reading and writing .xz compressed files
import networkx as nx       # グラフ構造操作ライブラリ / For graph operations with NetworkX

# 頂点数式を安全に評価する関数（例: "n-2" を数値に変換）
# Safely evaluate expressions like "n-2" to an integer based on current n
def eval_expr(expr, n):
    return eval(expr, {"n": n})

# 入力ディレクトリ名と、頂点数 n をユーザー入力から受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3cpt): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 出力ディレクトリは、入力ディレクトリ名に 'd' を付けた名前（例: d3cptd）
# The output directory is named by appending 'd' to the input directory (e.g., d3cptd)
output_dir = input_dir + "d"

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

# ユーザーから次数条件を受け取る
# Prompt the user to input degree constraints
num_constraints = int(input("How many degree constraints would you like to apply? ").strip())
degree_conditions = []

for i in range(num_constraints):
    deg_expr = input(f"  Constraint {i+1} - Enter degree (e.g., '3' or 'n-2'): ").strip()
    count_expr = input(f"  Constraint {i+1} - Number of vertices with this degree (e.g., '2' or 'n-3'): ").strip()
    deg = eval_expr(deg_expr, n)
    count = eval_expr(count_expr, n)
    degree_conditions.append((deg, count))

# 指定されたグラフファイルを処理して、条件を満たすものだけ出力
# Process each graph and write only those that match the degree conditions
def process_file(input_path, output_path, n, degree_conditions):
    with lzma.open(input_path, "rt") as f_in, lzma.open(output_path, "wt") as f_out:
        count = 0  # 条件を満たすグラフの個数をカウント / Counter for matching graphs
        
        # 入力ファイルを 1 行ずつ読み取りながら処理
        # Process each line (graph) from the input file
        for line in f_in:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # graph6 文字列を NetworkX グラフに変換
            # Convert the graph6 string to a NetworkX graph
            G = nx.from_graph6_bytes(line.encode())

            # 指定された次数条件をすべて満たすか確認
            # Check if the graph satisfies all specified degree constraints
            degrees = [d for _, d in G.degree()]
            if all(degrees.count(deg) == cnt for deg, cnt in degree_conditions):
                f_out.write(line + '\n')
                count += 1

        # 結果を表示
        # Print result summary
        print(f"  -> {count} graphs matching degree constraints saved to {output_path}")

# 単一ファイルが存在すれば、それを処理
# If the single file exists, process it
if os.path.exists(single_input_path):
    print(f"Processing: {single_input_path}")
    process_file(single_input_path, single_output_path, n, degree_conditions)

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
        process_file(input_path, output_path, n, degree_conditions)

# 入力ファイルもチャンクも存在しない場合はエラー
# If neither a file nor a chunk directory exists, show an error
else:
    print("Error: No valid input file or chunk directory found.")
