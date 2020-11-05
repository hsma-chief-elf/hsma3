#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 10:49:51 2020

@author: sean
"""

import pandas as pd
import numpy as np

data = pd.read_csv("data/PD_Data_HSMA_2020.csv", low_memory = False)

print(data.head)

## Data cleaning
# Replace missing discharge dates with a date
data.ReferralDischarge.replace(np.nan, "18/02/2018", inplace=True)
# Replace missing values with None
data.replace(np.nan, "None", inplace=True)
# Remove rows without a referral date
data = data[data.ReferralDate != "None"]

# Convert dates to datetime format
data['ReferralDate'] = pd.to_datetime(data['ReferralDate'], format="%d/%m/%Y")
data['ReferralDischarge'] = pd.to_datetime(data['ReferralDischarge'], format="%d/%m/%Y")

# Calculate length of stay for all rows
data['LoSdays'] = (data.ReferralDischarge - data.ReferralDate).astype('timedelta64[D]')

# Remove rows with a negative length of stay
data = data[data.LoSdays >= 0]

# Sort the data by Client ID then by date
data = data.sort_values(['ClientID', 'ReferralDate'], ascending=[True, True])

# Amalgamate out of area services into a single category
data_ooa = data.copy(deep=True)
wardteam_np = data_ooa.WardTeam.values
setting_np = data_ooa.Setting.values
mask = setting_np =='OOA'
wardteam_np[mask] = str('All OOA services')
del data_ooa['WardTeam']
data_ooa['WardTeam'] = wardteam_np

# Transform categorical data columns to category type
data_sg = data_ooa.copy(deep=True)
data_sg['wardTeamCat'] = data_sg['WardTeam'].astype('category')
data_sg['wardTeamCatCode'] = data_sg['wardTeamCat'].cat.codes

## Create the adjacency matrix
n_wardteams = max(data_sg.wardTeamCatCode) + 1
servMove = np.zeros((n_wardteams, n_wardteams))
singles = np.zeros((1))

clientIDUni = data_sg.ClientID.unique()

for ID in clientIDUni:
    mask = data_sg.ClientID == ID
    cWardTeam = data_sg[mask].wardTeamCatCode
    n_services = len(cWardTeam)
    if (n_services > 1):
        for j in range(0, (n_services - 1)):
            servMove[int(cWardTeam.iloc[j]),int(cWardTeam.iloc[j + 1])] +=1
    else:
        singles = np.vstack((singles,ID))

np.savetxt('data/servMove_matrix.csv',servMove, delimiter=",")

## Create the edge list
edges = np.zeros((1,3))              
lenRow = servMove.shape[0]           
for i in range (0,lenRow):           
    for j in range(0,lenRow):
        if (int(servMove[j, i]) > 0):
            rowData = np.array([[j,i, int(servMove[j, i])]])
            edges = np.vstack((edges,rowData))
edges = edges.astype(int)
edges = edges[1:edges.shape[0], :]
lenEdge = edges.shape[0]

edgeType = np.repeat("Directed", lenEdge)
edgeid = np.arange(0, lenEdge)
edges = np.vstack((edges[:,0], edges[:,1], edgeType, edgeid, edges[:,2]))
edges = np.transpose(edges)
edgesdf = pd.DataFrame(edges, columns = ['Source', 'Target', 'Type', 'Id', 'Weight'])
edgesdf.to_csv('data/edge_list.csv', sep=',', index=False)

## Create the node list
losMean = data_sg.groupby('wardTeamCatCode')['LoSdays'].mean()
losMedian = data_sg.groupby('wardTeamCatCode')['LoSdays'].median()

df = pd.DataFrame()
df['wardTeamCat'] = data_sg.wardTeamCat
df['wardTeamCatCode'] = data_sg.wardTeamCatCode
df['Setting'] = data_sg.Setting

df = df.drop_duplicates(subset = ['wardTeamCat', 'wardTeamCatCode', 'Setting'])
df.sort_values('wardTeamCatCode', inplace=True)

nodes = np.vstack((df.wardTeamCatCode, df.wardTeamCat, 
                      losMean, losMedian, df.Setting))
nodes = np.transpose(nodes)
nodesdf = pd.DataFrame(nodes,columns = ['ID', 'Label', 'MeanLoS', 'MedianLoS', 'Setting'])

nodesdf.to_csv('data/node_list.csv', sep=',', index=False)
