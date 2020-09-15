#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random
import csv
from statistics import mean
import pandas as pd

# Arrivals generator function
def patient_generator_dn(env, dn_inter, mean_visit, district_nurse):
    while True:        
        p = activity_generator_dn(env, mean_visit, district_nurse)
        
        env.process(p)
        
        t = random.expovariate(1.0 / dn_inter)
        
        yield env.timeout(t)
        
# Activity Generator
def activity_generator_dn(env, mean_visit, district_nurse):
    global list_of_queuing_times_dn
    global warm_up_period
    
    time_entered_queue_for_dn = env.now
    
    # Calculate how much resource to take from the container; here, this is
    # the number of district nurse minutes to remove (ie the visit duration)
    dn_mins_sampled = random.expovariate(1.0 / mean_visit)
    
    # We can use the level attribute of the container to find out the current
    # level of the container (how many hours in the pot here)
    print ("DN mins available before request : ", district_nurse.level)
    
    # When we want to take some quantity from the container, we can use the
    # get() method of the Container class, passing it the number of units of
    # resource we want to remove.  We use the yield keyword with the function
    # to tell the generator function to freeze in place until the requested
    # amount can be taken from the container.  If you omit the yield keyword,
    # the program will still appear to work, but no queues will form if there
    # are insufficient levels of resource in the container (because the
    # generator function will just carry on regardless)
    yield district_nurse.get(dn_mins_sampled)
    
    print ("DN mins available after request : ", district_nurse.level)
    
    # The patient has now left the queue as we've got the district nurse hours
    # at this point
    time_left_queue_for_dn = env.now
    time_queuing_for_dn = (time_left_queue_for_dn - time_entered_queue_for_dn)
    list_of_queuing_times_dn.append(time_queuing_for_dn)
    
    # Call the timeout for the length of the visit (obviously here that's the
    # same as the amount of resource we've taken from the container, but
    # that won't always be the case in all models)
    yield env.timeout(dn_mins_sampled)
    
    # Once the visit duration has elapsed, we'll be back here in the function.
    # So we can now put back the minutes into the container using the put()
    # method of the container class.  Again we need to use the yield keyword.
    yield district_nurse.put(dn_mins_sampled)

# Set up number of times to the run the simulation
number_of_simulation_runs = 100

# Specify the results collection and warm up period for each simulation run
results_collection_period = 1440
warm_up_period = 2880

# Create a file to store the results of each run, and write the column headers
with open("dn_results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    
    writer.writerow(["Run", "Mean Q DN"])

for run in range(number_of_simulation_runs):
    # Set up simulation environment
    env = simpy.Environment()
    
    # Set up the container, passing in the environment, the initial level of
    # the container, and the maximum capacity of the container.  Here, it
    # makes sense to keep these the same (if we've put back more district
    # nurse hours than we took then something's gone wrong!), but in some
    # situations you may want your container to go above the initial level
    district_nurse = simpy.Container(env, init=1000, capacity=1000)
    
    # Set up parameter values
    dn_inter = 10
    mean_visit = 60
    
    # Set up list to store queuing times
    list_of_queuing_times_dn = []
    
    # Start the arrivals generator
    env.process(patient_generator_dn(env, dn_inter, mean_visit, 
                                     district_nurse))
    
    # Run the simulation for the warm up period + the results collection period
    env.run(until=(results_collection_period + warm_up_period))
    
    # Calculate and print average queuing time
    mean_queuing_time_dn = mean(list_of_queuing_times_dn)
    
    print ("Mean queuing time for the district nurse (mins) : ",
           mean_queuing_time_dn, sep="")
    
    # Set up list to write to file - here we'll store the run number alongside
    # the mean queuing time for the nurse in that run
    list_to_write = [run, mean_queuing_time_dn]
    
    # Store the run results to file.  We need to open in append mode ("a"),
    # otherwise we'll overwrite the file each time.  That's why we set up the
    # new file before the for loop, to start anew for each batch of runs
    with open("dn_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",")
        
        writer.writerow(list_to_write)
        
# After the batch of runs is complete, we might want to read the results back
# in and take some summary statistics
# Here, we're going to use a neat shortcut for easily reading a csv file into
# a pandas dataframe
results_df = pd.read_csv("dn_results.csv")

# We may want to take the average queuing time across runs
mean_trial_queuing_time_dn = results_df["Mean Q DN"].mean()
print ("Mean queuing time over trial : ", 
       round(mean_trial_queuing_time_dn, 2))

# Maybe the max and min run results too
max_trial_queuing_time_dn = results_df["Mean Q DN"].max()
min_trial_queuing_time_dn = results_df["Mean Q DN"].min()
print ("Max mean queuing result over trial : ",
       round(max_trial_queuing_time_dn, 2))
print ("Min mean queuing result over trial : ", 
       round(min_trial_queuing_time_dn, 2))

