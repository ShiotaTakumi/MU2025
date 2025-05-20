#!/usr/bin/env python3

import os                   # ファイル操作 / For file and directory handling
import lzma                 # .xz 圧縮ファイルの読み書き / For reading and writing .xz compressed files
import networkx as nx       # グラフ構造操作ライブラリ / For graph operations with NetworkX
from collections import Counter, defaultdict

# 入力ディレクトリ名と、頂点数 n をユーザー入力から受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3cpt): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 単一の .g6.xz ファイルのパス（ファイルが分割されていない場合）
# Path for the single .g6.xz file if not split
single_input_path = os.path.join(input_dir, f"n{n}.g6.xz")
chunk_input_dir = os.path.join(input_dir, f"n{n}")

# 出現する次数分布のカウント辞書
# Dictionary to count how often each degree pattern appears
degree_pattern_counter = defaultdict(int)

# 指定されたファイルを処理して次数分布を集計する関数
# Function to process a file and count degree patterns
def count_degree_patterns(input_path):
    with lzma.open(input_path, "rt") as f_in:
        for line in f_in:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            G = nx.from_graph6_bytes(line.encode())
            degree_seq = [d for _, d in G.degree()]
            deg_count = sorted(Counter(degree_seq).items())  # [(deg, count), ...]
            key = tuple(deg_count)
            degree_pattern_counter[key] += 1

# 単一ファイルが存在すれば、それを処理
# If the single file exists, process it
if os.path.exists(single_input_path):
    print(f"Processing: {single_input_path}")
    count_degree_patterns(single_input_path)

# それ以外の場合、チャンクされたファイル群が存在するか確認し、すべて処理する
# Otherwise, if chunked files exist, process each one
elif os.path.isdir(chunk_input_dir):
    for fname in sorted(os.listdir(chunk_input_dir)):
        if not fname.endswith(".g6.xz"):
            continue
        input_path = os.path.join(chunk_input_dir, fname)
        print(f"Processing chunk: {input_path}")
        count_degree_patterns(input_path)

# 入力ファイルもチャンクも存在しない場合はエラー
# If neither a file nor a chunk directory exists, show an error
else:
    print("Error: No valid input file or chunk directory found.")
    exit(1)

# 結果の出力
# Output the frequency of each degree pattern
print("\nAll degree patterns and their frequencies:")
for pattern, count in sorted(degree_pattern_counter.items(), key=lambda x: (-x[1], x[0])):
    formatted = " ".join(f"[{deg},{cnt}]" for deg, cnt in pattern)
    print(f"{formatted} : {count}")

# 一意のものだけを出力
# Output only the degree patterns that appear exactly once
print("\nDegree patterns that appear exactly once:")
for pattern, count in sorted(degree_pattern_counter.items()):
    if count == 1:
        formatted = " ".join(f"[{deg},{cnt}]" for deg, cnt in pattern)
        print(f"{formatted}")
