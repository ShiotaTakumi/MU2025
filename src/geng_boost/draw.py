#!/usr/bin/env python3

import os                           # ファイル操作 / For file and directory handling
import lzma                         # .xz 圧縮ファイルの読み書き / For reading and writing .xz compressed files
import networkx as nx               # グラフ構造操作ライブラリ / For graph operations with NetworkX
import matplotlib.pyplot as plt     # グラフ描画 / For drawing graphs
from math import ceil               # 切り上げ関数（ページ数計算に使用）/ For rounding up when computing number of pages

# 入力ディレクトリ名と頂点数を受け取る
# Prompt the user for the input directory and number of vertices
input_dir = input("Enter input directory name (e.g., d3cpt): ").strip()
n = int(input("Enter the number of vertices (e.g., 11): ").strip())

# 単一ファイル・分割ファイルパスを構成
# Construct paths for single-file input or chunked input
single_input_path = os.path.join(input_dir, f"n{n}.g6.xz")
chunk_input_dir = os.path.join(input_dir, f"n{n}")

# 出力ディレクトリ（描画結果）を作成
# Create output directory for graph drawings
draw_dir = os.path.join("drawing", input_dir, f"n{n}")
os.makedirs(draw_dir, exist_ok=True)

graphs = []  # グラフを格納するリスト / List to store loaded graphs

# 入力ファイルを読み込み（単一ファイルの場合）
# Read input from a single .g6.xz file
if os.path.exists(single_input_path):
    print(f"Reading from: {single_input_path}")
    with lzma.open(single_input_path, "rt") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                G = nx.from_graph6_bytes(line.encode())
                graphs.append(G)

# 分割された複数ファイルを順に読み込み
# Read from chunked directory if present
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

# グリッド設定（1 ページあたりの描画数）
# Grid layout settings (graphs per page)
cols = 5                                 # 横方向のグラフ数 / Number of graphs per row
rows = 7                                 # 縦方向のグラフ数 / Number of graphs per column
per_page = cols * rows                   # 1 ページあたりの最大グラフ数 / Max number of graphs per page
figsize = (cols * 2.5, rows * 2.5)       # 1ページのサイズ（インチ）/ Page size in inches
num_pages = ceil(len(graphs) / per_page) # ページ数の計算 / Calculate number of pages

# グラフ描画とページごとの保存処理
# Draw and save each page of graphs
for page in range(num_pages):
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten()

    for i in range(per_page):
        idx = page * per_page + i
        ax = axes[i]
        ax.axis('off')  # 軸を非表示にする / Hide axis

        if idx >= len(graphs):
            continue

        G = graphs[idx]
        try:
            pos = nx.planar_layout(G)  # 平面レイアウトで配置 / Use planar layout
        except:
            pos = nx.spring_layout(G, seed=42)  # 失敗時は spring_layout にフォールバック / Fallback to spring layout

        # グラフ描画（ノード・エッジは黒、ラベルなし）
        # Draw graph with black nodes and edges, no labels
        nx.draw(
            G, pos, ax=ax,
            node_size=40,
            node_color='black',
            edge_color='black',
            with_labels=False
        )

        # 各グラフにインデックス番号を表示
        # Show graph index below the drawing
        ax.text(0.5, -0.02, f"({idx + 1})", ha='center', va='top',
                transform=ax.transAxes, fontsize=13)

    # PDF として保存（複数ページに対応）
    # Save figure as PDF (per page)
    page_path = os.path.join(draw_dir, f"n{n}_page{page + 1}.pdf")
    plt.savefig(page_path, dpi=600, bbox_inches='tight')
    plt.close()
    print(f"Saved page: {page_path}")

# 完了メッセージ
# Print summary message
print(f"Done. {len(graphs)} graphs saved in {num_pages} PDF pages at: {draw_dir}")
