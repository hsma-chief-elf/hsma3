#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:04:44 2020

@author: dan
"""


import matplotlib as mpl
import matplotlib.pyplot as plt

day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
               "Saturday", "Sunday"]
hospital_a_ed_attendances = [242,180,156,191,231,378,345]
hospital_b_ed_attendances = [310,290,317,351,341,261,295]

figure_1, ax = plt.subplots()

ax.set_xlabel("Day of Week")
ax.set_ylabel("Mean Number of ED Attendances")

ax.plot(day_of_week, hospital_a_ed_attendances, color="green", linestyle="-",
        label="Hospital A")
ax.plot(day_of_week, hospital_b_ed_attendances, color="darkviolet", 
        linestyle="-.", label="Hospital B")

ax.legend(loc="lower right")

ax.set_ylim(ymin=0)

figure_1.show()

total_mean_ed_attendances  = []

for i in range(len(hospital_a_ed_attendances)):
    total_mean_ed_attendances.append(hospital_a_ed_attendances[i] +
                                     hospital_b_ed_attendances[i])

figure_2, ax_2 = plt.subplots()

ax_2.set_xlabel("Day of Week")
ax_2.set_ylabel("Total Mean Attendances Across Both Hospitals")

ax_2.bar(day_of_week, total_mean_ed_attendances)

figure_2.show()

