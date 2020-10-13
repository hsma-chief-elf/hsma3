#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:44:36 2019

@author: dan
"""

import pandas as pd

list_of_miu_numbers = [463,571,614,732,817]
list_of_locations = ["Lostwithiel","St Austell","Truro","Looe","Camborne"]
list_of_x_ray = [True,False,True,False,True]
list_of_opening_times = ["Morning","Afternoon","Afternoon","Morning","Evening"]

df_mius = pd.DataFrame()

df_mius['miu_number'] = list_of_miu_numbers
df_mius['location'] = list_of_locations
df_mius['x_ray_facilities'] = list_of_x_ray
df_mius['opening_time'] = list_of_opening_times

df_mius.set_index('miu_number', inplace=True)

print (df_mius.loc[[571,732]])
print ()
print (df_mius['location'])
print ()

list_of_mean_pts_seen_per_day = [4,3,3,1,2]

df_mius['mean_pts_per_day'] = list_of_mean_pts_seen_per_day

print (df_mius)
print ()

df2 = pd.DataFrame({"miu_number":[901], 
                    "location":["Callington"],
                    "x_ray_facilities":[True],
                    "opening_time":["Morning"],
                    "mean_pts_per_day":[5]})
df2.set_index('miu_number', inplace=True)

df_mius = df_mius.append(df2)

print (df_mius)

