#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:15:48 2020

@author: dan
"""

import csv # import csv library

list_of_names = []
list_of_ages = []
list_of_locations = []

with open("filename.csv", "r") as f:
    # create a csv reader object that reads the file with comma delimiters
    reader = csv.reader(f, delimiter=",")
    
    # for each row (line) in the csv file
    for row in reader:
        # add the first value before a comma to the list of names
        list_of_names.append(row[0])
        
        # add the second value to the list of ages
        list_of_ages.append(row[1])
        
        # add the third value to the list of locations
        list_of_locations.append(row[2])
        
# Writing csv files is easy with the csv library too!

# Let's say we have some lists we want to write to file
list_of_penchordians = ["Alison", "Andy", "Dan", "Kerry", "Martin", "Mike",
                        "Sean", "Tom"]
list_of_numbers = [1,2,3,4,5,6,7,8]
list_of_lists = [list_of_penchordians, list_of_numbers]

with open("output.csv", "w") as f:
    # Create a csv writer objects that writes a csv file with comma delimiters
    writer = csv.writer(f, delimiter=",")
    
    # Write a row for each of our lists within lists
    for sublist in list_of_lists:
        writer.writerow(sublist)
        
