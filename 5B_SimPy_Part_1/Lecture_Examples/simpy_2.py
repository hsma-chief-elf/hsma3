#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random

# Arrivals generator function
def patient_generator_ed(env, ed_inter, mean_register, mean_triage,
                         receptionist, nurse):
    p_id = 0
    
    while True:
        # Create new instance of activity generator
        p = activity_generator_ed(env, mean_register, mean_triage,
                                  receptionist, nurse, p_id)
        
        # Run the activity generator
        env.process(p)
        
        # Sample time to next arrival
        t = random.expovariate(1.0 / ed_inter)
        
        # Freeze until time elapsed
        yield env.timeout(t)
        
        p_id += 1

# Activity generator function
def activity_generator_ed(env, mean_register, mean_triage, receptionist,
                          nurse, p_id):
    time_entered_queue_for_registration = env.now
    
    # Request a receptionist
    with receptionist.request() as req:
        # Freeze until the request can be met
        yield req
        
        time_left_queue_for_registration = env.now        
        time_in_queue_for_registration = (time_left_queue_for_registration -
                                          time_entered_queue_for_registration)
        print ("Patient ", p_id, " queued for registration for ",
               time_in_queue_for_registration, " minutes.", sep="")
        
        # Sample the time spent in registration
        sampled_registration_time = random.expovariate(1.0 / mean_register)
        
        # Freeze until that time has elapsed
        yield env.timeout(sampled_registration_time)
        
    # Here, we're outside of the with statement, and so have just finished
    # with the receptionist.  Which means we've started queuing for the nurse.
    # So we just do exactly as we did before for the next activity in our
    # system.
    time_entered_queue_for_triage = env.now
    
    # Request a nurse
    with nurse.request() as req:
        # Freeze until the request can be met
        yield req
        
        time_left_queue_for_triage = env.now
        time_in_queue_for_triage = (time_left_queue_for_triage -
                                    time_entered_queue_for_triage)
        print ("Patient ", p_id, " queued for triage for ",
               time_in_queue_for_triage, " minutes.", sep="")
        
        # Sample the time spent in triage
        sampled_triage_time = random.expovariate(1.0 / mean_triage)
        
        # Freeze until that time has elapsed
        yield env.timeout(sampled_triage_time)

# Set up simulation environment
env = simpy.Environment()

# Set up resources
receptionist= simpy.Resource(env, capacity=1)
nurse = simpy.Resource(env, capacity=2)

# Set up parameter values
ed_inter = 8
mean_register = 2
mean_triage = 5

# Start the arrivals generator
env.process(patient_generator_ed(env, ed_inter, mean_register, mean_triage, 
                                 receptionist, nurse))

# Run the simulation
env.run(until=2880)

