#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:10:15 2019

@author: dan
"""

from disease_model import Disease_Model
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    # Set up portrayal dictionary
    portrayal = {"Shape":"circle", "Filled":"true", "r":0.5}
    
    # Specify visual characteristics for infected agents & non-infected agents
    if agent.infected == True:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif agent.immunised == True:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
        
    return portrayal

# Set up visualisation elements
grid = CanvasGrid(agent_portrayal,10,10,500,500)
total_infected_and_imm_graph = ChartModule(
        [{"Label":"Total_Infected", "Color":"Red"},
         {"Label":"Total_Imm", "Color":"Black"}],
        data_collector_name='datacollector'
        )

# Set up user sliders
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
prob_imm_slider = UserSettableParameter(
        'slider', "Probability of Immunisation", 0.05, 0, 1, 0.01)
mean_imm_duration_slider = UserSettableParameter(
        'slider', "Mean Length of Immunisation (days)", 20, 1, 100, 1)

server = ModularServer(Disease_Model, [grid, total_infected_and_imm_graph],
                       "Disease Spread Model", 
                       {"N":number_of_agents_slider, "width":10, "height":10, 
                        "initial_infection":initial_infection_slider, 
                        "transmissibility":transmissibility_slider, 
                        "level_of_movement":level_of_movement_slider, 
                        "mean_length_of_disease":mean_length_of_disease_slider,
                        "prob_being_immunised":prob_imm_slider,
                        "mean_imm_duration":mean_imm_duration_slider}
                       )

