#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:21:57 2020

@author: dan
"""

class Integer_Calculator:
    def __init__(self):
        self.switched_on = False
        
    def switch_on_calculator(self):
        self.switched_on = True
        print ("Calculator is now turned on")
        
    def switch_off_calculator(self):
        self.switched_on = False
        print ("Calculator is now turned off")
        
    def add_numbers(self, list_of_numbers):
        result = sum(list_of_numbers)
        
        return result
    
    def subtract_numbers(self, list_of_numbers):
        result = list_of_numbers[0]
        
        for x in range(1, len(list_of_numbers)):
            result -= list_of_numbers[x]
            
        return result
    
    def multiply_numbers(self, list_of_numbers):
        result = list_of_numbers[0]
        
        for x in range(1, len(list_of_numbers)):
            result = result * list_of_numbers[x]
            
        return result
    
    def divide_numbers(self, list_of_numbers):
        result = list_of_numbers[0]
        
        for x in range(1, len(list_of_numbers)):
            result = result / list_of_numbers[x]
            
        return result
    
    def input_numbers(self):
        if self.switched_on == False:
            print ("Calculator is switched off")
            
            return []
        else:
            keep_inputting = True
            list_of_inputs = []
            
            while keep_inputting == True:
                try:
                    input_number = int(input("Please input number : "))
                    list_of_inputs.append(input_number)
                    
                    valid_continue_decision = False
                    
                    while valid_continue_decision == False:
                        continue_decision = input("Continue (Y/N)? : ")
                        
                        if continue_decision == "Y":
                            valid_continue_decision = True
                        elif continue_decision == "N":
                            valid_continue_decision = True
                            keep_inputting = False
                            return list_of_inputs
                except:
                    print ("You must input integers only")
                    
    def input_operator(self):
        if self.switched_on == False:
            print ("Calculator is switched off")
            
            return "ERR"
        else:
            valid_operator = False
            
            while valid_operator == False:
                print ("Please input : ")
                print ("+ for addition")
                print ("- for subtraction")
                print ("* for multiplication")
                print ("/ for division")
                selected_operator = input("SELECTION : ")
                
                if selected_operator in ["+", "-", "*", "/"]:
                    valid_operator = True
                    return selected_operator
                else:
                    print ("Invalid operator")
                    
my_calculator = Integer_Calculator()

my_calculator.switch_on_calculator()
list_of_input_numbers = my_calculator.input_numbers()
chosen_operator = my_calculator.input_operator()

if len(list_of_input_numbers) > 1:
    if chosen_operator == "+":
        answer = my_calculator.add_numbers(list_of_input_numbers)
    elif chosen_operator == "-":
        answer = my_calculator.subtract_numbers(list_of_input_numbers)
    elif chosen_operator == "*":
        answer = my_calculator.multiply_numbers(list_of_input_numbers)
    elif chosen_operator == "/":
        answer = my_calculator.divide_numbers(list_of_input_numbers)
    else:
        print ("Error - calculator was switched off")
    
    print ("The answer is ", answer, sep="")
else:
    print ("Only one number given")