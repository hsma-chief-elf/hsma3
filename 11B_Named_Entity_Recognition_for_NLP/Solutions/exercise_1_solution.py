#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:23:22 2020

@author: dan
"""

# import spacy and the downloaded en_core_web_sm pre-trained model
# Also import the Counter module, which allows us to easily count occurrences
# of items
import spacy
import en_core_web_sm
from collections import Counter

# Load the pre-trained model as a language into a variable called nlp
nlp = en_core_web_sm.load()

# Read in the document for which we want to extract named entities
with open("TrumpArticle.txt", encoding='utf8') as f:
    # Read in the whole file as a single string but strip out any spaces at
    # the start and end of the file
    raw_read = f.read().strip()
    
# Apply the pre-trained model to the raw text string to extract named entities
article = nlp(raw_read)

# Store the Named Entity categories (stored in label_ for each entity) in the 
# article in a list. The named entities themselves are stored in article.ents
labels = [x.label_ for x in article.ents]

# Print all of the named entities with their frequencies
ne_list = [str(ne) for ne in article.ents]
ne_freq_dictionary = {ne:ne_list.count(ne) for ne in ne_list}

print (ne_freq_dictionary)
print ()

# Print the ten most common recognised entities with their frequencies
print ("The 10 most common named entities found, and their frequencies : ")
most_common_ne = Counter(ne_freq_dictionary).most_common(10)

print (most_common_ne)
print ()
    
# Print the 16th sentence (sentence 15) of the article
sentences = list(article.sents)
print ("16th Sentence : ")
print (sentences[15])
print ()

# List the unique named entity categories predicted in the text, and ask the
# user to select one to see all the named entities predicted in that category
unique_label_set = set(labels)

while True:
    print ("Found the following Named Entity Categories : ")
    
    for label in unique_label_set:
        print (label)
    
    while True:
        selected_label = input("List named entities for which label? : ")
        if selected_label in unique_label_set:
            break
        else:
            print ("No such label.  Please try again.")
    
    # Store a list of named entity values for the specified category
    ne_subl = [str(ne) for ne in article.ents if str(ne.label_) == 
               selected_label]
    
    # Convert to a set so we only have unique values
    ne_subl_set = set(ne_subl)
    
    print ()
    print ("The following named entities were found and predicted to be of ",
           selected_label, " category : ", sep="")
    
    for ne in ne_subl_set:    
        print (ne)
    
    print ()
    
