#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 11:11:30 2020

@author: sean
"""

import networkx as nx
import pandas as pd
import holoviews as hv
from holoviews import opts, dim

#Read in game of thrones data
nodes = pd.read_csv('data/got-s1-nodes.csv', low_memory=False)
edges = pd.read_csv('data/got-s1-edges.csv', low_memory=False)

# Specify the plot render to use
hv.extension('bokeh')
hv.output(size=300)

# Chord diagram with interactive components
edgeList = edges[['Source','Target','weight']]
nodeDS = hv.Dataset(nodes,'Id')
chord = hv.Chord((edgeList, nodeDS))
chord.opts(
        opts.Chord(inspection_policy='nodes', tools=['hover'],
                   edge_hover_line_color='green', node_hover_fill_color='red'))
hv.save(chord,'simple_chord.html')

# Coloured interactive chord diagram
kwargs = dict(width=300, height=300, xaxis=None, yaxis=None)
opts.defaults(opts.Nodes(**kwargs), opts.Graph(**kwargs))

graph = hv.Graph((edgeList, nodeDS), label='GoT season 1')

graph.opts(cmap='Category20', edge_cmap='Category20', node_size=10, edge_line_width=1,
           node_color=dim('Id').str(), edge_color=dim('Source').str())

hv.save(graph, 'coloured_chord.html')

# Facebook data as graph with predifined coordinate system
kwargs = dict(width=300, height=300, xaxis=None, yaxis=None)
opts.defaults(opts.Nodes(**kwargs), opts.Graph(**kwargs))

colors = ['#000000']+hv.Cycle('Category20').values
edges_df = pd.read_csv('data/fb_edges.csv')
fb_nodes = hv.Nodes(pd.read_csv('data/fb_nodes.csv')).sort()
fb_graph = hv.Graph((edges_df, fb_nodes), label='Facebook Circles')

fb_graph.opts(cmap=colors, node_size=10, edge_line_width=1,
              node_line_color='gray', node_color='circle')

hv.save(fb_graph, 'fb_graph.html')

# Bundled graph of facebook data
from holoviews.operation.datashader import datashade, bundle_graph
bundled = bundle_graph(fb_graph)
hv.save(bundled, 'fb_bundled.html')


