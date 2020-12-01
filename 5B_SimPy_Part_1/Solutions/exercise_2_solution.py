#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 15:34:30 2020

@author: dan
"""


import simpy
import random
from statistics import mean
import csv
import pandas as pd

# Arrivals generator function
def patient_generator_gp(env, gp_inter, mean_register, mean_consult,
                         mean_book_test, receptionist, gp):
    while True:
        p = activity_generator_gp(env, mean_register, mean_consult,
                                  mean_book_test, receptionist, gp)
        
        env.process(p)
        
        t = random.expovariate(1.0 / gp_inter)
        
        yield env.timeout(t)
        
# Arrivals generator for telephone calls
def call_generator_reception(env, call_inter, mean_call, receptionist):
    while True:
        c = activity_generator_call(env, mean_call, receptionist)
        
        env.process(c)
        
        t = random.expovariate(1.0 / call_inter)
        
        yield env.timeout(t)
        
# Activity generator for receptionist taking telephone calls
def activity_generator_call(env, mean_call, receptionist):    
    with receptionist.request() as req:
        yield req
        
        sampled_call_time = random.expovariate(1.0 / mean_call)
        
        yield env.timeout(sampled_call_time)
        
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
        if env.now > warm_up_period:
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
        if env.now > warm_up_period:
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
            if env.now > warm_up_period:
                list_of_queuing_times_book_test.append(
                    time_in_queue_for_book_test)
            
            sampled_book_test_time = random.expovariate(1.0 / mean_book_test)
            
            yield env.timeout(sampled_book_test_time)
            
    time_left_system = env.now
    time_in_system = (time_left_system - time_entered_system)
    if env.now > warm_up_period:
        list_of_times_in_system.append(time_in_system)

number_of_runs = 100
warm_up_period = 180
results_collection_period = 480

with open("ex_2_results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    
    writer.writerow(["Run", "Q Reg", "Q Cons", "Q Book Test", "Time in Sys"])

for run in range(number_of_runs):
    # Set up simulation environment
    env = simpy.Environment()
    
    # Set up resources
    receptionist = simpy.Resource(env, capacity=1)
    gp = simpy.Resource(env, capacity=2)
    
    # Set up parameter values
    gp_inter = 3
    call_inter = 10
    mean_register = 2
    mean_consult = 8
    mean_book_test = 4
    mean_call = 4
    
    # Lists to store queuing times and time in system across patients
    list_of_queuing_times_registration = []
    list_of_queuing_times_consultation = []
    list_of_queuing_times_book_test = []
    list_of_times_in_system = []
    
    # Start the arrivals generators (in person and incoming calls)
    env.process(patient_generator_gp(env, gp_inter, mean_register, 
                                     mean_consult, mean_book_test, 
                                     receptionist, gp))
    env.process(call_generator_reception(env, call_inter, mean_call, 
                                         receptionist))
    
    # Run the simulation
    env.run(until=(warm_up_period + results_collection_period))
    
    # Calculate and print the mean queuing times for each queue and the mean
    # time in system
    mean_queue_time_registration = mean(list_of_queuing_times_registration)
    mean_queue_time_consultation = mean(list_of_queuing_times_consultation)
    mean_queue_time_book_test = mean(list_of_queuing_times_book_test)
    mean_time_in_system = mean(list_of_times_in_system)
    
    list_to_write = [run, 
                     mean_queue_time_registration,
                     mean_queue_time_consultation,
                     mean_queue_time_book_test,
                     mean_time_in_system]

    with open("ex_2_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",")
        
        writer.writerow(list_to_write)
        
results_df = pd.read_csv("ex_2_results.csv")

mean_q_reg_trial = results_df["Q Reg"].mean()
mean_q_con_trial = results_df["Q Cons"].mean()
mean_q_book_trial = results_df["Q Book Test"].mean()
mean_tis_trial = results_df["Time in Sys"].mean()

print ("Trial Results")
print ("-------------")
print ("Mean time in queue for registration (mins) : ",
       round(mean_q_reg_trial, 2))
print ("Mean time in queue for consultation (mins) : ",
       round(mean_q_con_trial, 2))
print ("Mean time in queue for booking tests (mins) : ",
       round(mean_q_book_trial, 2))
print ("Mean time in system (mins) : ",
       round(mean_tis_trial,2))

