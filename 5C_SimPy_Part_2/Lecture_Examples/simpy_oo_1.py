#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simpy
import random

# Class to store global parameter values.  We don't create an instance of this
# class - we just refer to the class blueprint itself to access the numbers
# inside
class g:
    wl_inter = 5
    mean_consult = 6
    number_of_nurses = 1
    sim_duration = 120
    number_of_runs = 10
    
# Class representing our patients coming in for the weight loss clinic.
# Here, we only have a constructor method, that sets up the patient's ID
class Weight_Loss_Patient:
    def __init__(self, p_id):
        self.id = p_id
        
# Class representing our model of the GP Surgery.
class GP_Surgery_Model:
    # Here, the constructor sets up the SimPy environment, sets a patient
    # counter to 0 (which we'll use for assigning patient IDs), and sets up
    # our resources (here just a nurse resource, with capacity given by
    # the number stored in the g class)
    def __init__(self):
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        self.nurse = simpy.Resource(self.env, capacity=g.number_of_nurses)
        
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
        # Print the time the patient started queuing for a nurse
        print ("Patient ", patient.id, " started queuing at ", self.env.now,
               sep = "")
        
        # Request a nurse
        with self.nurse.request() as req:
            # Freeze the function until the request for a nurse can be met
            yield req
            
            # Print the time the patient finished queuing for a nurse
            print ("Patient ", patient.id, " finished queuing at ", 
                   self.env.now, sep="")
            
            # Randomly sample the time the patient will spend in consultation
            # with the nurse.  The mean is stored in the g class.
            sampled_cons_duration = random.expovariate(1.0 / g.mean_consult)
            
            # Freeze this function until that time has elapsed
            yield self.env.timeout(sampled_cons_duration)
    
    # The run method starts up the entity generators, and tells SimPy to start
    # running the environment for the duration specified in the g class.
    def run(self):
        self.env.process(self.generate_wl_arrivals())
        
        self.env.run(until=g.sim_duration)

# Everything above is definition of classes and functions, but here's where
# the code will start actively doing things.        
# For the number of runs specified in the g class, create an instance of the
# GP_Surgery_Model class, and call its run method
for run in range(g.number_of_runs):
    print ("Run ", run+1, " of ", g.number_of_runs, sep="")
    my_gp_model = GP_Surgery_Model()
    my_gp_model.run()
    print ()

