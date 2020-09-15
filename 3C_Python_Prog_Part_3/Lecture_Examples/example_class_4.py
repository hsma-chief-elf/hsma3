#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:03:54 2020

@author: dan
"""

# Here, we only need to provide a name when creating a new instance of a
# Student - the other two attributes will be set to default values
class Student:
    def __init__(self, name):
        self.name = name
        self.completed_course = False
        self.level = 1
        
my_student = Student("Dan Chalk")
        
# The parameter names passed in don't have to match the names of the attributes
# in the class either (although often they will).  But make sure you refer to 
# the correct attribute name when referencing the object.
class Student:
    def __init__(self, full_name, dob, year):
        self.name = full_name
        self.date_of_birth = dob
        self.class_year = year
        
