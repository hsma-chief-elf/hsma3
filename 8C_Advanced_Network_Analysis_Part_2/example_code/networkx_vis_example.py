#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:08:23 2020

@author: sean
"""

import networkx as nx
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts

# Create some simple graph data
nodes = {'ID':['1','2','3','4','5'],
         'Label':['1','2','3','4','5']}
edges = {'Source':['1','1','2','2','3','3','4','4','5','5'],
         'Target':['2','3','3','4','4','5','5','1','1','2'],
         'Weight':[3,6,4,7,8,2,4,3,2,5]}

nodes = pd.DataFrame(nodes)
edges = pd.DataFrame(edges)

#Create graph function - networkX
def create_graph(nodeData, edgeData):
    ## Initiate the graph object
    G = nx.Graph()
    
    ## Tranform the data into the correct format for use with NetworkX
    # Node tuples (ID, dict of attributes)
    idList = nodeData['ID'].tolist()
    labels =  pd.DataFrame(nodeData['Label'])
    labelDicts = labels.to_dict(orient='records')
    nodeTuples = [tuple(r) for r in zip(idList,labelDicts)]
    
    # Edge tuples (Source, Target, dict of attributes)
    sourceList = edgeData['Source'].tolist()
    targetList = edgeData['Target'].tolist()
    weights = pd.DataFrame(edgeData['Weight'])
    weightDicts = weights.to_dict(orient='records')
    edgeTuples = [tuple(r) for r in zip(sourceList,targetList,weightDicts)]
    
    ## Add the nodes and edges to the graph
    G.add_nodes_from(nodeTuples)
    G.add_edges_from(edgeTuples)
    
    return G

# Create the graph object
G = create_graph(nodes,edges)
# Define the node positions
pos = nx.circular_layout(G)
# Define the attribute inputs
n_size = [100,120,150,80,200]
n_col = ['#2c96c7','#32a852','#bd132f','#e6c315','#e315e6']
e_size = nx.get_edge_attributes(G,'Weight')
e_col = np.array(['#2c96c7','#32a852','#bd132f','#e6c315','#e315e6','#2c96c7','#32a852','#bd132f','#e6c315','#e315e6'])
shape = 'D'
alpha = 0.8
# Draw the graph and add edge labels
plot = nx.draw(G, pos, node_size=n_size, node_color=n_col, node_shape=shape, alpha=alpha, edge_color=e_col)
nx.draw_networkx_edge_labels(G,pos,edge_labels=e_size)





