#!/usr/bin/env python3

import os       # ファイル操作 / For file handling
import lzma     # .xz 圧縮ファイルの読み書き / For reading .xz compressed files

# 入力ディレクトリ名と、頂点数 n をユーザー入力から受け取る
# Prompt the user for the input directory name and the number of vertices
input_dir = input("Enter input directory name (e.g., d3c): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 単一ファイルとチャンクディレクトリのパスを構築
# Construct paths for single file and chunk directory
single_file_path = os.path.join(input_dir, f"n{n}.g6.xz")
chunk_dir_path = os.path.join(input_dir, f"n{n}")

total_lines = 0  # 全体の行数 / Total line count

# 単一ファイルが存在する場合はそれを読み込んでカウント
# If a single .g6.xz file exists, count its lines
if os.path.exists(single_file_path):
    print(f"Counting lines in: {single_file_path}")
    with lzma.open(single_file_path, "rt") as f:
        for _ in f:
            total_lines += 1

# チャンクされたファイル群が存在する場合はそれぞれ読み込んで合計
# If a directory of chunked files exists, count all their lines
elif os.path.isdir(chunk_dir_path):
    print(f"Counting lines in chunked files under: {chunk_dir_path}")
    for fname in sorted(os.listdir(chunk_dir_path)):
        if not fname.endswith(".g6.xz"):
            continue
        chunk_path = os.path.join(chunk_dir_path, fname)
        print(f"  -> {chunk_path}")
        with lzma.open(chunk_path, "rt") as f:
            for _ in f:
                total_lines += 1

# 入力が見つからない場合のエラー表示
# Show an error if no valid input found
else:
    print("Error: No .g6.xz file or chunk directory found.")
    exit(1)

# 結果の出力
# Print the total number of lines
print(f"\nTotal number of graphs (lines): {total_lines}")
