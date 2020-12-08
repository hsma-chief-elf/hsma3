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
    ed_inter = 8
    mean_register = 2
    mean_triage = 5
    mean_ed_assess = 30
    mean_acu_assess = 60
    
    unavail_time_ed_doctor = 240
    unavail_freq_ed_doctor = 480
    
    prob_acu = 0.2
    
    number_of_receptionists = 1
    number_of_nurses = 2
    number_of_ed_doctors = 2
    number_of_acu_doctors = 1
    
    sim_duration = 2880
    warm_up_duration = 1440
    number_of_runs = 1
    
# Class representing our patients coming in to the ED.  Here, we'll store a
# patient ID and whether the patient will be sent to the ACU or stay in the
# ED, along with a method that makes that determination randomly
class ED_Patient:
    def __init__(self, p_id, prob_acu):
        self.id = p_id
        self.prob_acu = prob_acu
        self.acu_patient = False
        
        # The PriorityResource will see entities (in this case patients)
        # according to their priority - an integer value, where the lower the
        # integer, the higher the priority
        self.priority = 1
        
        self.q_time_reg = 0
        self.q_time_triage = 0
        self.q_time_ed_assess = 0
        self.q_time_acu_assess = 0
        
    # Method to determine whether or not this patient will be diverted to the
    # ACU, based on their probability of being an ACU patient
    def determine_acu_destiny(self):
        if random.uniform(0, 1) < self.prob_acu:
            self.acu_patient = True
            
    # Method to determine the patient's priority.  Here we just randomly
    # select a priority value, but obviously this could include any logic you
    # lile
    def determine_priority(self):
        self.priority = random.randint(1,5)
            
