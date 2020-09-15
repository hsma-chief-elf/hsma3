#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:03:54 2020

@author: dan
"""


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

mikes_ambulance.drive(50)
seans_car.drive(20)
alisons_bicycle.drive(7)
toms_monster_truck.drive(80)

print ("Tom's vehicle has ", toms_monster_truck.number_of_wheels, " wheels",
       sep="")

