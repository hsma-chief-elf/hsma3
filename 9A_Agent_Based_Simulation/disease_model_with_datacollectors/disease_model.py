#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:42:28 2019

@author: dan
"""

from mesa import Agent, Model
from mesa.time import RandomActivation # random order of agent actions
from mesa.space import MultiGrid # multiple agents per cell
from mesa.datacollection import DataCollector

import random

class Person_Agent(Agent):
    # Agent initialisation function, possibility of being infected at inception
    def __init__(self, unique_id, model, initial_infection, transmissibility, 
                 level_of_movement, mean_length_of_disease):
        super().__init__(unique_id, model)
        self.transmissibility = transmissibility
        self.level_of_movement = level_of_movement
        self.mean_length_of_disease = mean_length_of_disease
        if random.uniform(0, 1) < initial_infection:
            self.infected = True
            self.disease_duration = int(round(
                    random.expovariate(1.0 / self.mean_length_of_disease), 0))
        else:
            self.infected = False
                
    # Agent movement function
    def move(self):
        # Find possible neighbouring cells to which to move, include diagonals
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            
        # Select new position at random
        new_position = random.choice(possible_steps)
            
        # Move the agent
        self.model.grid.move_agent(self, new_position)
        
    # Agent infection function
    def infect(self):
        # Get list of agents in this cell
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        
        # Check if there are other agents here
        if len(cellmates) > 1:
            # for each agent in the cell
            for inhabitant in cellmates:
                # infect the agent with a given probability (transmissibility)
                # if they're not already infected
                if inhabitant.infected == False:
                    if random.uniform(0, 1) < self.transmissibility:
                        inhabitant.infected = True
                        inhabitant.disease_duration = int(round(
                                random.expovariate(
                                        1.0 / self.mean_length_of_disease), 0))
                        
    def step(self):
        # Move with given probability
        if random.uniform(0, 1) < self.level_of_movement:
            self.move()
            
        # Begin infecting cellmates (if agent is infected), and update 
        # remaining disease duration
        if self.infected == True:
            self.infect()
            # decrement remaining disease duration by one time unit
            self.disease_duration -= 1
            
            # if disease has now run its course, flag that the agent is no 
            # longer infected
            if self.disease_duration <= 0:
                self.infected = False

class Disease_Model(Model):
    # 2D Model initialisation function - initialise with N agents, and 
    # specified width and height
    """A model of disease spread.  For training purposes only."""
    def __init__(self, N, width, height, initial_infection, transmissibility,
                 level_of_movement, mean_length_of_disease):
        self.running = True # required for BatchRunner
        self.num_agents = N # assign number of agents at initialisation
        self.grid = MultiGrid(width, height, True) # setup Toroidal multi-grid
        # set up a scheduler with random order of agents being activated 
        # each turn
        self.schedule = RandomActivation(self)
        
        # Create agents up to number specified
        for i in range(self.num_agents):
            # Create agent with ID taken from for loop
            a = Person_Agent(i, self, initial_infection, transmissibility, 
                             level_of_movement, mean_length_of_disease)
            self.schedule.add(a) # add agent to the schedule
            
            # Try adding the agent to a random empty cell
            try:
                start_cell = self.grid.find_empty()
                self.grid.place_agent(a, start_cell)
            # If you can't find an empty cell, just pick any cell at random
            except:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                self.grid.place_agent(a, (x,y))
                
        # Create a new datacollector, and pass in a model reporter as a
        # dictionary entry, with the index value as the name of the result
        # (which we'll refer to by this name elsewhere) and the lookup value
        # as the name of the function we created below that will calculate
        # the result we're reporting
        self.datacollector = DataCollector(
                model_reporters={"Total_Infected":calculate_number_infected},
                agent_reporters={}
                )
                
    # Function to advance the model by one step
    def step(self):
        self.schedule.step()
        # Tell the datacollector to collect data from the specified model
        # and agent reporters
        self.datacollector.collect(self)

# Function to calculate total number infected in the model
# The function takes as an input a model object for which we want to calculate
# these results
def calculate_number_infected(model):
    # set up a counter with default value of 0 that will keep count of the
    # total number infected
    total_infected = 0
    
    # use list comprehension to establish a new list that contains the
    # infected variable value of each agent in the model
    infection_report = [agent.infected for agent in model.schedule.agents]
    
    # loop through the stored variable values which indicate whether each
    # agent is infected, and for each one that is True incremenent the total
    # number of infected by 1
    for x in infection_report:
        if x == True:
            total_infected += 1
            
    # Return the total number of infected as the output from the function
    return total_infected

