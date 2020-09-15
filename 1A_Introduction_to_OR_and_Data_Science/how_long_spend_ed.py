#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:54:44 2019

@author: dan
"""

import simpy
import random

# Our patient arrivals generator
def arrival_generator(env, mean_interarrival_time, receptionist, triage_nurse,\
                      treatment_cubicle, mean_registration_time, \
                      mean_triage_time, mean_treatment_time):
    # Keep generating until the simulation finishes
    while True:
        # Create a new patient with the necessary attributes
        p = ed_patient(env, receptionist, triage_nurse, treatment_cubicle, \
                       mean_registration_time, mean_triage_time, \
                       mean_treatment_time)
        
        # Have the environment process the new patient (bring into being)
        env.process(p)
        
        # Randomly sample the time until the next patient arrives and have the 
        # generator function timeout until then
        # We'll use an exponential distribution here
        t = random.expovariate(1.0 / mean_interarrival_time)
        
        # Activate the timeout
        yield env.timeout(t)
        
# The function that defines the journey of an ED patient
def ed_patient(env, receptionist, triage_nurse, treatment_cubicle, \
               mean_registration_time, mean_triage_time, mean_treatment_time):
    # Patient enters queue for receptionist
    # Record the time the patient entered the queue
    time_ent_q_for_recep = env.now
    
    # Record the time the patient entered the system
    time_ent_system = env.now
    
    # Request a receptionist resource and do these things only once one is
    # available
    with receptionist.request() as req:
        yield req
        
        # Record the time the patient left the queue for the receptionist
        time_left_q_for_recep = env.now
        
        # Calcuate the time spent in the queue for the receptionist and add
        # to the list of queuing times
        list_of_q_recep.append(time_left_q_for_recep - time_ent_q_for_recep)
        
        # Randomly sample time patient spends with receptionist
        time_with_recep = random.expovariate(1.0 / mean_registration_time)
        
        # Timeout the function until the patient has finished registration
        yield env.timeout(time_with_recep)
        
    # Patient enters queue for triage nurse
    # Record the time the patient entered the queue
    time_ent_q_for_triage = env.now
    
    # Request a triage nurse resource and do these things only once one is
    # available
    with triage_nurse.request() as req:
        yield req
        
        # Record the time the patient left the queue for the triage nurse
        time_left_q_for_triage = env.now
        
        # Calculate the time spent in the queue for the triage nurse and add
        # to the list of queuing times
        list_of_q_triage.append(time_left_q_for_triage - time_ent_q_for_triage)
        
        # Randomly sample time patient spends with triage nurse
        time_in_triage = random.expovariate(1.0 / mean_triage_time)
        
        # Timeout the function until the patient has finished triage
        yield env.timeout(time_in_triage)
        
    # Patient enters queue for treatment cubicle
    # Record the time the patient entered the queue
    time_ent_q_for_treat = env.now
    
    # Request a treatment cubicle resource and do these things only once one is
    # available
    with treatment_cubicle.request() as req:
        yield req
        
        # Record the time the patient left the queue for treatment
        time_left_q_for_treat = env.now
        
        # Calculate the time spent in the queue for treatment and add
        # to the list of queuing times
        list_of_q_treat.append(time_left_q_for_treat - time_ent_q_for_treat)
        
        # Randomly sample time patient spends in treatment cubicle
        time_in_treatment = random.expovariate(1.0 / mean_treatment_time)
        
        # Timeout the function until the patient has finished treatment
        yield env.timeout(time_in_treatment)
        
    # Record the time the patient left the system
    time_left_system = env.now
    
    # Calculate the total time the patient was in the system and append it
    # to the list of times in system
    list_of_system_times.append(time_left_system - time_ent_system)
    
# Set up environment
env = simpy.Environment()

# Set up resources
receptionist = simpy.Resource(env, capacity=1)
triage_nurse = simpy.Resource(env, capacity=2) # base = 2
treatment_cubicle = simpy.Resource(env, capacity=4) # base = 4

# Specify distribution parameters
mean_interarrival_time = 8
mean_registration_time = 2
mean_triage_time = 5
mean_treatment_time = 30

# Set up lists of queuing times
list_of_q_recep = []
list_of_q_triage = []
list_of_q_treat = []
list_of_system_times = []

# Launch the patient generator
env.process(arrival_generator(env, mean_interarrival_time, receptionist,\
                              triage_nurse, treatment_cubicle, \
                              mean_registration_time, mean_triage_time, \
                              mean_treatment_time))

# Run the simulation for one year (525,600 minutes)
env.run(until=525600)

# Calculate the average queuing time for each activity
mean_queuing_time_reception = sum(list_of_q_recep) / len(list_of_q_recep)
mean_queuing_time_triage_nurse = sum(list_of_q_triage) / len(list_of_q_triage)
mean_queuing_time_treatment = sum(list_of_q_treat) / len(list_of_q_treat)

# Print the average queuing time results
print ("Average queuing time for reception : ", \
       round(mean_queuing_time_reception, 2), " minutes.", sep="")
print ("Average queuing time for triage    : ", \
       round(mean_queuing_time_triage_nurse, 2), " minutes.", sep="")
print ("Average queuing time for treatment : ", \
       round(mean_queuing_time_treatment, 2), " minutes.", sep="")

# Calculate the average time in system across patients
mean_time_in_system = sum(list_of_system_times) / len(list_of_system_times)

# Print the average time in system results
print ("Average time in system : ", round(mean_time_in_system, 2),\
       " minutes.", sep="")

