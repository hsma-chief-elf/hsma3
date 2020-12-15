#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 13:35:50 2020

@author: sean
"""

import networkx as nx
import pandas as pd
import holoviews as hv
from holoviews import opts, dim

nodes = pd.read_csv('data/got-s1-nodes.csv', low_memory=False)
edges = pd.read_csv('data/got-s1-edges.csv', low_memory=False)

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

# Create the graph object
G = create_graph(nodes,edges)

# Do an analysis
e_cent = nx.eigenvector_centrality(G)
page_rank = nx.pagerank(G)

# Extract the analysis output and convert to a suitable scale and format
e_cent_size = pd.DataFrame.from_dict(e_cent, orient='index',columns=['cent_value'])
e_cent_size.reset_index(drop=True, inplace=True)
e_cent_size = e_cent_size*100
page_rank_size = pd.DataFrame.from_dict(page_rank, orient='index',columns=['rank_value'])
page_rank_size.reset_index(drop=True, inplace=True)
page_rank_size = page_rank_size*1000

# Add the analysis data to the node dat input for the graph
nodes_extended = nodes.join([e_cent_size,page_rank_size])

# Now we switch to holoviews to render the plot
# Specify the plot render to use
hv.extension('bokeh')
hv.output(size=300)

# Chord diagram with interactive components
edgeList = edges[['Source','Target','weight']]
# Within the holoviews dataset object we define kdim and vdims
# Kdims are the independent variables which is Id in this example
# Vdims are dependent variables cent_value and rank_value
# By defining these here were can use them when creating the graph
nodeDS = hv.Dataset(nodes_extended,'Id',['cent_value','rank_value'])

# Coloured interactive chord diagram with node size determined by Vdims
kwargs = dict(width=300, height=300, xaxis=None, yaxis=None)
opts.defaults(opts.Nodes(**kwargs), opts.Graph(**kwargs))

graph = hv.Graph((edgeList, nodeDS), label='GoT season 1')
graph.opts(cmap='Category20', edge_cmap='Category20', node_size='cent_value', edge_line_width=1,
           node_color=dim('Id').str(), edge_color=dim('Source').str())
graph.opts(
    opts.Chord(inspection_policy='nodes', tools=['hover'],
                   edge_hover_line_color='green', node_hover_fill_color='red'))

hv.save(graph, 'node_size_chord.html')
