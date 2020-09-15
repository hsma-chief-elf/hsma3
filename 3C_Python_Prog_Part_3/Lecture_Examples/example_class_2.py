#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:03:54 2020

@author: dan
"""


class Vehicle:
    def __init__(self, common_name, number_of_wheels, capacity):
        self.common_name = common_name
        self.number_of_wheels = number_of_wheels
        self.capacity = capacity
        
    def drive(self, speed):
        print ("I'm now driving at ", speed, " mph.", sep="")

# Create an instance of the Vehicle class called my_ambulance, that's an
# ambulance with 4 wheels and a passenger capacity of 3        
my_ambulance = Vehicle("Ambulance", 4, 3)

# Tell the ambulance to drive at 60mph by running the drive() method of
# the instance.  Note - you don't need to pass 'self', this is all done
# automatically.
my_ambulance.drive(60)

mikes_ambulance = Vehicle("Ambulance", 4, 3)
seans_car = Vehicle("Car", 3, 2)
alisons_bicycle = Vehicle("Bike", 2, 1)
toms_monster_truck = Vehicle("Monster Truck", 4, 1)

