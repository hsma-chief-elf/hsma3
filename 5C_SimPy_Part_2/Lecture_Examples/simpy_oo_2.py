#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simpy
import random
import pandas as pd
import csv

# Class to store global parameter values.  We don't create an instance of this
# class - we just refer to the class blueprint itself to access the numbers
# inside
class g:
    wl_inter = 5
    mean_consult = 6
    number_of_nurses = 1
    sim_duration = 120
    number_of_runs = 100
    
# Class representing our patients coming in for the weight loss clinic.
class Weight_Loss_Patient:
    def __init__(self, p_id):
        self.id = p_id
        self.q_time_nurse = 0
        
# Class representing our model of the GP Surgery.
class GP_Surgery_Model:
    # Here, the constructor sets up the SimPy environment, sets a patient
    # counter to 0 (which we'll use for assigning patient IDs), and sets up
    # our resources (here just a nurse resource, with capacity given by
    # the number stored in the g class)
    # We'll also set up a Pandas DataFrame to store run results
    def __init__(self, run_number):
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        self.nurse = simpy.Resource(self.env, capacity=g.number_of_nurses)
        
        self.run_number = run_number
        
        self.mean_q_time_nurse = 0
        
        self.results_df = pd.DataFrame()
        self.results_df["P_ID"] = []
        self.results_df["Start_Q_Nurse"] = []
        self.results_df["End_Q_Nurse"] = []
        self.results_df["Q_Time_Nurse"] = []
        self.results_df.set_index("P_ID", inplace=True)
        
    # A method that generates patients arriving for the weight loss clinic
    def generate_wl_arrivals(self):
        # Keep generating indefinitely (until the simulation ends)
        while True:
            # Increment the patient counter by 1
            self.patient_counter += 1
            
            # Create a new patient - an instance of the Weight_Loss_Patient 
            # class, and give the patient an ID determined by the patient
            # counter
            wp = Weight_Loss_Patient(self.patient_counter)
            
            # Get the SimPy environment to run the attend_wl_clinic method
            # with this patient
            self.env.process(self.attend_wl_clinic(wp))
            
            # Randomly sample the time to the next patient arriving for the
            # weight loss clinic.  The mean is stored in the g class.
            sampled_interarrival = random.expovariate(1.0 / g.wl_inter)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_interarrival)
            
    # A method that models the processes for attending the weight loss clinic.
    # The method needs to be passed a patient who will go through these
    # processes
    def attend_wl_clinic(self, patient):
        # Record the time the patient started queuing for a nurse
        start_q_nurse = self.env.now
        
        # Request a nurse
        with self.nurse.request() as req:
            # Freeze the function until the request for a nurse can be met
            yield req
            
            # Record the time the patient finished queuing for a nurse
            end_q_nurse = self.env.now
            
            # Calculate the time this patient spent queuing for a nurse and
            # store in the patient's attribute
            patient.q_time_nurse = end_q_nurse - start_q_nurse
            
            # Store the start and end queue times alongside the patient ID in
            # the Pandas DataFrame of the GP_Surgery_Model class
            df_to_add = pd.DataFrame({"P_ID":[patient.id],
                                      "Start_Q_Nurse":[start_q_nurse],
                                      "End_Q_Nurse":[end_q_nurse],
                                      "Q_Time_Nurse":[patient.q_time_nurse]})
            df_to_add.set_index("P_ID", inplace=True)
            self.results_df = self.results_df.append(df_to_add)
            
            # Randomly sample the time the patient will spend in consultation
            # with the nurse.  The mean is stored in the g class.
            sampled_cons_duration = random.expovariate(1.0 / g.mean_consult)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_cons_duration)
    
    # A method that calculates the average quueing time for the nurse.  We can
    # call this at the end of each run
    def calculate_mean_q_time_nurse(self):
        self.mean_q_time_nurse = self.results_df["Q_Time_Nurse"].mean()
        
    # A method to write run results to file
    def write_run_results(self):
        with open("trial_results.csv", "a") as f:
            writer = csv.writer(f, delimiter=",")
            results_to_write = [self.run_number,
                                self.mean_q_time_nurse]
            writer.writerow(results_to_write)
    
    # The run method starts up the entity generators, and tells SimPy to start
    # running the environment for the duration specified in the g class. After
    # the simulation has run, it calls the methods that calculate run
    # results, and the method that writes these results to file
    def run(self):
        # Start entity generators
        self.env.process(self.generate_wl_arrivals())
        
        # Run simulation
        self.env.run(until=g.sim_duration)
        
        # Calculate run results
        self.calculate_mean_q_time_nurse()
        
        # Write run results to file
        self.write_run_results()

# Class to store, calculate and manipulate trial results
class Trial_Results_Calculator:
    def __init__(self):
        self.trial_results_df = pd.DataFrame()
        
    # A method to read in the trial results and print them for the user
    def print_trial_results(self):
        print ("TRIAL RESULTS")
        print ("-------------")
        
        # Read in results from each run
        trial_results_df = pd.read_csv("trial_results.csv")
        
        # Take average over runs
        trial_mean_q_time_nurse = trial_results_df["Mean_Q_Time_Nurse"].mean()
        
        print ("Mean Queuing Time for Nurse over Trial : ",
               round(trial_mean_q_time_nurse, 2))

# Everything above is definition of classes and functions, but here's where
# the code will start actively doing things.        

# Create a file to store trial results
with open("trial_results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    column_headers = ["Run", "Mean_Q_Time_Nurse"]
    writer.writerow(column_headers)

# For the number of runs specified in the g class, create an instance of the
# GP_Surgery_Model class, and call its run method
for run in range(g.number_of_runs):
    print ("Run ", run+1, " of ", g.number_of_runs, sep="")
    my_gp_model = GP_Surgery_Model(run)
    my_gp_model.run()
    print ()

# Once the trial is complete, we'll create an instance of the
# Trial_Result_Calculator class and run the print_trial_results method
my_trial_results_calculator = Trial_Results_Calculator()
my_trial_results_calculator.print_trial_results()

