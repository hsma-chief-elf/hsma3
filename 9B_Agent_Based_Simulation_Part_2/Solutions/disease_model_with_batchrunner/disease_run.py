#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:08:18 2019

@author: dan
"""

"""Use this section for watching model run on a server with visualisation"""

#from disease_server import server
#server.port = 8521 # the default
#server.launch()

"""Use this section for running the model in batch runs"""

# Import everything from our disease_model module (all classes and functions)
from disease_model import *
# The arange function of numpy allows us to create evenly spaced numbers
# within a given interval - we'll use that below
from numpy import arange
# Import matplotlib so we can plot our results
import matplotlib.pyplot as plt
# Import the BatchRunner class so we can run our model in batch
from mesa.batchrunner import BatchRunner

# Set up a dictionary to store the attributes we want to keep fixed
fixed_params = {"width":10, 
                "height":10, 
                "initial_infection":0.8,
                "transmissibility":0.5, 
                "mean_length_of_disease":10,
                "mean_imm_duration":20, 
                "prob_being_immunised":0.05}

# Set up a dictionary to store the attributes we want to change between
# tested scenarios, and the values to test.  Here, we'll test different
# numbers of agents in the model between 2 and 100 (in increments of 1), and 
# different levels of movement from 0 to 1 in increments of 0.1
variable_params = {"N":range(2,100,1), 
                   "level_of_movement":arange(0.0,1.0,0.1)}

# Run each combination 5 times, for 365 days of simulated time
num_iterations = 5
num_steps = 365

# Set up a BatchRunner with the above information
batch_run = BatchRunner(Disease_Model, 
                        fixed_parameters=fixed_params,
                        variable_parameters=variable_params,
                        iterations=num_iterations,
                        max_steps=num_steps,
                        model_reporters=
                        {"Total_Infected":calculate_number_infected,
                         "Total_Imm":calculate_number_immunised}
                        )

# Tell the BatchRunner to run
batch_run.run_all()

# Store the results in a Pandas DataFrame
run_data = batch_run.get_model_vars_dataframe()

# Plot a scatter plot of level of movement vs total infected
plt.scatter(run_data.level_of_movement, run_data.Total_Infected)

