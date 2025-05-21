#!/usr/bin/env python3

from collections import Counter  # 次数分布の頻度集計に使用 / For counting frequency of degrees
import os  # ファイル操作・存在確認に使用 / For file handling and path checking

# Shift 距離関数の定義
# 1つずれた次数をコスト1として扱い、近接した構造の類似性を評価
# Define the shift distance function
# Treat degree +/-1 shifts as cost-1 and evaluate similarity
def shift_distance(c1, c2):
    c1 = c1.copy()  # 入力を破壊しないようコピー / Copy input to avoid modifying original
    c2 = c2.copy()
    distance = 0  # 距離の初期値 / Initialize distance

    # 完全一致部分を削除
    # Cancel out exact matches
    for k in list(c1.keys()):
        common = min(c1[k], c2.get(k, 0))
        c1[k] -= common
        c2[k] -= common
        if c1[k] == 0:
            del c1[k]
        if c2.get(k, 0) == 0:
            c2.pop(k, None)

    # ±1 の次数シフトを処理
    # Handle off-by-one shifts
    for k in list(c1.keys()):
        for dk in [-1, 1]:  # 隣接次数を調査 / Check neighbors
            neighbor = k + dk
            if neighbor in c2:
                shift = min(c1[k], c2[neighbor])
                c1[k] -= shift
                c2[neighbor] -= shift
                distance += shift  # コスト1として加算 / Count as cost 1
                if c1[k] == 0:
                    del c1[k]
                if c2[neighbor] == 0:
                    del c2[neighbor]

    # 残りの unmatched を L1 距離として加算
    # Add unmatched as L1 distance
    all_keys = set(c1) | set(c2)
    for k in all_keys:
        distance += abs(c1.get(k, 0) - c2.get(k, 0))

    return distance

# 次数分布文字列を Counter に変換
# Convert degree pattern string to Counter
def parse_degree_pattern(line):
    # 入力文字列をスペースで分割し、[次数, 個数] に変換
    # Parse and map [degree,count]
    parts = line.strip().split(" ")
    return Counter({int(p[1]): int(p[3]) for p in parts})

# 頂点数の範囲をユーザーから取得
# Prompt user for start and end n values
n_start = int(input("Enter the start number of vertices (e.g., 8): ").strip())
n_end = int(input("Enter the end number of vertices (e.g., 11): ").strip())

# モード（全体 / 偶数のみ / 奇数のみ）を取得
# Ask user for filtering mode
mode = input("Select mode: (a)ll, (e)ven only, (o)dd only: ").strip().lower()

# 全ての n に対するパターンを格納する辞書
# Dictionary to store all patterns
all_patterns = {}

# 指定範囲でファイルを読み込む
# Load degree pattern files for each n in range
for n in range(n_start, n_end + 1):
    # 偶数モードで奇数ならスキップ
    # Skip odd if even-only
    if mode == 'e' and n % 2 != 0:
        continue
    # 奇数モードで偶数ならスキップ
    # Skip even if odd-only
    if mode == 'o' and n % 2 != 1:
        continue

    # ファイルパスの構築
    # Construct file path
    path = f"degree_unique/n{n}.txt"

    # ファイル存在チェック
    # Check if file exists
    if not os.path.exists(path):
        continue

    # ファイルを開いて内容を読み込む
    # Read patterns from file
    with open(path, "r") as f:
        patterns = [line.strip() for line in f if line.strip()]
    # 各パターンを Counter に変換して保存
    # Store as (line, Counter)
    all_patterns[n] = [(line, parse_degree_pattern(line)) for line in patterns]

# 使用する頂点数の一覧を昇順に取得
# Get sorted list of valid n values
ns = sorted(all_patterns.keys())

# 距離1の連鎖を出力
# Print chains with shift distance = 1
print("\nValid chains with shift distance = 1 between each step:\n")
for line0, c0 in all_patterns.get(ns[0], []):
    chain = [(ns[0], line0)]  # 初期パターンを登録 / Initialize chain
    current_pattern = c0
    valid = True  # チェイン有効フラグ / Validity flag

    # 次の n 値へ連続してたどる
    # Traverse subsequent n values
    for i in range(1, len(ns)):
        n = ns[i]
        found = False
        for line_next, c_next in all_patterns[n]:
            # 同じ種類数かつ距離1ならチェインに追加
            # Same length and shift=1
            if len(current_pattern) == len(c_next) and shift_distance(current_pattern, c_next) == 1:
                chain.append((n, line_next))
                current_pattern = c_next
                found = True
                break
        if not found:
            valid = False  # 中断されたら終了 / Chain broken
            break

    # 成功したチェインを表示
    # Print valid chain
    if valid:
        for step_n, pat in chain:
            print(f"n={step_n}: {pat}")
        print("---")

# 距離2の連鎖を出力
# Print chains with shift distance = 2
print("\nValid chains with shift distance = 2 between each step:\n")
for line0, c0 in all_patterns.get(ns[0], []):
    chain = [(ns[0], line0)]
    current_pattern = c0
    valid = True

    # 次の n 値へ連続してたどる
    # Traverse subsequent n values
    for i in range(1, len(ns)):
        n = ns[i]
        found = False
        for line_next, c_next in all_patterns[n]:
            # 同じ種類数かつ距離2ならチェインに追加
            # Same length and shift=2
            if len(current_pattern) == len(c_next) and shift_distance(current_pattern, c_next) == 2:
                chain.append((n, line_next))
                current_pattern = c_next
                found = True
                break
        if not found:
            valid = False  # 中断されたら終了 / Chain broken
            break

    # 成功したチェインを表示
    # Print valid chain
    if valid:
        for step_n, pat in chain:
            print(f"n={step_n}: {pat}")
        print("---")
