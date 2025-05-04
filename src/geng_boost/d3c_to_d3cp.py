#!/usr/bin/env python3

import networkx as nx       # グラフ構造操作ライブラリ / Graph library
import subprocess           # 外部 C++ プログラムとの連携 / For invoking external C++ program
import lzma                 # .xz 圧縮ファイルの読み書き用 / For handling .xz compressed files

# 最大頂点数をユーザー入力から受け取る
# Prompt user to enter the maximum number of vertices
max_n = int(input("Enter the maximum number of vertices (>= 4): "))

for n in range(4, max_n + 1):
    print(f"Filtering planar graphs for n = {n} ...")

    # 入力・出力ファイルのパスを構成（.xz 形式の graph6 ファイル）
    # Construct input and output paths for .xz compressed graph6 files
    input_path = f"d3c/n{n}.g6.xz"     # 入力元：次数3以上 + 連結な非同型グラフ / Input: degree ≥3, connected, non-isomorphic graphs
    output_path = f"d3cp/n{n}.g6.xz"   # 出力先：上記のうち平面グラフのみ / Output: planar subset of the above

    # Boost の平面性判定 C++ バイナリを起動（in/out をパイプ接続）
    # Launch the compiled Boost-based C++ binary and connect via pipes
    with lzma.open(input_path, mode="rt") as f_in, lzma.open(output_path, mode="wt") as f_out:
        proc = subprocess.Popen(
            ["./a.out"],                    # 実行するバイナリ / The Boost-based planar checker
            stdin=subprocess.PIPE,          # C++ 側の標準入力（エッジリストなどを渡す） / Provide graph data via stdin
            stdout=subprocess.PIPE,         # C++ 側の標準出力（平面graph6文字列）を受け取る / Receive filtered output via stdout
            text=True                       # 文字列モード（Python3） / Enable text mode (str, not bytes)
        )

        count = 0  # 平面グラフの個数をカウント / Counter for planar graphs

        # 入力ファイル（.g6.xz）から 1 行ずつ読み込む
        # Read graph6 strings line-by-line from input
        for line in f_in:
            line = line.strip()

            # 空行・コメント行はスキップ
            # Skip blank or comment lines
            if not line or line.startswith('#'):
                continue

            # graph6 文字列 → NetworkX グラフへ変換
            # Convert graph6 string to a NetworkX graph
            G = nx.from_graph6_bytes(line.encode())

            # 辺リスト（u, v）形式で取得
            # Extract edges as list of (u, v) pairs
            edges = list(G.edges())

            # 以下の 4 項目を 1 つのグラフ単位として C++ へ送信
            # Send the following 4 items as a single graph unit to the C++ program
            # 1) グラフの情報：# n m
            # 1) Graph info line: "# n m"
            proc.stdin.write(f"# {n} {len(edges)}\n")

            # 2) 辺リスト行：u v（改行区切り）
            # 2) Edge list lines: "u v" (one per line)
            for u, v in edges:
                proc.stdin.write(f"{u} {v}\n")

            # 3) graph6 文字列行
            # 3) Graph6 format string (original input)
            proc.stdin.write(f"{line}\n")

            # 4) 区切りの空行
            # 4) Separator (blank line)
            proc.stdin.write("\n")

        # C++ 側への入力を終了
        # Close stdin to finish sending input to the C++ program
        proc.stdin.close()

        # C++ プログラムから出力を受け取り、圧縮ファイルに書き出す
        # Read planar graph6 strings from C++ and write to compressed output
        for result_line in proc.stdout:
            f_out.write(result_line)
            count += 1

        # C++ 側の出力受信を完了させる
        # Finalize receiving output from the C++ program
        proc.stdout.close()

        # C++ プログラムの終了を待つ
        # Wait for subprocess to finish
        proc.wait()

    # 処理結果の要約を表示
    # Print summary of how many planar graphs were saved
    print(f"  -> {count} planar graphs saved to {output_path}")
