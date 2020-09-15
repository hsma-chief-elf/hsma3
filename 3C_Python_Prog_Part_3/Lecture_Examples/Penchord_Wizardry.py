#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 09:28:42 2020

@author: dan
"""

import random

# Class defining a Penchordian
class Penchordian :
    def __init__(self, name):
        self.name = name
        self.is_a_wizard = False
        
    def write_model(self, type_of_model):
        print (self.name, " is now writing a ", type_of_model, " model.",
               sep="")
        
    def tell_joke(self, prob_success):
        if random.uniform(0,1) < prob_success:
            print (self.name, " attempted a joke.  People loved it!", sep="")
        else:
            print (self.name, " attempted a joke.  It fell flat.", sep="")
            
# Function to turn someone into a wizard
# Input subject must be an object with a "name" string attribute and a 
# "is_a_wizard" boolean attribute
def turn_into_a_wizard(subject):
    subject.is_a_wizard = True
    print (subject.name, " is now a wizard.", sep="")
        
