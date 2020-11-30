#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:08:09 2020

@author: sean
"""

import networkx as nx
import pandas as pd

#Create graph function
def create_graph(nodeData, edgeData):
    ## Initiate the graph object
    G = nx.Graph()
    
    ## Tranform the data into the correct format for use with NetworkX
    # Node tuples (ID, dict of attributes)
    idList = nodeData['Id'].tolist()
    labels =  pd.DataFrame(nodeData['Label'])
    labelDicts = labels.to_dict(orient='records')
    nodeTuples = [tuple(r) for r in zip(idList,labelDicts)]
    
    # Edge tuples (Source, Target, dict of attributes)
    sourceList = edgeData['Source'].tolist()
    targetList = edgeData['Target'].tolist()
    weights = pd.DataFrame(edgeData['weight'])
    weightDicts = weights.to_dict(orient='records')
    edgeTuples = [tuple(r) for r in zip(sourceList,targetList,weightDicts)]
    
    ## Add the nodes and edges to the graph
    G.add_nodes_from(nodeTuples)
    G.add_edges_from(edgeTuples)
    
    return G

#Read in data
nodesOne = pd.read_csv('data/got-s1-nodes.csv', low_memory=False)
edgesOne = pd.read_csv('data/got-s1-edges.csv', low_memory=False)

G = create_graph(nodesOne, edgesOne)

nx.degree(G)

nx.modularity_matrix(G)

nx.density(G)

list(nx.find_cliques(G))
nx.number_of_cliques(G)

nx.clustering(G)

nx.eigenvector_centrality(G)

nx.number_of_isolates(G)
nx.isolates(G)

nx.pagerank(G)

nx.shortest_path(G)

