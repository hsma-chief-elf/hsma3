#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:25:28 2020

@author: dan
"""


import matplotlib as mpl # the matplotlib library
import matplotlib.pyplot as plt # provides matlab-style plotting interface

# Data to plot
a = [11,52,61,72,83,12,23,31,46]
b = [23,61,65,81,60,15,29,40,42]

figure_1, ax = plt.subplots()

ax.set_xlabel("Variable a")
ax.set_ylabel("Variable b")

ax.scatter(a, b)

figure_1.show()

