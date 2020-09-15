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

# A class representing a 'person' agent.  Note we're passing in the Agent class
# we imported from the mesa library.  Remember that this means our class here
# is inheriting from the 'parent' Agent class, and our class is the 'child',
# which inherits all the attributes and methods of the parent, but may have
# some of its own.
class Person_Agent(Agent):
    # Constructor
    def __init__(self, unique_id, model, initial_infection, transmissibility, 
                 level_of_movement, mean_length_of_disease):
        # Call the constructor from the parent Agent class, which will do all
        # the hard work of defining what an agent is - we just give it an ID
        # and a model that it will live in
        super().__init__(unique_id, model)
        
        # Now we define the attributes of our Person Agent that aren't in the
        # parent class
        # First, we specify the level of transmissibility (the probability of
        # passing the disease onto someone else after contact with them,
        # assuming this agent is infected, and the other one isn't)
        self.transmissibility = transmissibility
        
        # The probability that the agent will move from its current location
        # at any given time step
        self.level_of_movement = level_of_movement
        
        # Average duration of being infected with the disease
        self.mean_length_of_disease = mean_length_of_disease
        
        # We're going to set up our model so that some agents are already
        # infected at the start.  We've got a parameter value passed in
        # (initial_infection) that defines the probability of any given agent
        # being infected at the start.  So, we just randomly sample from a
        # uniform distribution between 0 and 1, and if the sampled value is
        # less than this probability, then we say that the agent is infected -
        # we set their Boolean infected attribute to True, and randomly
        # sample a duration for which they'll have the disease, based on the
        # mean duration we passed in.  Otherwise, we set their infected
        # attribute to false
        if random.uniform(0, 1) < initial_infection:
            self.infected = True
            self.disease_duration = int(round(
                    random.expovariate(1.0 / self.mean_length_of_disease), 0))
        else:
            self.infected = False
                
    # Agent movement method - this is called if it is determined the agent
    # is going to move on this time step
    def move(self):
        # Get a list of possible neighbouring cells to which to move
        # We use the get_neighborhood function, giving it the agent's current
        # position on the grid, stating we want a Moore neighbourhood (which
        # includes diagonals), and that we don't want to include the centre
        # (where the agent is currently) in the returned neighbourhood list
        possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            
        # Select new position at random
        new_position = random.choice(possible_steps)
            
        # Move the agent to the randomly selected new position
        self.model.grid.move_agent(self, new_position)
        
    # Agent infection method
    def infect(self):
        # Get list of agents in this cell.  We use the get_cell_list_contents
        # function of the grid object and pass it our current position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        
        # Check if there are other agents here - if the list of cellmates is
        # greater than 1 then there must be more here than this agent
        if len(cellmates) > 1:
            # for each agent in the cell
            for inhabitant in cellmates:
                # infect the agent with a given probability (transmissibility)
                # if they're not already infected.  If they become infected,
                # then we set their infected attribute to True, and their
                # disease_duration attribute to a value randomly sampled based
                # on the mean_length_of_disease attribute.
                if inhabitant.infected == False:
                    if random.uniform(0, 1) < self.transmissibility:
                        inhabitant.infected = True
                        inhabitant.disease_duration = int(round(
                                random.expovariate(
                                        1.0 / self.mean_length_of_disease), 0))
                        
