#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 08:22:45 2021

@author: dan
"""


# Following tutorial here :
# https://www.analyticsvidhya.com/blog/2019/09/introduction-information-extraction-python-spacy/

# Remember to download spacy model using 
# python -m spacy download en_core_web_sm

import spacy

from spacy.matcher import Matcher
from spacy import displacy

import en_core_web_sm

# Load spacy model
nlp = en_core_web_sm.load()

"""
METHOD 1 - Using Hearst Patterns for rule-based matching in SpaCy (named after
Prof Marti Hearst, Computational Linguistics Professor at University of
California, Berkeley)

Hearst Patterns are a set of patterns for recognizing hyponymy.  Hyponymy
describes the semantic relationship between a hyponym (a subtype) and a
hypernym (a supertype).  For example : "cars", "buses", "vans" would all be 
hyponyms of the hypernym "vehicle".

The Hearst Patterns are as follows (in each case, X represents the hyponym
and Y the hypernym):
- X and other Y (e.g cars and other vehicles)
- X or other Y (e.g. cars or other vehicles)
- Y such as X (e.g. vehicles such as cars)
- such Y as X (e.g. such vehicles as cars)
- Y including X (e.g. vehicles including cars)
- Y, especially X (e.g. vehciles, especially cars)
"""

# Hearst Pattern : Y such as X
print ("Hearst Pattern : Y such as X")
print ("----------------------------")

# simple example text
text = ("GDP in developing countries such as Vietnam will continue growing " +
        "at a high rate")

# Apply the loaded SpaCy model to the text
doc = nlp(text)

# Print tokens, dependencies, POS tags
#
# tokens = the individual words or punctuation marks
#
# dependencies = describes how words are connected to each other (e.g. "amod"
# is an "adjectival modifier" and therefore indicates that the role the word
# plays in the given sentence is to modify an adjective).  You can use
# spacy.explain("X") where X is the POS Tag or Dependency Tag you want the
# grammatical name for (so, for example, spacy.explain("amod") will output
# 'adjectival modifier'.  Of course, unless you're a grammar buff, you'll
# probably need to Google what many of these mean :) )
#
# POS tags = Parts of Speech tags.  Every word in the English Language belongs
# to a part of Speech (Nouns, Adverbs etc), of which there are 9 in the English
# Language.  The POS Tag indicates which one.
for tok in doc:
    print (f"{tok.text} --> {tok.dep_} --> {tok.pos_}")
    
print ()

# Define the pattern
# See https://spacy.io/usage/rule-based-matching
# amod = adjectival modifier, ? means can occur once or not at all
# DEP = Dependency Tag
# POS = POS Tag
# OP = Operator or quantifier
# LOWER = The lowercase form of the token text
# PROPN = Proper Noun (a named noun, making it specific)
# So, this pattern says to look for an optional adjectival modifier, followed
# by a noun, followed by the words "such as", followed by a proper noun.
pattern = [{'DEP':'amod', 'OP':"?"}, 
           {'POS':'NOUN'},
           {'LOWER':'such'},
           {'LOWER':'as'},
           {'POS':'PROPN'}]

# Extract the pattern from the text
# Create a Matcher object.  Pass in the vocab for the loaded SpaCy model
# (the vocab stores the vocabularly and other data shared across a language)
matcher = Matcher(nlp.vocab)

# See https://stackoverflow.com/questions/66164156/problem-with-using-spacy-matcher-matcher-matcher-add-method
# Define the Matcher object
# (matcher now only takes 2 positional arguments in Spacy 3 - an ID for the
# matcher, and a list of patterns (which must be passed as a list, even if
# there is only 1 pattern)
matcher.add("matching_1", [pattern])

# Apply the matcher to the SpaCy document
matches = matcher(doc)

# The matcher returns a list of three-element tuples, in which each tuple is :
# (match_id, start, end).  match_id is the hash value of the ID of the matcher
# ("matching_1" in this case).  start and end represent the token positions of
# where the identified match starts and ends (So the first token is 0, second
# token is 1 etc).  We'll get a tuple returned for every match identified.
# Here, we know we only have one match, so we can just refer to matches[0],
# which refers to the first (and only) tuple.  We can then specify the "span"
# (the matched text) using the start and end token positions stored in 
# the second and third elements of the tuple (so matches[0][1] and 
# matches[0][2] respectively)
span = doc[matches[0][1]:matches[0][2]]

# Print the text that matched the pattern
print (span.text)
print ()

# Hearst Pattern : X and/or Y
print ("Hearst Pattern X and/or Y")
print ("-------------------------")

doc = nlp("Here is how you can keep your car and other vehicles clean.")

# Print tokens, dependencies, POS tags
for tok in doc:
    print (f"{tok.text} --> {tok.dep_} --> {tok.pos_}")
    
print ()

# Define the pattern
pattern = [{'DEP':'amod', 'OP':"?"},
           {'POS':'NOUN'},
           {'LOWER':'and', 'OP':"?"},
           {'LOWER':'or', 'OP':"?"},
           {'LOWER':'other'},
           {'POS':'NOUN'}]

# Create a Matcher object
matcher = Matcher(nlp.vocab)

# Define the Matcher object
matcher.add("matching_1", [pattern])

# Apply the matcher to the SpaCy document
matches = matcher(doc)

# Grab the span of the matched text and print it
span = doc[matches[0][1]:matches[0][2]]
print (span.text)

