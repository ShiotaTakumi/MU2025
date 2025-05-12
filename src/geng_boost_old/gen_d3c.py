#!/usr/bin/env python3

import subprocess   # 外部コマンドの実行に使用 / For running external commands
import lzma         # .xz 圧縮ファイルの読み書きに使用 / For reading and writing .xz compressed files

# 最大頂点数をユーザー入力から受け取る
# Prompt user for the maximum number of vertices to process
max_n = int(input("Enter the maximum number of vertices (>= 4): "))

# 4 頂点から max_n 頂点まで順に処理
# Loop from 4 to max_n (inclusive) to generate graphs for each size
for n in range(4, max_n + 1):
    print(f"Generating n = {n} graphs ...")

    # 出力ファイルのパス（.g6.xz 形式で保存）
    # Construct output file path (compressed graph6 format)
    output_path = f"d3c/n{n}.g6.xz"

    # geng コマンドを構築（連結グラフ、頂点次数 3 以上）
    # Build geng command to generate connected graphs with min degree 3
    geng_cmd = ["geng", "-c", "-d3", str(n)]

    # geng を実行し、その出力をそのまま圧縮ファイルに保存
    # Run geng and directly pipe its output into a compressed file
    with lzma.open(output_path, mode="wt") as f_out:
        proc = subprocess.Popen(
            geng_cmd,
            stdout=subprocess.PIPE,       # geng の出力を取得 / Capture geng output
            stderr=subprocess.DEVNULL,    # エラーメッセージを抑制 / Suppress error messages
            text=True                     # テキストモード（str）/ Enable text mode
        )

        count = 0  # 出力されたグラフ数をカウント / Counter for number of graphs

        # geng の出力を1行ずつ読み取り
        # Read geng output line by line
        for line in proc.stdout:
            # ヘッダ行（例: >>graph6<<）はスキップ
            # Skip header lines starting with '>>'
            if not line.startswith(">>"):
                f_out.write(line)   # 圧縮ファイルに書き込み / Write to compressed output
                count += 1

        proc.stdout.close()   # 出力ストリームを閉じる / Close output stream
        proc.wait()           # geng の終了を待つ / Wait for geng to finish

    # 結果を出力
    # Print results
    print(f"  -> Saved {count} graphs to {output_path}")
