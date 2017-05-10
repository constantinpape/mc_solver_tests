#include "andres/graph/graph.hxx"
#include "andres/graph/multicut/greedy-additive.hxx"

#include "util.hxx"

// argv[1] -> edge weights
// argv[2] -> graph
// argv[3] -> out file
int main(int argc, char* argv[]) {
    
    std::string edgeIn = argv[1];
    std::vector<double> edgeValues = readEdges( edgeIn );
    std::string graphIn = argv[2];
    andres::graph::Graph<> graph   = readGraph( graphIn );

    std::vector<char> edgeLabels( graph.numberOfEdges() );
    andres::graph::multicut::greedyAdditiveEdgeContraction(graph, edgeValues, edgeLabels);
    
    std::string edgeOut = argv[3];
    writeEdges(edgeLabels, edgeOut );

    return 0;
}
