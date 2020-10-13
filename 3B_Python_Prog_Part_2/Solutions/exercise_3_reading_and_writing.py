#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:46:45 2019

@author: dan
"""

# Import the csv library
import csv

list_of_names = []
list_of_genders = []
list_of_ages = []
list_of_counties = []

# Read the file and put each data value in each row in the appropriate list
with open("input_data.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    
    for row in reader:
        list_of_names.append(row[0])
        list_of_genders.append(row[1])
        list_of_ages.append(int(row[2]))
        list_of_counties.append(row[3])
        
# Take the length of the list of names to find how many records read in
number_of_patient_records = len(list_of_names)
print(number_of_patient_records, " records read in.", sep="")

# Calculate the mean age and round to 2 dp
average_age = sum(list_of_ages) / len(list_of_ages)
average_age = round(average_age, 2)
print("Average age of patients is ", average_age, sep="")

number_in_Cornwall = 0
number_in_Devon = 0
number_in_Somerset = 0

# Count up the records for each county
for county in list_of_counties:
    if county == "Cornwall":
        number_in_Cornwall += 1
    elif county == "Devon":
        number_in_Devon += 1
    elif county == "Somerset":
        number_in_Somerset += 1
        
print("Patients living in Cornwall : ", number_in_Cornwall, sep="")
print("Patients living in Devon    : ", number_in_Devon, sep="")
print("Patients living in Somerset : ", number_in_Somerset, sep="")

number_male = 0
number_female = 0

# Count the number of males and females, and then calculate the % split and
# round to 2 dp
for gender in list_of_genders:
    if gender == "MALE":
        number_male += 1
    elif gender == "FEMALE":
        number_female += 1
        
percentage_male = (number_male / (number_male + number_female)) * 100
percentage_male = round(percentage_male, 2)
percentage_female = 100 - percentage_male
percentage_female = round(percentage_female, 2)

print(percentage_male, "% of patients are male", sep="")
print(percentage_female, "% of patients are female", sep="")

# Set up lists ready for writing to csv
list_of_column_names = ["Number of Records", 
                        "Mean Age", 
                        "No. in Cornwall",
                        "No. in Devon", 
                        "No. in Somerset", 
                        "% Male",
                        "% Female"]
list_of_results = [number_of_patient_records,
                   average_age,
                   number_in_Cornwall,
                   number_in_Devon,
                   number_in_Somerset,
                   percentage_male,
                   percentage_female]

list_of_lists_to_write = [list_of_column_names, list_of_results]

# Write results to csv file
with open("results.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    
    for sublist in list_of_lists_to_write:
        writer.writerow(sublist)

