#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random
from statistics import mean # this allows us to take a mean of a list easily

# Arrivals generator function
def patient_generator_weight_loss(env, wl_inter, mean_consult, nurse):
    while True:        
        wp = activity_generator_weight_loss(env, mean_consult, nurse)
        
        env.process(wp)
        
        t = random.expovariate(1.0 / wl_inter)
        
        yield env.timeout(t)
        
# Activity generator function
def activity_generator_weight_loss(env, mean_consult, nurse):
    # Strictly speaking, variables referenced outside of a function, and which
    # aren't passed in, don't exist in the eyes of the function.
    # This means that if we were to refer to a variable that we haven't passed
    # in, and we make any sort of change to it, it will set up a NEW variable
    # with the same name INSIDE the function.  Usually, we don't want that.
    # By using the global keyword, we declare that the
    # list_of_queuing_times_nurse list that we're referring to here is the same
    # one we've declared OUTSIDE of the function (ie towards the bottom of the
    # code) and not a new one.  So when we add something to it here, it adds
    # it to the global list, not a brand new list with the same name.
    global list_of_queuing_times_nurse
    
    time_entered_queue_for_nurse = env.now
    
    with nurse.request() as req:
        yield req
        
        time_left_queue_for_nurse = env.now
        time_in_queue_for_nurse = (time_left_queue_for_nurse -
                                   time_entered_queue_for_nurse)
        
        # Append the calculated time in queue for this patient to our
        # global list of queuing times for all patients
        list_of_queuing_times_nurse.append(time_in_queue_for_nurse)
        
        sampled_consultation_time = random.expovariate(1.0 / mean_consult)
        
        yield env.timeout(sampled_consultation_time)
        
# Set up simulation environment
env = simpy.Environment()

# Set up resources
nurse = simpy.Resource(env, capacity=1)

# Set up parameter values
wl_inter = 5
mean_consult = 6

# Set up a list to store queuing times for the nurse
list_of_queuing_times_nurse = []

# Start the arrivals generator
env.process(patient_generator_weight_loss(env, wl_inter, mean_consult, nurse))

# Run the simulation
env.run(until=120)

# Calculate and print mean queuing time for the nurse
mean_queue_time_nurse = mean(list_of_queuing_times_nurse)
print ("Mean queuing time for nurse (mins) : ", 
       round(mean_queue_time_nurse, 2), sep="")