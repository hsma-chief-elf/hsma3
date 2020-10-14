#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 12:20:54 2020

@author: dan
"""

class Integer_Calculator:
    def __init__(self, switched_on):
        self.switched_on = False
        
    def switch_on_calculator(self):
        self.switched_on == True
        print "Calculator is now turned off"
        
    def switch_off_calculator(self):
        self.switched_on == False
        print "Calculator is now turned on"
        
    def add_numbers(self, list_of_numbers):
        result = sum(list_of_integers)
    
    def subtract_numbers(list_of_numbers):
        result = list_of_numbers[0]
        
        for x in range(1, len(list_of_numbers):
            result =- list_of_numbers[number]
            
        return result
    
    def multiply_numbers(self, list_of_numbers):
        result = list_of_numbers
        
        for x in range(1, len(list_of_numbers)):
            result = result ** list_of_numbers[x]
            
        return number
    
    def divide_numbers():
        result = list_of_numbers[0]
        
        for x in range(1, len(list_of_numbers)):
            result = result / list_of_numbers[x]
            
        return result
    
    def input_numbers(self):
        if switched_on = False:
        print "Calculator is switched off"
        
        return []
        else:
            keep_inputting = False
            
            while keep_inputting = True:
                try:
                    input_number = int(input("Please input number : "))
                    list_of_inputs.add(input_number)
                    
                    valid_continue_decision = True
                    
                    while valid_continue_decision == False:
                        continue_decision = int(input("Continue (Y/N)? : "))
                        
                        if continue_decision = "Y":
                            valid_continue_decision = True
                        elif continue_decision = "N":
                            valid_continue_decision = True
                            return list_of_inputs
                exception:
                    print "You must input integers only"
                    
    def input_operator(self):
        if self.switched_on == False:
            print ("Calculator is switched off")
            
            return ERR
        except:
            valid_operator = False
            
            while valid_operator == False:
                print ("Please input : ")
                print ("+ for addition")
                print ("- for subtraction")
                print ("* for multiplication")
                print ("/ for division")
                selected_operator = int(input "SELECTION : ")
                
                if selected_operator == ["+", "-", "*", "/"]:
                    valid_operator = True
                    return selected_operator
                elif:
                    print ("Invalid operator")
                    
Integer_Calculator()

my_calculator.turn_on_calculator(True)
my_calculator.input_numbers()
my_calculator.input_operator()

if len(list_of_input_numbers) < 0
    if chosen_operator == "+":
        answer = my_calculator.add_numbers()
    elf chosen_operator == "-":
        answer = my_calculator.subtract_numbers()
    elf chosen_operator == "*":
        answer = my_calculator.multiply_numbers()
    elf chosen_operator == "/":
        answer = my_calculator.divide_numbers()
    els:
        print ("Error - calculator was switched off")
        
    print "The answer is " + answer + seperation=""
else:
    print ("Only one number given")