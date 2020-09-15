#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:25:28 2020

@author: dan
"""


import matplotlib as mpl # the matplotlib library
import matplotlib.pyplot as plt # provides matlab-style plotting interface

# Data to plot
time = [1,2,3,4,5,6,7,8,9,10]

patients = [3,7,2,1,4,8,1,2,3,12]
doctors = [2,0,1,2,1,1,1,2,0,1]

# Create a figure object and an axes object, and add the axes object as a
# subplot of the figure object
figure_1, ax = plt.subplots()

# Set x axis and y axis labels
ax.set_xlabel('Time')
ax.set_ylabel('Number in Clinic')

# Plot our data, and set each dataset we plot to a different colour / style
ax.plot(time, patients, color="blue", linestyle="-", label="Patients")
ax.plot(time, doctors, color="red", linestyle=":", label="Doctors")

# Create and set up a legend
ax.legend(loc="upper left")

# Show the figure
figure_1.show()

figure_1.savefig("figure_1.pdf")

