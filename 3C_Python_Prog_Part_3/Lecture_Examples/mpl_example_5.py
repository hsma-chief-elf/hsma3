#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:25:28 2020

@author: dan
"""


import matplotlib as mpl # the matplotlib library
import matplotlib.pyplot as plt # provides matlab-style plotting interface

# Data to plot
hsma_trainers = ["Dan", "Mike", "Kerry", "Sean", "Tom"]
hours_of_teaching = [54, 15, 6, 18, 15]

figure_1, ax = plt.subplots()

ax.set_xlabel("Trainer")
ax.set_ylabel("Hours of Teaching on HSMA")

ax.bar(hsma_trainers, hours_of_teaching)

figure_1.show()

