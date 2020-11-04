#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:10:15 2019

@author: dan
"""

# We'll first import from the module that we ourselves created!  We only need
# the Disease_Model class bit of the module here, so that's all we'll import
from disease_model import Disease_Model
# This will import the type of grid we want to visualise our agents
from mesa.visualization.modules import CanvasGrid
# This will import the ModularServer class, which allows us to create a new
# server to host the visualisation of our model
from mesa.visualization.ModularVisualization import ModularServer
# We'll also the UserSettableParameter class, which allows us to create
# user-interface elements, such as sliders, so the user can change model
# parameters
from mesa.visualization.UserParam import UserSettableParameter

# Portrayal function that defines how agents will be drawn onto the grid
# We specify that the function takes an agent as its input - it will draw the
# agent passed to it in the manner we define in this function
def agent_portrayal(agent):
    # Set up portrayal dictionary to store the key aspects of our portrayal
    portrayal = {"Shape":"circle", "Filled":"true", "r":0.5}
    
    # Specify visual characteristics for infected agents & non-infected agents
    # Here, we specify that if an agent is infected, then colour them red, and
    # put them on the lowest layer; otherwise, colour them grey, change their
    # radius to 0.2 (compared to the default of 0.5 we specified above), and
    # put them on a higher level so they'll appear on top of infected agents
    # if both occupy a cell
    if agent.infected == True:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
        portrayal["Layer"] = 1
        
    # Return the portrayal of the agent so it can be drawn by the server
    return portrayal

# Set up visualisation elements
# Set up a CanvasGrid, that portrays agents as defined by the portrayal
# function we defined, has 10 x 10 cells, and a display size of 500x500 pixels
grid = CanvasGrid(agent_portrayal,10,10,500,500)

# Set up user sliders.  For each, we create an instance of the
# UserSettableParameter class, and pass to it that we want a slider, the
# label for the slider, the default, minimum and maximum values for the
# slider, and the increments of change for the slider.
number_of_agents_slider = UserSettableParameter(
        'slider', "Number of Agents", 20, 2, 100, 1)
initial_infection_slider = UserSettableParameter(
        'slider', "Probability of Initial Infection", 0.3, 0.01, 1, 0.01)
transmissibility_slider = UserSettableParameter(
        'slider', "Transmissibility", 0.2, 0.01, 1, 0.01)
level_of_movement_slider = UserSettableParameter(
        'slider', "Level of Movement", 0.5, 0.01, 1, 0.01)
mean_length_of_disease_slider = UserSettableParameter(
        'slider', "Mean Length of Disease (days)", 10, 1, 100, 1)

# Set up the server as a ModularServer, passing in the model class we
# imported earlier, the list of elements we want to visualise (just the grid
# here), the title to display for the server visualisation, and each user
# interface we want to include (our sliders here) in a dictionary, where the
# index name in " marks must match the respective variable name in the Model 
# Class, and the lookup value is the name of the slider we declared above
# (ie "name_of_variable":name_of_slider)
server = ModularServer(Disease_Model, 
                       [grid], 
                       "Disease Spread Model", 
                       {"N":number_of_agents_slider, "width":10, "height":10, 
                        "initial_infection":initial_infection_slider, 
                        "transmissibility":transmissibility_slider, 
                        "level_of_movement":level_of_movement_slider, 
                        "mean_length_of_disease":mean_length_of_disease_slider}
                       )

