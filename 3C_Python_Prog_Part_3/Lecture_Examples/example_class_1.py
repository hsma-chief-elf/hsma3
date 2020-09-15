#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:46:02 2020

@author: dan
"""

# Declare a class using the class keyword followed by a class name, which
# should start with a capital letter
class My_Class:
    # Class attributes go here, and are attributes that have the same
    # value for instances created from this class
    class_attribute_1 = "Class attribute value"
    
    # The constructor method.  Note the two underscores both before and after
    # init in the name.  The constructor sets up the Instance Attributes
    # (those with values specific to this instance of a class).  Any values
    # that need to be passed in to set up the attributes need to be declared
    # here, as with any function (method = a function in a class).  However,
    # all class methods must have 'self' as the first parameter (even if there
    # are no other attributes).  The 'self' parameter essentially stores
    # the instance of the class (the copy from the blueprint).  Don't worry
    # too much about this - just know that you need to include it, and that
    # when you say self.something you're referring to the instance of the
    # Class, rather than the Class itself
    def __init__(self, attribute_1, attribute_2):
        self.attribute_1 = atrribute_1
        self.attribute_2 = attribute_2
        
    # All classes must have at least a constructor, but may also have other
    # methods.  These methods must have self as their first parameter, but
    # may also have other parameters, as we've seen before in functions.
    def method_1(self):
        # What do we want method_1 to do
        
    def method_2(self, method_parameter_1):
        # What do we want method_2 to do with method_parameter_1
        
