#include "andres/graph/graph.hxx"
#include "andres/graph/multicut/kernighan-lin.hxx"
#include "andres/graph/multicut/greedy-additive.hxx"

#include "util.hxx"

// argv[1] -> edge weights
// argv[2] -> graph
// argv[3] -> out file
// argv[4] -> greedy warmstart
int main(int argc, char* argv[]) {
    
    std::string edgeIn = argv[1];
    std::vector<double> edgeValues = readEdges( edgeIn );
    std::string graphIn = argv[2];
    andres::graph::Graph<> graph   = readGraph( graphIn );

    std::vector<char> edgeLabels( graph.numberOfEdges() );
   
    bool greedy_ws = std::atoi(argv[4]);
    if(greedy_ws) {
        andres::graph::multicut::greedyAdditiveEdgeContraction(graph, edgeValues, edgeLabels);
    }

    andres::graph::multicut::kernighanLin(graph, edgeValues, edgeLabels, edgeLabels);

    std::string edgeOut = argv[3];
    writeEdges(edgeLabels, edgeOut );

    return 0;
}
