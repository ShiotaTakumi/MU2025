#!/usr/bin/env python3

import os           # ファイル・ディレクトリ操作 / For file and directory operations
import lzma         # .xz 圧縮ファイルの読み書き / For handling .xz compressed files
import math         # 行数からチャンク数を計算 / For calculating chunk count
import subprocess   # split コマンドの実行に使用 / For running external shell commands

# ベースディレクトリ名をユーザーから取得
# Prompt user for the base directory name
base_dir = input("Enter the base directory name (e.g., d3c): ").strip()

# 頂点数 n をユーザーから取得
# Prompt user for the number of vertices
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 入力ファイルパスを構築（.g6.xz 圧縮ファイル）
# Construct input file path (.g6.xz format)
target_file = f"{base_dir}/n{n}.g6.xz"

# 分割後のファイルを保存するディレクトリを作成
# Construct output directory path
output_dir = f"{base_dir}/n{n}"

# 一時的に展開する .g6 ファイルのパス
# Temporary uncompressed .g6 file path
decompressed_file = f"{base_dir}/n{n}.g6"

# .xz ファイルを展開して .g6 ファイルに書き出す
# Decompress .xz file and write to a temporary .g6 file
print(f"Decompressing: {target_file} -> {decompressed_file}")
with lzma.open(target_file, "rt") as fin, open(decompressed_file, "wt") as fout:
    fout.writelines(fin)

# 展開した .g6 ファイルの行数をカウント
# Count the number of lines in the decompressed file
with open(decompressed_file) as f:
    num_lines = sum(1 for _ in f)

# 分割数を計算（10000 行ごと）し、ファイル名サフィックスの桁数を決定
# Compute number of chunks (each ~10000 lines) and determine suffix length
num_chunks = math.ceil(num_lines / 10000)
suffix_length = len(str(num_chunks - 1))  # e.g., 0〜5499 → 4 digits

# 出力ディレクトリを作成（存在しなければ）
# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# split コマンドでファイルを分割
# Run split command to divide the file into chunks
print(f"Splitting {num_lines} lines into ~10000-line chunks...")
subprocess.run([
    "split",
    "-l", "10000",            # 10000 行ごとに分割 / Split every 10000 lines
    "-d",                     # 数字サフィックスを使用 / Use numeric suffixes
    f"-a{suffix_length}",     # サフィックスの桁数を指定 / Specify suffix length
    decompressed_file,
    os.path.join(output_dir, "")
])

# 各チャンクファイルに .g6 拡張子を追加し、.xz 形式で圧縮
# Rename each chunk file with .g6 extension and compress it to .xz format
print("Renaming and compressing split files...")
for fname in sorted(os.listdir(output_dir)):
    old_path = os.path.join(output_dir, fname)
    new_path = f"{old_path}.g6"
    os.rename(old_path, new_path)

    with open(new_path, "rb") as f_in, lzma.open(f"{new_path}.xz", "wb") as f_out:
        f_out.write(f_in.read())

    os.remove(new_path) # 元の .g6 ファイルを削除 / Remove original .g6 file

# 一時的に展開したファイルを削除
# Delete temporary decompressed file
print(f"Cleaning up temporary file: {decompressed_file}")
os.remove(decompressed_file)

# 元の .g6.xz ファイルを削除
# Remove original .g6.xz file
os.remove(target_file)

# 完了メッセージ
# Completion message
print("Done.")
