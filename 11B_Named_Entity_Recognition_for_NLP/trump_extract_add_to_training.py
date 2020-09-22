#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:23:22 2020

@author: dan
"""

# import spacy and the downloaded en_core_web_sm pre-trained model
# Also import random for shuffling of training data
import spacy
from spacy.util import minibatch, compounding
import en_core_web_sm
import random

# Load the pre-trained model as a language into a variable called nlp
nlp = en_core_web_sm.load()

# Read in the document for which we want to extract named entities
with open("TrumpArticleEnhanced.txt", encoding='utf8') as f:
    # Read in the whole file as a single string but strip out any spaces at
    # the start and end of the file
    raw_read = f.read().strip()
    
# Apply the pre-trained model to the raw text string to extract named entities
article = nlp(raw_read)

# Store the Named Entity categories (stored in label_ for each entity) in the 
# article in a list. The named entities themselves are stored in article.ents
labels = [x.label_ for x in article.ents]

# Print each predicted named entity, along with its predicted category
for i in range(len(article.ents)):
    print (article.ents[i], " : ", labels[i], sep="")
    
# By default, SpaCy classifies PenCHORD as a Geo-Political Entity (GPE).  But
# ideally, we want it recognised as an organisation (ORG).  Let's train the
# model to do this.

# First, we need to get the en_core_web_sm model's Named Entity Recognition 
# pipeline components so we can add labels
ner_pipeline_components = nlp.get_pipe("ner")

# Now let's give it some example sentences, and flag up where the Named
# Entities are, and what type they are
list_of_training_sentences = [
    "PenCHORD is a fantastic team because Dan Chalk is in it.",
    "Mike Allen loves System Dynamics."
    ]
list_of_named_entities = [[list_of_training_sentences[0],
                           [["PenCHORD", 0, 0, "ORG"], 
                           ["Dan Chalk", 0, 0, "PERSON"]]],
                          [list_of_training_sentences[1],
                           [["Mike Allen", 0, 0, "PERSON"],
                           ["System Dynamics", 0, 0, "WORK_OF_ART"]]]
                          ]

# Find the start and end character positions of all the named entities in each
# training sentence
for sublist in list_of_named_entities:
    for ne_prop_list in sublist[1]:
        # The find method returns the index of the starting character in the
        # string for a given substring
        start_char_index = sublist[0].find(ne_prop_list[0])
        
        # We can find the end character index by simply taking length of the
        # substring, and adding it to the starting character index
        length_of_substring = len(ne_prop_list[0])
        
        end_char_index = start_char_index + length_of_substring
        
        # Update the start and end character indices stored in the list of
        # properties for this named entity
        ne_prop_list[1] = start_char_index
        ne_prop_list[2] = end_char_index
        
        # Add the entity label to the NER pipeline
        ner_pipeline_components.add_label(ne_prop_list[3])
    
# We want to disable all other pipelines other than the NER pipeline during
# training, because we're only updating Named Entity Recognition training here.
# First we grab the names of the other pipelines, and then we can disable
# these other pipelines whilst training the NER pipeline.
other_pipelines = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

# Set up the training data in the format needed by SpaCy.  Specifically as a
# list of tuples, where each tuple represents a training sentence.  The first
# element of each tuple consists of the training sentence as a string, and
# the second element consists of a dictionary with index 'entities', and value
# as a list of tuples, with each tuple representing a named entity in the
# training sentence.  The first element of the tuple is the start character
# of the named entity, the second the end character, and the third the label
# for the named entity.  Specifically :
# [ (training_sentence_1, {'entities':[(start_char_1, end_char_1, label_1),
#                                      (start_char_2, end_char_2, label_2)]}),
#   (training_sentence_2, {'entities':[(start_char_1, end_char_1, label_1),
#                                      (start_char_2, end_char_2, label_2)]}) ]
training_data = []

# For each sublist containing sentence followed by list of named entity
# property lists
for sublist in list_of_named_entities:
    # Start a new list of tuples to add for this training sentence
    list_of_entity_tuples = []
    
    # For each named entity property list (ie each named entity)
    for ne_prop_list in sublist[1]:
        # Add elements an indices 1, 2 and 3 (start char, end char, label) as
        # a tuple and add to the list of tuples we're building
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
    # (training_sentence_1, {'entities':[(start_char_1, end_char_1, label_1),
    #                                    (start_char_2, end_char_2, label_2)]})
    outer_tuple = (sublist[0], {'entities':list_of_entity_tuples})
    
    training_data.append(outer_tuple)

# Set up number of training iterations to go through
number_of_training_iterations = 100

# Now we're going to train the model with our training data.  We'll hold the
# non-NER pipelines as disabled whilst we do this.  The * preceding 
# other_pipes passed into the disable_pipes method just means 'unpack this
# list', so the unpacked list gets passed in
with nlp.disable_pipes(*other_pipelines):
    # For the specified number of training iterations
    for iteration in range(number_of_training_iterations):
        # Randomly shuffle the training data.  This is less important here
        # as we've only got two sentences and four named entities, but with
        # lots more data this becomes more important
        random.shuffle(training_data)
        
        # Set up a dictionary to store losses (values that represent a 
        # summation of errors between training and validation. So lower loss = 
        # better.
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
            # text (sentence) data and annotation (label, char positions etc) 
            # data, ready to be passed in to the training
            texts, annotations = zip(*batch)
            
            # Update the language (train it) - tell it the sentences (texts),
            # label data (annotations), dropout rate (this is the % of nodes
            # and their links will be randomly dropped from the neural
            # network during training - we do this to prevent over-fitting
            # where the neural network just ends up being very good at 
            # predicting the training data, but nothing else.  50% dropout
            # rate is pretty standard) and where to store the losses (which
            # in this case is the losses dictionary we set up above)
            nlp.update(texts, annotations, drop=0.5, losses=losses)
            
        # Print the losses for this iteration of training
        print ("Losses", losses)
        
# Let's save our new model to disk, so we can reload it at any time using
# nlp = spacy.load('model_name')
nlp.to_disk('enhanced_en_core_web_sm')

# Now we've trained the model, let's test it, first on the sentences it was
# trained with
print ()
print ("Test on sentences used for training")
print ("-----------------------------------")

for text, _ in training_data:
    # Apply the SpaCy model to the sentence
    test_doc = nlp(text)
    
    # Print the sentence, followed by the named entities predicted (both the
    # text for the entity and its predicted label).
    print ("Sentence : ", text, sep="")
    print ("Entities", [(ent.text, ent.label_) for ent in test_doc.ents])
    
# Now let's test it on some new sentences with these named entities in them
print ()
print ("Test on new, unseen sentences")
print ("-----------------------------")

list_of_test_sentences = [
    "Dan Chalk recently built a System Dynamics model",
    "PenCHORD is lucky to have Mike Allen as one of its modellers",
    "Dan Chalk and Mike Allen build System Dynamics models for PenCHORD"]

for sentence in list_of_test_sentences:
    test_doc_2 = nlp(sentence)
    
    # Print the sentence, followed by the named entities predicted (both the
    # text for the entity and its predicted label).
    print ("Sentence : ", sentence, sep="")
    print ("Entities", [(ent.text, ent.label_) for ent in test_doc_2.ents])
    
# Now let's try named entity recognition on our enhanced Trump article again,
# to make sure it no longer picks up PenCHORD as a GPE.

# Apply the pre-trained model to the raw text string to extract named entities
article = nlp(raw_read)

# Store the Named Entity categories (stored in label_ for each entity) in the 
# article in a list. The named entities themselves are stored in article.ents
labels = [x.label_ for x in article.ents]

# Print each predicted named entity, along with its predicted category
print ()
for i in range(len(article.ents)):
    print (article.ents[i], " : ", labels[i], sep="")
    
