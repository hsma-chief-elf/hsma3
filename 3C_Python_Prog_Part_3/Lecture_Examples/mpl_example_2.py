#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:25:28 2020

@author: dan
"""


import matplotlib as mpl # the matplotlib library
import matplotlib.pyplot as plt # provides matlab-style plotting interface

# Data to plot
x = [1,2,3,4,5,6,7,8,9,10]
y = [3,7,2,1,4,8,1,2,3,12]

# Create a figure object and an axes object, and add the axes object as a
# subplot of the figure object
figure_1, ax = plt.subplots()

# Set x axis and y axis labels
ax.set_xlabel('Time')
ax.set_ylabel('Number of patients')

# Plot our data (x and y here)
# Set plot to red and line style to --
ax.plot(x, y, color="red", linestyle="--")

# Show the figure
figure_1.show()

