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

# n → n+1 の比較結果から、継続すべき系列情報を返す
# Compare p1 and p2 to identify change direction and diff (degree or count)
def extract_diff(p1, p2):
    diffs = []
    for a, b in zip(p1, p2):
        if a == b:
            continue
        if a[0] == b[0] and b[1] > a[1]:
            diffs.append(("count", a[0], b[1] - a[1]))  # count増加 / count increased
        elif a[1] == b[1] and b[0] > a[0]:
            diffs.append(("degree", a[1], b[0] - a[0]))  # degree増加 / degree increased
        else:
            return None  # 変化が複雑すぎるので不採用 / Skip if mixed or invalid
    return diffs

# extract_diff で得た情報を使って予測パターンを生成
# Generate expected p3 from p2 and diff info
def predict_next(p2, diffs):
    predicted = []
    for a in p2:
        modified = False
        for t, val, d in diffs:
            if t == "count" and a[0] == val:
                predicted.append([a[0], a[1] + d])
                modified = True
            elif t == "degree" and a[1] == val:
                predicted.append([a[0] + d, a[1]])
                modified = True
        if not modified:
            predicted.append(a[:])
    return predicted

# 完全一致判定（順番も一致） / Exact match including order
def is_exact_match(p1, p2):
    return all(a == b for a, b in zip(p1, p2))

# ユーザーから頂点数 n を入力
# Prompt user to input number of vertices n
n = int(input("Enter number of vertices n: ").strip())

# n, n+1, n+2 に対応するパターンを読み込む / Load patterns for n, n+1, n+2
patterns_n = load_patterns(n)
patterns_np1 = load_patterns(n + 1)
patterns_np2 = load_patterns(n + 2)

print(f"\n--- Searching for 3-step growth chains: n={n} → n={n+1} → n={n+2} ---\n")

# n → n+1 のペアを列挙して、系列候補を構築 / Compare n vs n+1
for p1 in patterns_n:
    for p2 in patterns_np1:
        if len(p1) != len(p2):
            continue
        diffs = extract_diff(p1, p2)
        if not diffs:
            continue
        predicted_p3 = predict_next(p2, diffs)
        for p3 in patterns_np2:
            if len(p3) != len(predicted_p3):
                continue
            if is_exact_match(predicted_p3, p3):
                print("✔ Found 3-step chain:")
                print(f"n{n}:{format_pattern(p1)}")
                print(f"n{n+1}:{format_pattern(p2)}")
                print(f"n{n+2}:{format_pattern(p3)}")
                print("---")