#!/usr/bin/env python3

import subprocess   # 外部コマンドの実行に使用 / For running external commands
import lzma         # .xz 圧縮ファイルの読み書きに使用 / For reading and writing .xz compressed files
import shlex        # コマンドライン文字列をトークンに分割 / For parsing option strings
import os           # ディレクトリ操作に使用 / For directory handling

# geng に渡す追加オプションを受け取る
# Prompt user for geng options
opt_str = input("Enter geng options (e.g., -c -d3): ")
geng_options = shlex.split(opt_str)  # 空白で区切ってリストに変換 / Split options string into list

# オプションを変換：大文字なら x を付けて小文字化（例: -F → xf
# Convert options: uppercase becomes 'x' + lowercase (e.g., -F → xf)
converted_opts = []
for opt in geng_options:
    if opt.startswith('-'):
        opt_body = opt[1:]  # '-' を除去 / Remove leading '-'
        new_opt = ''
        for ch in opt_body:
            if ch.isupper():
                new_opt += 'x' + ch.lower()  # 大文字 → 'x' + 小文字 / Uppercase → 'x' + lowercase
            else:
                new_opt += ch  # 小文字はそのまま / Keep lowercase as is
        converted_opts.append(new_opt)
    else:
        converted_opts.append(opt)  # '-' で始まらない文字列はそのまま / Keep unprefixed items as is

# 変換後オプションを逆順にソートし、連結（例: ['c', 'd3', 'xf'] → 'xfd3c'）
# Sort reversed and concatenate (e.g., ['c', 'd3', 'xf'] → 'xfd3c')
base_dir = ''.join(sorted(converted_opts, reverse=True))

# 出力用ディレクトリを作成 / Create output directory
os.makedirs(base_dir, exist_ok=True)

# ループ処理か単体処理かを選択
# Ask user whether to run for a single n or a loop range
single_mode = input("Run in single-n mode? (y/n): ").strip().lower() == "y"

if single_mode:
    # 頂点数をユーザー入力から受け取る
    # Prompt user for the number of vertices
    n = int(input("Enter the number of vertices (>= 4): "))
    max_n = n
    min_n = n
else:
    # 最大頂点数をユーザー入力から受け取る
    # Prompt user for the maximum number of vertices to process
    max_n = int(input("Enter the maximum number of vertices (>= 4): "))
    min_n = 4

# ループ開始 / Begin loop
for n in range(min_n, max_n + 1):
    print(f"Generating n = {n} graphs ...")

    # 出力ファイルのパス（.g6.xz 形式で保存）
    # Construct output file path (compressed graph6 format)
    output_path = os.path.join(base_dir, f"n{n}.g6.xz")

    # geng コマンドを構築（ユーザー指定オプション + 頂点数）
    # Build geng command using user-specified options + vertex count
    geng_cmd = ["geng"] + geng_options + [str(n)]

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
