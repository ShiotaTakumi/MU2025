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

# 2つの次数分布を比較して、degree または count のみ一致する要素ペアを表示する
# Compare two degree patterns and print element pairs where only degree or only count matches
def compare_and_print(p1, p2):
    print(f"Compare: {p1} vs {p2}")
    for a in p1:
        for b in p2:
            # 完全一致はスキップ / Skip if fully identical
            if a == b:
                continue
            # degree（次数）のみ一致 / Match only on degree
            if a[0] == b[0] and a[1] != b[1]:
                print(f"{a} <-> {b}")
            # count（出現数）のみ一致 / Match only on count
            elif a[1] == b[1] and a[0] != b[0]:
                print(f"{a} <-> {b}")
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