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
                        
    # Step method - this defines which of the agent's actions will be taken
    # on a time step, and in which order
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
    # specified width and height.  Also pass in the things we need to pass
    # to our agents when instantiating them.
    # The comment below which uses triple " will get picked up by the server
    # if we run a live display of the model.
    """A model of disease spread.  For training purposes only."""
    def __init__(self, N, width, height, initial_infection, transmissibility,
                 level_of_movement, mean_length_of_disease):
        self.running = True # required for BatchRunner
        self.num_agents = N # assign number of agents at initialisation
        
        # Set up a Toroidal multi-grid (Toroidal = if the agent is in a cell
        # on the border of the grid, and moves towards the border, they'll
        # come out the other side.  Think PacMan :) The True Boolean passed in
        # switches that on.  Multi-Grid just means we can have more than one 
        # agent per cell)
        self.grid = MultiGrid(width, height, True)
        # set up a scheduler with random order of agents being activated 
        # each turn.  Remember order is important here - if an infected agent
        # is going to move into a cell with an uninfected agent, but that
        # uninfected agent moves first, they'll escape infection.
        self.schedule = RandomActivation(self)
        
        # Create person_agent objects up to number specified
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
                
    # Function to advance the model by one step
    def step(self):
        self.schedule.step()
        
