#!/usr/bin/env python3

import lzma                         # .xz 圧縮ファイルの読み書き / For handling .xz compressed files
import networkx as nx               # グラフ構造操作ライブラリ / Graph library
import matplotlib.pyplot as plt     # グラフ描画ライブラリ / For drawing graphs using matplotlib
from math import ceil               # 切り上げ関数（ページ数計算に使用）/ For rounding up when computing number of pages

# 頂点数 n をユーザー入力から受け取る
# Prompt user to enter number of vertices
n = int(input("Enter the number of vertices (>= 4): "))

# 入力・出力ファイルのパスを構成
# Construct input/output paths (from 3-connected planar graph .g6.xz)
input_path = f"d3cpt/n{n}.g6.xz"         # 入力ファイル / Input file (.g6.xz format)
output_path = f"drawing/n{n}.pdf"           # 出力ファイル / Output PDF file

# グリッド設定（1 ページあたりの描画数）
# Grid layout settings (graphs per page)
cols = 5                                 # 横方向のグラフ数 / Number of graphs per row
rows = 7                                 # 縦方向のグラフ数 / Number of graphs per column
per_page = cols * rows                   # 1 ページあたり最大描画数 / Max number of graphs per page
figsize = (cols * 2.5, rows * 2.5)       # ページサイズ（インチ）/ Page figure size in inches

graphs = []  # 描画対象グラフを格納 / List of graphs to be drawn

# .g6.xz ファイルからグラフを読み込む
# Read graphs from compressed .g6.xz file
with lzma.open(input_path, "rt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        G = nx.from_graph6_bytes(line.encode())
        graphs.append(G)

# 必要ページ数を計算
# Compute number of required pages
num_pages = ceil(len(graphs) / per_page)

# ページごとに描画処理
# Render graphs page by page
for page in range(num_pages):
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten()

    for i in range(per_page):
        idx = page * per_page + i
        ax = axes[i]
        ax.axis('off')  # 軸非表示 / Hide axes

        if idx >= len(graphs):
            continue

        G = graphs[idx]
        pos = nx.planar_layout(G)  # 平面レイアウト計算 / Compute planar layout

        # グラフ描画（黒ノード・黒エッジ、ラベルなし）
        # Draw graph with small black nodes and black edges
        nx.draw(
            G, pos, ax=ax,
            node_size=40,
            node_color='black',
            edge_color='black',
            with_labels=False
        )

        # グラフ下に番号を表示（中央寄せ、やや近め、少し大きめ）
        # Show (index) label under each graph (centered and slightly closer)
        ax.text(0.5, -0.02, f"({idx + 1})", ha='center', va='top',
                transform=ax.transAxes, fontsize=13)

    # PDF 保存（複数ページにも対応）
    # Save current page as PDF (supports multi-page output)
    if num_pages == 1:
        plt.savefig(output_path, dpi=600, bbox_inches='tight')
    else:
        page_path = f"drawing/n{n}_page{page + 1}.pdf"
        plt.savefig(page_path, dpi=600, bbox_inches='tight')

    plt.close()  # メモリ解放 / Release memory

# 最終メッセージ出力
# Print summary message
print(f"Saved {len(graphs)} graphs to {output_path} (or split pages if needed)")
