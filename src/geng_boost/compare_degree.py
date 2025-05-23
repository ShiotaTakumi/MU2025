#!/usr/bin/env python3

import re  # 正規表現を使った文字列抽出に使用 / For extracting structured patterns using regular expressions
import os  # ファイル操作と存在確認に使用 / For file access and path checking

# 次数分布パターン文字列をパースする関数
# Parse a degree pattern string (e.g., "[3,2] [4,3]") into a list of [degree, count] pairs
def parse_line(line):
    matches = re.findall(r"\[(\d+),\s*(\d+)\]", line)  # 正規表現で [数字, 数字] をすべて抽出 / Extract all [number, number] pairs
    return [[int(deg), int(cnt)] for deg, cnt in matches]  # 数字を整数に変換してリストに格納 / Convert to list of integer pairs

# 指定された n に対応するパターンファイルを読み込む
# Load all degree patterns from file degree_list/n{n}.txt
def load_patterns(n):
    path = f"degree_list/n{n}.txt"  # ファイルパスを生成 / Generate file path
    if not os.path.exists(path):  # ファイルが存在するか確認 / Check if file exists
        print(f"File not found: {path}")
        return []
    with open(path, "r") as f:
        return [parse_line(line.strip()) for line in f if line.strip()]  # 空行を除いて各行をパース / Parse each non-empty line

# パターンリストを "[a,b] [c,d]" の形式に整形する関数
# Format pattern list as "[a,b] [c,d]" string for display
def format_pattern(pattern):
    return " ".join([f"[{a},{b}]" for a, b in pattern])  # 各ペアを整形して連結 / Format each pair and join as string

# n → n+1 の比較結果から、継続すべき系列情報を返す
# Compare p1 and p2 to identify change direction and diff (degree or count)
def extract_diff(p1, p2):
    diffs = []
    for a, b in zip(p1, p2):  # 同じインデックスのペアを比較 / Compare corresponding elements
        if a == b:
            continue  # 完全一致ならスキップ / Skip if fully equal
        if a[0] == b[0] and b[1] > a[1]:  # 次数が同じで個数が増加 / Degree same, count increased
            diffs.append(("count", a[0], b[1] - a[1]))
        elif a[1] == b[1] and b[0] > a[0]:  # 個数が同じで次数が増加 / Count same, degree increased
            diffs.append(("degree", a[1], b[0] - a[0]))
        else:
            return None  # それ以外は無効と見なす / Skip if other cases (complex change)
    return diffs

# count と degree が両方含まれているか確認する関数
# Check whether both count and degree changes are present
def is_count_and_degree_growth(diffs):
    has_count = any(d[0] == "count" for d in diffs)
    has_degree = any(d[0] == "degree" for d in diffs)
    return has_count and has_degree

# extract_diff で得た情報を使って予測パターンを生成
# Generate expected next pattern from p using diff info
def predict_next(p, diffs):
    predicted = []
    for a in p:
        modified = False  # 修正されたかどうかを追跡 / Track if element was modified
        for t, val, d in diffs:
            if t == "count" and a[0] == val:  # 次数が一致すれば個数を増加 / If degree matches, increment count
                predicted.append([a[0], a[1] + d])
                modified = True
            elif t == "degree" and a[1] == val:  # 個数が一致すれば次数を増加 / If count matches, increment degree
                predicted.append([a[0] + d, a[1]])
                modified = True
        if not modified:
            predicted.append(a[:])  # 変化がない場合はそのままコピー / Copy unchanged element
    return predicted

# 完全一致判定（順番も一致）
# Exact match including order
def is_exact_match(p1, p2):
    return all(a == b for a, b in zip(p1, p2))  # 全要素が順番も含め一致 / All elements match in order

# ユーザーから範囲とモードを取得
# Prompt user for n range and mode
n_start = int(input("Enter start value of n: ").strip())
n_end = int(input("Enter end value of n: ").strip())
mode = input("Select mode: (a)ll, (e)ven only, (o)dd only: ").strip().lower()

# モードに基づきステップを決定
# Determine step based on mode
if mode == 'a':
    step = 1
elif mode == 'e':
    step = 2
    if n_start % 2 != 0:
        n_start += 1  # 偶数に調整 / Adjust to even
elif mode == 'o':
    step = 2
    if n_start % 2 != 1:
        n_start += 1  # 奇数に調整 / Adjust to odd
else:
    print("Error: Invalid mode. Use a, e, or o.")
    exit(1)

# 範囲が不正な場合は終了
# Exit if range is invalid
if n_end <= n_start:
    print("Error: Invalid range. Start must be less than end.")
    exit(1)

# 対象の n 値をリストに格納
# Generate list of n values to use
n_values = list(range(n_start, n_end + 1, step))  # モードに応じた n のリスト / Generate n list with appropriate step

# 各 n に対してパターンを読み込む
# Load all pattern lists in range
all_patterns = {}
for n in n_values:
    all_patterns[n] = load_patterns(n)  # 各 n に対応するパターンを辞書に格納 / Store patterns in dict

print(f"\n--- Searching for full chains from n={n_values[0]} to n={n_values[-1]} (mode: {mode}) ---\n")

# 最初の n を起点にしてチェインを探す
# Start from first n in n_values
for p1 in all_patterns[n_values[0]]:
    for p2 in all_patterns[n_values[1]]:
        if len(p1) != len(p2):
            continue
        diffs = extract_diff(p1, p2)
        if not diffs:
            continue  # 有効な差分がなければスキップ / Skip if no valid diff found
        chain = [(n_values[0], p1), (n_values[1], p2)]  # チェイン初期化 / Initialize chain
        current = p2
        success = True
        for i in range(2, len(n_values)):
            next_n = n_values[i]
            predicted = predict_next(current, diffs)  # 次のパターンを予測 / Predict next pattern
            match_found = False
            for candidate in all_patterns[next_n]:
                if len(candidate) == len(predicted) and is_exact_match(candidate, predicted):
                    chain.append((next_n, candidate))  # チェインに追加 / Append to chain
                    current = candidate
                    match_found = True
                    break
            if not match_found:
                success = False  # 一致するパターンがなければ中断 / Break if no match found
                break
        if success:
            # countとdegreeの両成長がある場合は$、そうでなければ#で表示
            # Use $ if both count and degree grow
            marker = "$" if is_count_and_degree_growth(diffs) else "#"
            print(f"{marker} Chains:")
            for step_n, pat in chain:
                print(f"n{step_n}: {format_pattern(pat)}")
            print("---")