# Class representing our model of the ED
class ED_Model:
    def __init__(self, run_number):
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        self.receptionist = simpy.Resource(self.env,
                                           capacity=g.number_of_receptionists)
        self.nurse = simpy.Resource(self.env,
                                    capacity=g.number_of_nurses)
        
        # If we want a queue where higher priority entities are seen first,
        # then the resource they queue for needs to be a PriorityResource
        self.ed_doctor = simpy.PriorityResource(
            self.env, capacity=g.number_of_ed_doctors)
        self.acu_doctor = simpy.PriorityResource(
            self.env, capacity=g.number_of_acu_doctors)
        
        self.run_number = run_number
        
        self.mean_q_time_registration = 0
        self.mean_q_time_triage = 0
        self.mean_q_time_ed_assessment = 0
        self.mean_q_time_acu_assessment = 0
        
        self.results_df = pd.DataFrame()
        self.results_df["P_ID"] = []
        self.results_df["Q_Time_Registration"] = []
        self.results_df["Q_Time_Triage"] = []
        self.results_df["Q_Time_ED_Assessment"] = []
        self.results_df["Q_Time_ACU_Assessment"] = []
        self.results_df.set_index("P_ID", inplace=True)
        
    # A method that generates patients arriving at the ED
    def generate_ed_arrivals(self):
        # Keep generating indefinitely whilst the simulation is running
        while True:
            # Increment patient counter by 1
            self.patient_counter += 1
            
            # Create a new patient
            p = ED_Patient(self.patient_counter, g.prob_acu)
            
            # Determine the patient's ACU destiny by running the appropriate
            # method
            p.determine_acu_destiny()
            
            # Get the SimPy environment to run the ed_patient_journey method 
            # with this patient
            self.env.process(self.ed_patient_journey(p))
            
            # Randomly sample the time to the next patient arriving
            sampled_interarrival = random.expovariate(1.0 / g.ed_inter)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_interarrival)
            
    # A method to obstruct the ed doctor(s) to emulate other non-modelled
    # tasks or other unavailability
    def obstruct_ed_doctor(self):
        while True:
            print ("An ED Doctor will be removed around time ",
                   self.env.now + g.unavail_freq_ed_doctor, sep="")
            
            # Freeze the function for the unavailability frequency period.
            # This could represent time on shift (the time the doctor is
            # available).  Here, we use a fixed value to reflect a set shift,
            # but you could also sample from a probability distribution.
            yield self.env.timeout(g.unavail_freq_ed_doctor)
            
            # Once this time has elapsed, request an ed doctor with a priority
            # of -1 (so that we know this will get the top priority, as none
            # of our patients will have a negative priority), and hold them
            # for the specified unavailability amount of time
            with self.ed_doctor.request(priority=-1) as req:
                # Freeze the function until the request can be met (this
                # ensures that the doctor will finish what they're doing first)
                yield req
                
                print ("An ED Doctor is unavailable. They'll be back at time ",
                       self.env.now + g.unavail_time_ed_doctor, sep="")
                
                yield self.env.timeout(g.unavail_time_ed_doctor)
            
    def ed_patient_journey(self, patient):
        """REGISTRATION"""
        # Record the time the patient started queuing for registration
        start_q_reg = self.env.now
        
        # Request a receptionist
        with self.receptionist.request() as req:
            # Freeze the function until the request can be met
            yield req
            
            # Record the time the patient finished queuing for registration
            end_q_reg = self.env.now
            
            # Calculate the time the patient was queuing and store in the
            # patient's attribute
            patient.q_time_reg = end_q_reg - start_q_reg
            
            # Randomly sample the time the patient will spend being registered
            sampled_reg_duration = random.expovariate(1.0 / g.mean_register)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_reg_duration)
            
        """TRIAGE"""
        # Record the time the patient started queuing for triage
        start_q_triage = self.env.now
        
        # Request a nurse
        with self.nurse.request() as req:
            # Freeze the function until the request can be met
            yield req
            
            # Record the time the patient finished queuing for triage
            end_q_triage = self.env.now
            
            # Calculate the time the patient was queuing and store in the
            # patient's attribute
            patient.q_time_triage = end_q_triage - start_q_triage
            
            # Randomly sample the time the patient will spend being triaged
            sampled_triage_duration = random.expovariate(1.0 / g.mean_triage)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_triage_duration)
            
            # Now the patient has been triaged, we can assign their priority
            # to determine how quickly they'll be seen either by the ED doctor
            # or the ACU doctor
            patient.determine_priority()
            
        """BRANCH - ED ASSESSMENT OR ACU ASSESSMENT"""
        # Check if patient destined for ACU or not, and either send to ACU
        # for assessment, or keep in ED for assessment
        if patient.acu_patient == True:
            """ACU ASSESSMENT"""
            # Record the time the patient started queuing for ACU assessment
            start_q_acu_assess = self.env.now
            
            # Request an ACU doctor - now that ACU doctor is a
            # PriorityResource, we also specify the value to be used to
            # determine priority.  Here, that's the priority attribute of the
            # patient object.
            with self.acu_doctor.request(priority=patient.priority) as req:                
                # Freeze the function until the request can be met
                yield req
                
                # Record the time the patient finished queuing for ACU 
                # assessment
                end_q_acu_assess = self.env.now
                
                # Calculate the time the patient was queuing and store in the
                # patient's attribute
                patient.q_time_acu_assess = (end_q_acu_assess - 
                                             start_q_acu_assess)
                
                # Randomly sample the time the patient will spend being 
                # assessed
                sampled_acu_assess_duration = (
                    random.expovariate(1.0 / g.mean_acu_assess))
                
                # Freeze this function until that time has elapsed
                yield self.env.timeout(sampled_acu_assess_duration)
        else:
            """ED ASSESSMENT"""
            # Record the time the patient started queuing for ED assessment
            start_q_ed_assess = self.env.now
            
            # Request an ED doctor - now that ED doctor is a
            # PriorityResource, we also specify the value to be used to
            # determine priority.  Here, that's the priority attribute of the
            # patient object.
            with self.ed_doctor.request(priority=patient.priority) as req:
                # Freeze the function until the request can be met
                yield req
                
                # Record the time the patient finished queuing for ED 
                # assessment
                end_q_ed_assess = self.env.now
                
                # Calculate the time the patient was queuing and store in the
                # patient's attribute
                patient.q_time_ed_assess = end_q_ed_assess - start_q_ed_assess
                
                # Randomly sample the time the patient will spend being 
                # assessed
                sampled_ed_assess_duration = (
                    random.expovariate(1.0 / g.mean_ed_assess))
                
                # Freeze this function until that time has elapsed
                yield self.env.timeout(sampled_ed_assess_duration)
        
        # If the warm up time has passed, then call the store_patient_results 
        # method (this doesn't need to be processed by the environment, as it's
        # not a generator function)
        if self.env.now > g.warm_up_duration:
            self.store_patient_results(patient)
        
    # A method to store the patient's results (queuing times here) for this
    # run alongside their patient ID in the Pandas DataFrame of the ED_Model
    # class
    def store_patient_results(self, patient):        
        # First, because we have a branching path, this patient will have
        # queued for either ED assessment or ACU assessment, but not both.
        # Therefore, we need to check which happened, and insert NaNs
        # (Not A Number) in the entries for the other queue in the DataFrame.
        # NaNs are automatically ignored by Pandas when calculating the mean
        # etc.  We can create a nan by casting the string 'nan' as a float :
        # float("nan")
        if patient.acu_patient == True:
            patient.q_time_ed_assess = float("nan")
        else:
            patient.q_time_acu_assess = float("nan")
            
        df_to_add = pd.DataFrame({"P_ID":[patient.id],
                                  "Q_Time_Registration":[patient.q_time_reg],
                                  "Q_Time_Triage":[patient.q_time_triage],
                                  "Q_Time_ED_Assessment":(
                                      [patient.q_time_ed_assess]),
                                  "Q_Time_ACU_Assessment":(
                                      [patient.q_time_acu_assess]),
                                  })
        
        df_to_add.set_index("P_ID", inplace=True)
        self.results_df = self.results_df.append(df_to_add)

    # A method that calculates the average queuing times for each queue.  We
    # can call this at the end of each run
    def calculate_mean_q_times(self):
        self.mean_q_time_registration = (
            self.results_df["Q_Time_Registration"].mean())
        self.mean_q_time_triage = (
            self.results_df["Q_Time_Triage"].mean())
        self.mean_q_time_ed_assessment = (
            self.results_df["Q_Time_ED_Assessment"].mean())
        self.mean_q_time_acu_assessment = (
            self.results_df["Q_Time_ACU_Assessment"].mean())
        
    # A method to write run results to file
    def write_run_results(self):
        with open("trial_ed_results.csv", "a") as f:
            writer = csv.writer(f, delimiter=",")
            results_to_write = [self.run_number,
                                self.mean_q_time_registration,
                                self.mean_q_time_triage,
                                self.mean_q_time_ed_assessment,
                                self.mean_q_time_acu_assessment]
            writer.writerow(results_to_write)
            
    # The run method starts up the entity generators, and tells SimPy to start
    # running the environment for the duration specified in the g class. After
    # the simulation has run, it calls the methods that calculate run
    # results, and the method that writes these results to file
    def run(self):
        # Start entity generators
        self.env.process(self.generate_ed_arrivals())
        self.env.process(self.obstruct_ed_doctor())
        
        # Run simulation
        self.env.run(until=(g.sim_duration + g.warm_up_duration))
        
        # Calculate run results
        self.calculate_mean_q_times()
        
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
        self.trial_results_df = pd.read_csv("trial_ed_results.csv")
        
        # Take average over runs
        trial_mean_q_time_registration = (
            self.trial_results_df["Mean_Q_Time_Registration"].mean())
        trial_mean_q_time_triage = (
            self.trial_results_df["Mean_Q_Time_Triage"].mean())
        trial_mean_q_time_ed_assess = (
            self.trial_results_df["Mean_Q_Time_ED_Assessment"].mean())
        trial_mean_q_time_acu_assess = (
            self.trial_results_df["Mean_Q_Time_ACU_Assessment"].mean())
        
        print ("Mean Queuing Time for Registration over Trial : ",
               round(trial_mean_q_time_registration, 2))
        print ("Mean Queuing Time for Triage over Trial : ",
               round(trial_mean_q_time_triage, 2))
        print ("Mean Queuing Time for ED Assessment over Trial : ",
               round(trial_mean_q_time_ed_assess, 2))
        print ("Mean Queuing Time for ACU Assessment over Trial : ",
               round(trial_mean_q_time_acu_assess, 2))

# Everything above is definition of classes and functions, but here's where
# the code will start actively doing things.        

# Create a file to store trial results
with open("trial_ed_results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    column_headers = ["Run",
                      "Mean_Q_Time_Registration",
                      "Mean_Q_Time_Triage",
                      "Mean_Q_Time_ED_Assessment",
                      "Mean_Q_Time_ACU_Assessment"]
    writer.writerow(column_headers)

# For the number of runs specified in the g class, create an instance of the
# ED_Model class, and call its run method
for run in range(g.number_of_runs):
    print ("Run ", run+1, " of ", g.number_of_runs, sep="")
    my_ed_model = ED_Model(run)
    my_ed_model.run()
    print ()

# Once the trial is complete, we'll create an instance of the
# Trial_Result_Calculator class and run the print_trial_results method
my_trial_results_calculator = Trial_Results_Calculator()
my_trial_results_calculator.print_trial_results()

