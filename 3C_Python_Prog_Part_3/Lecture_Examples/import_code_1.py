#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:17:58 2020

@author: dan
"""


import random
# import the entire Penchord_Wizardry module (the Penchordian class and the 
# turn_into_a_wizard function)
import Penchord_Wizardry

list_of_penchordian_names = ["Alison", "Andy", "Dan", "Kerry", "Martin", 
                             "Mike", "Sarah", "Sean", "Tom"]

# Randomly select three PenCHORDian names
# random.sample selects three elements from a list without replacement
# (if you want values to be able to be repicked (replacement), use
# random.choices)
chosen_penchordian_names = random.sample(list_of_penchordian_names, 3)

list_of_penchordians = []

for name in chosen_penchordian_names:
    list_of_penchordians.append(Penchord_Wizardry.Penchordian(name))

# Call a couple of the class methods on the three created Penchordian objects    
for penchordian in list_of_penchordians:
    penchordian.write_model("Discrete Event Simulation")
    penchordian.tell_joke(0.1)
    
