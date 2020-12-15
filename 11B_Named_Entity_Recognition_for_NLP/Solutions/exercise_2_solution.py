#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:23:22 2020

@author: dan
"""

import spacy
from spacy.util import minibatch, compounding
import en_core_web_sm
import random
import csv

# Load the pre-trained model as a language into a variable called nlp
nlp = en_core_web_sm.load()

# Read in the document for which we want to extract named entities
with open("exercise_2_article.txt", encoding='utf8') as f:
    # Read in the whole file as a single string but strip out any spaces at
    # the start and end of the file
    raw_read = f.read().strip()

# Applies the standard pre-trained model to the raw text string to extract
# named entities
article_standard = nlp(raw_read)

# Store the Named Entity categories (stored in label_ for each entity) in the 
# article in a list. The named entities themselves are stored in article.ents
labels_standard = [x.label_ for x in article_standard.ents]

# Print each predicted named entity, along with its predicted category
print ()
for i in range(len(article_standard.ents)):
    print (article_standard.ents[i], " : ", labels_standard[i], sep="")

list_of_named_entities = []

# First, we need to get the en_core_web_sm model's Named Entity Recognition 
# pipeline components so we can add labels
ner_pipeline_components = nlp.get_pipe("ner")

# Now let's read in our csv file to get our training sentences, named
# entities and associated labels
with open("ex_2_training.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    
    for row in reader:            
        # Take a copy of the row and store in a new list
        temp_row_list = row.copy()
        
        # Remove any empty string values from the list (these will be
        # entries where there are no more named entities for this sentence)
        temp_row_list = [x for x in temp_row_list if x != '']
        
        # Set up temporary list to store lists for each named entity
        temp_label_list = []
        
        # For each pair of named entity text and label, create a temporary
        # list of the format [ne_text, 0, 0, ne_label], and then append
        # this to the list of lists we set up above
        for i in range(1, len(temp_row_list), 2):
            temp_inner_label_list = [row[i], 0, 0, row[(i+1)]]
            temp_label_list.append(temp_inner_label_list)
        
        # Append a list made up of the sentence and the list of lists of
        # label data to the list_of_named_entities, so that 
        # the list_of_named_entities is of the format :
        # [[sent_1, [[ne_1, 0, 0, ne_1_label],[ne_2, 0, 0, ne_2_label]]]]
        list_of_named_entities.append([temp_row_list[0], temp_label_list])
        
# Find the start and end character positions of all the named entities in
# each training sentence
for sublist in list_of_named_entities:
    for ne_prop_list in sublist[1]:
        # The find method returns the index of the starting character in
        # the string for a given substring
        start_char_index = sublist[0].find(ne_prop_list[0])
        
        # We can find the end character index by simply taking length of 
        # the substring, and adding it to the starting character index
        length_of_substring = len(ne_prop_list[0])
        
        end_char_index = start_char_index + length_of_substring
        
        # Update the start and end character indices stored in the list of
        # properties for this named entity
        ne_prop_list[1] = start_char_index
        ne_prop_list[2] = end_char_index
        
        # Add the entity label to the NER pipeline
        ner_pipeline_components.add_label(ne_prop_list[3])
    
# We want to disable all other pipelines other than the NER pipeline during
# training, because we're only updating Named Entity Recognition training.
# First we grab the names of the other pipelines, and then we can disable
# these other pipelines whilst training the NER pipeline.
other_pipelines = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

# Set up the training data in the format needed by SpaCy.  Specifically as
# a list of tuples, where each tuple represents a training sentence.  The 
# first element of each tuple consists of the training sentence as a string
# and the second element consists of a dictionary with index 'entities', 
# and value as a list of tuples, with each tuple representing a named 
# entity in the training sentence.  The first element of the tuple is the 
# start character of the named entity, the second the end character, and 
# the third the label for the named entity.  Specifically :
# [ (training_sentence_1, {'entities':[(start_char_1, end_char_1, label_1),
#                                   (start_char_2, end_char_2, label_2)]}),
#   (training_sentence_2, {'entities':[(start_char_1, end_char_1, label_1),
#                                  (start_char_2, end_char_2, label_2)]}) ]
training_data = []

# For each sublist containing sentence followed by list of named entity
# property lists
for sublist in list_of_named_entities:
    # Start a new list of tuples to add for this training sentence
    list_of_entity_tuples = []
    
    # For each named entity property list (ie each named entity)
    for ne_prop_list in sublist[1]:
        # Add elements an indices 1, 2 and 3 (start char, end char, label)
        # as a tuple and add to the list of tuples we're building
        # This is for the dictionary of entities we need to set up, as
        # explained above.
        # Remember - we can't change a tuple once it's been defined
        list_of_entity_tuples.append((ne_prop_list[1],
                                      ne_prop_list[2],
                                      ne_prop_list[3]))
        
    # Once we've picked up all the named entity tuples for this sentence
    # (ie all the named entities), we can assemble the outer tuple for this
    # sentence and append it to the training data
    # Remember, this needs to be in the format
    #(training_sentence_1,{'entities':[(start_char_1, end_char_1, label_1),
    #                                (start_char_2, end_char_2, label_2)]})
    outer_tuple = (sublist[0], {'entities':list_of_entity_tuples})
    
    training_data.append(outer_tuple)

# Set up number of training iterations to go through
number_of_training_iterations = 100

# Now we're going to train the model with our training data.  We'll hold
# the non-NER pipelines as disabled whilst we do this.  The * preceding 
# other_pipes passed into the disable_pipes method just means 'unpack this
# list', so the unpacked list gets passed in
with nlp.disable_pipes(*other_pipelines):
    # For the specified number of training iterations
    for iteration in range(number_of_training_iterations):
        # Randomly shuffle the training data.
        random.shuffle(training_data)
        
        # Set up a dictionary to store losses (values that represent a 
        # summation of errors between training and validation.
        losses = {}
        
        # Batch up the training examples using SpaCy's minibatch
        # The size attribute basically specifies how to batch up the data
        # To read more about this, see 
        # https://spacy.io/api/top-level#util.minibatch
        # and
        # https://spacy.io/api/top-level#util.compounding
        batches = minibatch(training_data,
                            size=compounding(4.0, 32.0, 1.001))
        
        # For each batch of training data
        for batch in batches:
            # The zip function joins multiple tuples together by taking the
            # joining the ith element in tuple a with the ith element in
            # tuple b etc to form a tuple of bundled up tuples
            # Here, that's done with the batches and we separate out the 
            # text (sentence) data and annotation (label, char positions 
            # etc) data, ready to be passed in to the training
            texts, annotations = zip(*batch)
            
            # Update the language (train it)-tell it the sentences (texts),
            # label data (annotations), dropout rate (this is % of nodes
            # nodes and their links will be randomly dropped from the NN
            # during training - we do this to prevent over-fitting
            # where the neural network just ends up being very good at 
            # predicting the training data, but nothing else.  50% dropout
            # rate is pretty standard) and where to store the losses (which
            # in this case is the losses dictionary we set up above)
            nlp.update(texts, annotations, drop=0.5, losses=losses)
            
        # Print the losses for this iteration of training
        print ("Losses", losses)
        
# Let's save our new model to disk, so we can reload it at any time using
# nlp = spacy.load('model_name')
nlp.to_disk('enhanced_ex_2')

# Load in the enhanced model we trained and saved above
nlp_e = spacy.load('enhanced_ex_2')

# Applies the enhanced model to the raw text string to extract named entities
article_enhanced = nlp_e(raw_read)

# Store the Named Entity categories (stored in label_ for each entity) in the 
# article in a list. The named entities themselves are stored in article.ents
labels_enhanced = [x.label_ for x in article_enhanced.ents]

# Print each predicted named entity, along with its predicted category
print ()
for i in range(len(article_enhanced.ents)):
    print (article_enhanced.ents[i], " : ", labels_enhanced[i], sep="")
    
