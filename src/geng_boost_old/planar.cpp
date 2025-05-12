#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/boyer_myrvold_planar_test.hpp>

using namespace std;
using namespace boost;

int main() {
    // Boost グラフライブラリの基本グラフ型を定義
    // Define the basic graph type using Boost's adjacency list
    using Graph = adjacency_list<vecS, vecS, undirectedS>;

    string line;                    // 1 行ずつ読み込む文字列 / String to read each line
    vector<pair<int, int>> edges;   // 辺の集合（u, v） / List of edges (u, v)
    int n = 0;                      // グラフの頂点数 / Number of vertices
    string graph6_line;             // graph6 形式の文字列表現 / The graph6 representation

    // 標準入力からデータを 1 行ずつ読み込む
    // Read data from standard input line by line
    while (getline(cin, line)) {
        // 空行が来たときの処理（1 つのグラフ情報の終端を示す）
        // When a blank line is encountered (end of one graph block)
        if (line.empty()) {
            // 辺の情報から Boost グラフを構築
            // Build Boost graph from edge list
            Graph G(n);
            for (auto& [u, v] : edges) add_edge(u, v, G);

            // グラフの平面性を判定
            // Test whether the graph is planar
            if (boyer_myrvold_planarity_test(G)) {
                // 平面グラフであれば graph6 文字列を出力
                // If planar, output the original graph6 string
                cout << graph6_line << "\n";
            }

            // 次のグラフの入力に備えて情報をリセット
            // Clear data for next graph
            edges.clear();
            graph6_line.clear();
            continue;
        }

        // "# n m" 行：n 頂点 m 辺のグラフという情報を取得
        // "# n m" line: number of vertices n and edges m
        if (line[0] == '#') {
            istringstream iss(line.substr(1));
            int m;
            iss >> n >> m;
        }
        // graph6 文字列（ASCII コード 'A' 以上から始まる）
        // graph6 string line (starts with ASCII >= 'A')
        else if (line[0] >= 'A') {
            graph6_line = line;
        }
        // "u v" 行：頂点 u, v の辺を読み込む
        // "u v" line: parse an edge between vertices u and v
        else {
            istringstream iss(line);
            int u, v;
            iss >> u >> v;
            edges.emplace_back(u, v);
        }
    }
}
