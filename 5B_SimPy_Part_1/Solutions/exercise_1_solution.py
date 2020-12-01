#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random
from statistics import mean
import matplotlib.pyplot as plt

# Arrivals generator function
def patient_generator_gp(env, gp_inter, mean_register, mean_consult,
                         mean_book_test, receptionist, gp):
    while True:
        p = activity_generator_gp(env, mean_register, mean_consult,
                                  mean_book_test, receptionist, gp)
        
        env.process(p)
        
        t = random.expovariate(1.0 / gp_inter)
        
        yield env.timeout(t)
        
# Activity generator function
def activity_generator_gp(env, mean_register, mean_consult, mean_book_test,
                          receptionist, gp):
    global list_of_queuing_times_registration
    global list_of_queuing_times_consultation
    global list_of_queuing_times_book_test
    global list_of_times_in_system
    
    time_entered_system = env.now
    time_entered_queue_for_registration = env.now
    
    with receptionist.request() as req:
        yield req
        
        time_left_queue_for_registration = env.now
        time_in_queue_for_registration = (time_left_queue_for_registration -
                                          time_entered_queue_for_registration)
        list_of_queuing_times_registration.append(
            time_in_queue_for_registration)
        
        sampled_registration_time = random.expovariate(1.0 / mean_register)
        
        yield env.timeout(sampled_registration_time)
    
    time_entered_queue_for_gp = env.now
    
    with gp.request() as req:
        yield req
        
        time_left_queue_for_gp = env.now
        time_in_queue_for_gp = (time_left_queue_for_gp -
                                time_entered_queue_for_gp)
        list_of_queuing_times_consultation.append(
            time_in_queue_for_gp)
        
        sampled_consult_time = random.expovariate(1.0 / mean_consult)
        
        yield env.timeout(sampled_consult_time)
        
    decide_test_needed = random.uniform(0,1)
    
    if decide_test_needed < 0.25:
        time_entered_queue_for_book_test = env.now
        
        with receptionist.request() as req:
            yield req
            
            time_left_queue_for_book_test = env.now
            time_in_queue_for_book_test = (time_left_queue_for_book_test -
                                           time_entered_queue_for_book_test)
            list_of_queuing_times_book_test.append(
                time_in_queue_for_book_test)
            
            sampled_book_test_time = random.expovariate(1.0 / mean_book_test)
            
            yield env.timeout(sampled_book_test_time)
            
    time_left_system = env.now
    time_in_system = (time_left_system - time_entered_system)
    list_of_times_in_system.append(time_in_system)
            
# Set up simulation environment
env = simpy.Environment()

# Set up resources
receptionist = simpy.Resource(env, capacity=1)
gp = simpy.Resource(env, capacity=2)

# Set up parameter values
gp_inter = 3
mean_register = 2
mean_consult = 8
mean_book_test = 4

# Lists to store queuing times and time in system across patients
list_of_queuing_times_registration = []
list_of_queuing_times_consultation = []
list_of_queuing_times_book_test = []
list_of_times_in_system = []

# Start the arrivals generator
env.process(patient_generator_gp(env, gp_inter, mean_register, mean_consult, 
                                 mean_book_test, receptionist, gp))

# Run the simulation
env.run(until=480)

# Calculate and print the mean queuing times for each queue and the mean time 
# in system
mean_queue_time_registration = mean(list_of_queuing_times_registration)
mean_queue_time_consultation = mean(list_of_queuing_times_consultation)
mean_queue_time_book_test = mean(list_of_queuing_times_book_test)
mean_time_in_system = mean(list_of_times_in_system)

print("Mean queuing time for registration : ",
      round(mean_queue_time_registration,2), " minutes", sep="")
print("Mean queuing time for consultation : ",
      round(mean_queue_time_consultation,2), " minutes.", sep="")
print("Mean queuing time for booking test : ",
      round(mean_queue_time_book_test, 2), " minutes.", sep="")
print("Mean time in system : ",
      round(mean_time_in_system, 2), " minutes.", sep="")

# Plot results in bar chart
result_names = ["Q Reg", "Q Consultation", "Q Book Test", "Time in System"]
results = [mean_queue_time_registration,
           mean_queue_time_consultation,
           mean_queue_time_book_test,
           mean_time_in_system
           ]

figure_1, ax = plt.subplots()

ax.set_ylabel("Time (minutes)")

ax.bar(result_names, results)

figure_1.show()

