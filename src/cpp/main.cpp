#include <iostream>
#include <tdzdd/DdStructure.hpp>
#include <tdzdd/util/Graph.hpp>

using tdzdd::Graph;
using namespace std;

int main(int argc, char **argv) {
    string file = string(argv[1]);
    Graph G;
    G.readEdges(file);

    for (int e = 0; e < G.edgeSize(); ++e) {
        cout << G.edgeInfo(e).v1 << " " <<G.edgeInfo(e).v2 << endl;
    }
}
