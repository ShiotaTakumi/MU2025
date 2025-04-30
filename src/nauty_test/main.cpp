// 頂点数の最大値を定義する（100頂点までのグラフに対応）
// Define the maximum number of vertices (supports graphs with up to 100 vertices)
#define MAX_NODE 100

#include <iostream>
extern "C" {
    #include <nauty.h>
}
#include <vector>
using namespace std;

int main() {
    // 頂点数 n を標準入力から受け取る
    // Read the number of vertices n from standard input
    int n; 
    cout << "n: "; cin >> n;
    // cout << "Number of vertices: " << n << endl;

    // nauty が内部的にグラフをビット列で表現するために必要な配列サイズ (word 数) を計算する
    // Compute the number of setwords needed to represent n vertices in nauty's internal bitset format
    int m = SETWORDSNEEDED(n);
    // cout << "Number of vertices: " << m << endl;

    // グラフ構造を表す配列（隣接行列）を定義する（MAXN 頂点まで対応）
    // Define the graph structure as an adjacency matrix (supports up to MAX_NODE vertices)
    graph g[MAX_NODE * MAX_NODE];

    // 空グラフ（辺のないグラフ）で初期化する
    // Initialize the graph as an empty graph (no edges)
    EMPTYGRAPH(g, m, n);

    // 頂点 i と j (i < j) のすべての組み合わせを列挙し、完全グラフ K_n の全ての辺を生成する
    // Generate all possible edges (i, j) with i < j to form the complete graph K_n
    vector<pair<int,int>> edges;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            edges.emplace_back(i, j); // (i, j) を辺として保存
        }
    }
    // for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) cout << "(" << i << "," << j << ") \n";

    // 辺の本数を取得する
    // Get the number of edges
    int num_edges = edges.size();

    // 辺の有無をビットで表現し、全ての部分グラフ（辺の組合せ）を列挙する
    // ⚠️ "bit" という変数名は絶対に使わないこと ⚠️
    // Enumerate all subsets of edges as bit patterns representing the presence or absence of each edge
    // ⚠️ Use of "bit" as a variable name is strictly prohibited! ⚠️
    for (int mask = 0; mask < (1 << num_edges); ++mask) {
        // 空グラフ（辺のないグラフ）で初期化する
        // Initialize the graph as an empty graph (no edges)
        EMPTYGRAPH(g, m, n);
        for (int i = 0; i < num_edges; ++i) {
            // i 番目の辺がこの部分グラフに含まれるかを確認する
            // Check whether the i-th edge is included in the current subgraph
            if (mask & (1 << i)) {
                auto [v, w] = edges[i];
                // 辺 (v, w) をグラフに追加する
                // Add the edge (v, w) to the graph
                ADDONEEDGE(g, v, w, m);
            }
        }
    }
}
