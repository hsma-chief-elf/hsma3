#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:30:12 2019

@author: dan
"""

import numpy as np

# Store in three lists
ages = [18,19,22,23,24,27,29,31,34,46]
previous_admissions = [0,3,2,0,0,1,2,0,0,1]
admitted_this_time = [1,0,0,0,0,1,1,1,0,0]

# Combine into 2D NumPy Array
data = np.array([ages,previous_admissions,admitted_this_time])

# Calculate mean age using slicing of the NumPy array
mean_age = data[0].mean()
print ("Mean Age : ", round(mean_age, 1), sep="")

# Calculate total age of those admitted this time using slicing and 
# a dot product calculation
total_age_admitted_this_time = np.dot(data[0], data[2])
print ("Total Age of those admitted this time : ",
       total_age_admitted_this_time, sep="")

# Calculate mean number of previous admissions for those under 30 in the data
mean_prev_admissions_under_30 = data[1][0:7].mean()
print ("Mean Number of Readmissions for those under 30 : ", \
       round(mean_prev_admissions_under_30, 1), sep="")

