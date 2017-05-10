#pragma once

#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include <algorithm>

#include "andres/graph/graph.hxx"

std::vector<double> readEdges(const std::string & edgeFile) {
    //std::cout << "reading edge values from " << edgeFile << std::endl;
    
    std::vector<double> edgeValues;
    std::fstream reader(edgeFile, std::ios::in);

    // read edge values
    double val;
    while(reader >> val) {
        edgeValues.push_back(val);
    }
    
    auto minmax = std::minmax_element(edgeValues.begin(), edgeValues.end());
    //std::cout << "Read in " << edgeValues.size() << " edge-values in range: " << *(minmax.first) << " to " << *(minmax.second) <<  std::endl;

    return edgeValues;
}


andres::graph::Graph<> readGraph(const std::string & graphFile){
    //std::cout << "reading graph from " << graphFile << std::endl;
    
    std::vector< std::pair<int,int> > uvIds;
    std::fstream reader(graphFile, std::ios::in);
    
    // read uv ids, find n-nodes and build graph
    int u, v;
    size_t numNodes = 0;
    while(reader >> u >> v) {
        if(std::max(u,v) > numNodes) {
            numNodes = std::max(u,v);
        }
        uvIds.emplace_back(std::make_pair(u,v));
    }
    ++numNodes;
    
    andres::graph::Graph<> g(numNodes);
    for(const auto & uv : uvIds) {
        g.insertEdge(uv.first, uv.second);
    }

    //std::cout << "Read graph:" << std::endl;
    //std::cout << "#-nodes: " << g.numberOfVertices() << std::endl;
    //std::cout << "#-edges: " << g.numberOfEdges() << std::endl;

    return g;
}


template<class T>
void writeEdges(const std::vector<T> & values, const std::string & outFile) {
    //std::cout << "writing edge results to " << outFile << std::endl;
    std::ofstream writer(outFile, std::ios::out);
    for(auto val : values) {
        writer << +val << '\n';
    }
}
