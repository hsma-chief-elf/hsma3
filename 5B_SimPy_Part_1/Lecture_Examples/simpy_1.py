#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random

# Arrivals generator function
def patient_generator_weight_loss(env, wl_inter, mean_consult, nurse):
    p_id = 0
    
    # Keep generating indefinitely
    while True:        
        # Create instance of activity generator
        wp = activity_generator_weight_loss(env, mean_consult, nurse, p_id)
        
        # Run the activity generator for this patient
        env.process(wp)
        
        # Sample time until next patient
        t = random.expovariate(1.0 / wl_inter)
        
        # Freeze until that time has passed
        yield env.timeout(t)
        
        p_id += 1
        
# Activity generator function
def activity_generator_weight_loss(env, mean_consult, nurse, p_id):
    time_entered_queue_for_nurse = env.now
    print ("Patient ", p_id, " entered queue at ", 
           time_entered_queue_for_nurse, sep="")
    
    # Request a nurse
    with nurse.request() as req:
        # Freeze until the request can be met
        yield req
        
        # Calculate time patient was queuing
        time_left_queue_for_nurse = env.now
        print ("Patient ", p_id, " left queue at ", time_left_queue_for_nurse, 
               sep="")
        time_in_queue_for_nurse = (time_left_queue_for_nurse -
                                   time_entered_queue_for_nurse)
        print ("Patient ", p_id, " queued for ", time_in_queue_for_nurse,
               " minutes.", sep="")
        
        # Sample time spent with nurse
        sampled_consultation_time = random.expovariate(1.0 / mean_consult)
        
        # Freeze until that time has passed
        yield env.timeout(sampled_consultation_time)
        
# Set up simulation environment
env = simpy.Environment()

# Set up resources
nurse = simpy.Resource(env, capacity=1)

# Set up parameter values
wl_inter = 5
mean_consult = 6

# Start the arrivals generator
env.process(patient_generator_weight_loss(env, wl_inter, mean_consult, nurse))

# Run the simulation
env.run(until=120)

