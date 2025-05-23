#!/usr/bin/env python3

import re  # 正規表現を使った文字列抽出に使用 / For extracting structured patterns using regular expressions
import os  # ファイル操作と存在確認に使用 / For file access and path checking

# 次数分布パターン文字列をパースする関数
# Parse a degree pattern string (e.g., "[3,2] [4,3]") into a list of [degree, count] pairs
def parse_line(line):
    matches = re.findall(r"\[(\d+),\s*(\d+)\]", line)
    return [[int(deg), int(cnt)] for deg, cnt in matches]

# 指定された n に対応するパターンファイルを読み込む
# Load all degree patterns from file degree_list/n{n}.txt
def load_patterns(n):
    path = f"degree_list/n{n}.txt"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
    with open(path, "r") as f:
        return [parse_line(line.strip()) for line in f if line.strip()]

# パターンリストを "[a,b] [c,d]" の形式に整形する関数
# Format pattern list as "[a,b] [c,d]" string for display
def format_pattern(pattern):
    return " ".join([f"[{a},{b}]" for a, b in pattern])

# 2つの次数分布を比較して、degree または count のみ一致する要素ペアとその差分を表示する
# Compare two degree patterns and print element pairs with matching degree or count, and show their difference
def compare_and_print(p1, p2):
    # 有効な比較が1つもなければ出力しない
    # Skip if there are no meaningful comparisons
    total_diff = 0  # 差分の合計を追跡 / Track total difference
    for a, b in zip(p1, p2):
        if a == b:
            continue
        if a[0] == b[0] and a[1] != b[1]:
            diff = b[1] - a[1]
            if diff < 0:
                return  # 減少があれば除外 / Skip if count decreased
            total_diff += diff
        elif a[1] == b[1] and a[0] != b[0]:
            diff = b[0] - a[0]
            if diff < 0:
                return  # 減少があれば除外 / Skip if degree decreased
            total_diff += diff
        else:
            return  # 完全不一致があるなら除外 / Skip if neither matches

    # 差分の合計が1または2のみ表示 / Show only if total difference is 1 or 2
    if total_diff == 1:
        print("--- diff = 1 ---")  # 差分1の表示ラベル / Label for total difference 1
        print(f"n{n}: {format_pattern(p1)}")
        print(f"n{n+1}: {format_pattern(p2)}")
        print("---")
    elif total_diff == 2:
        print("--- diff = 2 ---")  # 差分2の表示ラベル / Label for total difference 2
        print(f"n{n}: {format_pattern(p1)}")
        print(f"n{n+1}: {format_pattern(p2)}")
        print("---")

# ユーザーから頂点数 n を入力
# Prompt user to input number of vertices n
n = int(input("Enter number of vertices n: ").strip())

# n と n+1 に対応するパターンを読み込む / Load patterns for n and n+1
patterns_n = load_patterns(n)
patterns_np1 = load_patterns(n + 1)

print(f"\n--- Comparing n={n} vs n={n+1} (Cartesian product) ---\n")

# 要素数が一致するパターン間だけを比較する
# Compare only patterns with the same number of elements
for p1 in patterns_n:
    for p2 in patterns_np1:
        if len(p1) != len(p2):
            continue
        compare_and_print(p1, p2)
