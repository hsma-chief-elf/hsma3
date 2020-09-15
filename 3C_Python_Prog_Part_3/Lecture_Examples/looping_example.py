#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:03:54 2020

@author: dan
"""

import random

class Vehicle:
    def __init__(self, common_name, number_of_wheels, capacity, owner):
        self.common_name = common_name
        self.number_of_wheels = number_of_wheels
        self.capacity = capacity
        self.owner = owner
        
    def drive(self, speed):
        print (self.owner, " is now driving at ", speed, " mph.", sep="")

mikes_ambulance = Vehicle("Ambulance", 4, 3, "Mike")
seans_car = Vehicle("Car", 3, 2, "Sean")
alisons_bicycle = Vehicle("Bike", 2, 1, "Alison")
toms_monster_truck = Vehicle("Monster Truck", 4, 1, "Tom")

list_of_vehicles = [mikes_ambulance, seans_car, alisons_bicycle,
                    toms_monster_truck]

for vehicle in list_of_vehicles:
    if vehicle.common_name == "Bike":
        vehicle.drive(random.uniform(2,12))
    else:
        vehicle.drive(random.uniform(20,70))
    
    print("It is a ", vehicle.capacity, " passenger vehicle.", sep="")
    
