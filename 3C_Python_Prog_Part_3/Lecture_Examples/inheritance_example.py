#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:03:54 2020

@author: dan
"""


class Vehicle:
    def __init__(self, number_of_wheels, capacity, owner):
        self.number_of_wheels = number_of_wheels
        self.capacity = capacity
        self.owner = owner
        
    def drive(self, speed):
        print (self.owner, " is now driving at ", speed, " mph.", sep="")

# To create a new Child class, we simply define a class in the normal way,
# but feed the Parent class in as an input
class Ambulance(Vehicle):
    # We can use the super() function to refer to the Parent class.  Here,
    # we declare our Ambulance constructor with a new attribute - siren_on - 
    # and then use super().__init__ to call the Parent constructor so we don't
    # have to repeat all of that code.  We can then just add the new bit.
    def __init__(self, number_of_wheels, capacity, owner, siren_on):
        super().__init__(number_of_wheels, capacity, owner)
        self.siren_on = siren_on
        
    # We can set up new methods in the normal way
    def turn_on_siren(self):
        self.siren_on = True
        print ("Siren turned on")
    
    def turn_off_siren(self):
        self.siren_on = False
        print ("Siren turned off")
        
    # And if we want to overwrite an existing method we can just give it the
    # same name as the one in our Parent class
    def drive(self, speed):
        print ("This ambulance is driving at ", speed, " mph.", sep="")
        
my_ambulance = Ambulance(4, 3, "Dan", False)
my_ambulance.turn_on_siren()
my_ambulance.drive(70)

