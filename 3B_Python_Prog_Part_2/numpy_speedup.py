#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples of how numpy speed up computation.

For scientific applications you should aim to 
1. use numpy arrays over lists where possible
2. eliminate loops and use numpy built in functions and array operations 
(as these are written in C.)
"""

# Copy and paste each block to the console to run


#%%
import numpy as np

#%% 
#Example 1
# Lists versus arrays

python_list = list(range(1000000))
numpy_array = np.arange(1000000)


#%%
#baseline
%timeit sum(python_list)

#%%
#high performance
%timeit np.sum(numpy_array)
#%%

#Example 2: loops versus numpy array operations

#baseline peformance: loop through two arrays and create third array of values 
#added togeher

def add_two_arrays_demo(array1, array2, out):
    for i in range(len(array1)):
        out[i] = array1[i]+ array2[i]
        
a = np.arange(100)
b = np.arange(100)
sum_array = np.zeros(shape=100, dtype=np.float)

%timeit add_two_arrays_demo(a, b, sum_array)   

#%%

#high performance: just add numpy arrays together!
# Loops add overhead and are SLOW

a = np.arange(100)
b = np.arange(100)
sum_array = np.zeros(shape=100, dtype=np.float)

%timeit a + b

#%%
#Example 3: broadcasting demo

def add_scalar(array, to_add, out):
    for i in range(len(array)):
        out[i] = array[i] + to_add
     
a = np.arange(100)
sum_array = np.zeros(shape=100, dtype=np.float)
%timeit add_scalar(a, 100, sum_array)  

#%%

a = np.arange(100)
%timeit sum_array = a + 100

#%%