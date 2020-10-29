#!/usr/bin/env python
# coding: utf-8

# # Practical 1: Exploring time series data

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# **Step 1: Import emergency department reattendance data.**  
# 
# This is a time series from a hospital that measures the number of patients per month that have reattended an ED within 7 days of a previous attendance.
# 
# This can be found in **"data/ed_reattend.csv"**
# 
# * Hint 1: look back at the lecture notes and see how `pd.read_csv()` was used.  
# 
# * Hint 2: The format of the 'date' column is in UK standard dd/mm/yyyy.  You will need to set the `dayfirst=True` of `pd.read_csv()` to make sure pandas interprets the dates correctly.
# 
# * Hint 3: The data is monthly and the dates are all the first day of the month.  This is called monthly start and its shorthand is 'MS'

# In[ ]:


#your code here


# **Step 2: Check the shape of the `DataFrame` and print out the first 5 observations**

# In[ ]:


#your code here


# **Step 3: Check the minimum and maximum date of the series**
# 
# 

# In[ ]:


#your code here


# **Step 4: Create a basic plot of the time series**

# In[ ]:


#your code here


# **Step 5: Improve the appearance of your chart**
#     
# Try the following:
#     
# * Add a y-axis label
# * Add gridlines to the plot
# * Add markers to block
# * Change the colour of the line
# * Experiment with using seaborn

# In[ ]:


#your code here


# **Step 6: Perform a calender adjustment**
# 
# The data is at the monthly level.  Therefore some of the noise in the time series is due to the differing number of days per month.  Perform a calender adjust and plot the daily rate of reattendance.

# In[ ]:


#your code here


# **Step 7: Run a smoother through the series to assess trend**
# 
# Hint:  Try using the `.rolling` method of dataframe with a `window=12` and `center=True` to create a 12 month centred moving average 
# 
# Is there any benefit from switchoing to a 6 month MA?  Why does the 6-MA look different to the 12-MA.
# 
# Use the calender adjusted data.

# In[ ]:


#your code here


# **Step 8: Perform a seasonal decomposition on the time series**
# 
# Plot the trend, seasonal and remainder components of the decomposition.
# 
# Try both an additive and multiplicative model.  What is the difference between the two models?
# 
# * Hint: Look back at the lecture for a function to help you.
# 
# 
# 

# In[ ]:


#your code here

