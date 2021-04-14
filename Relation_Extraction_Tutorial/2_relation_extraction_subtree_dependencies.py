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

from spacy import displacy

import en_core_web_sm

# Load spacy model
nlp = en_core_web_sm.load()

"""
METHOD 2 - Using Subtree matching to look for dependency structures within a
sentence that identify the subject(s) and object(s) and the links between
them.
"""

text = "Tableau was recently acquired by Salesforce"
#text = "Careem, a ride hailing major in middle east was acquired by Uber"

# Apply the loaded SpaCy model to the text
doc = nlp(text)

# Plot and display the dependency graph using displacy
# 
# Use this for Spyder (will spin up a server) - see :
# https://spacy.io/usage/visualizers
# Once spun up, go to server address in console (e.g. 0.0.0.0:5000)
displacy.serve(doc, style='dep')

# Or, use this for Jupyter :
#displacy.render(doc, style='dep')

# Print tokens, dependencies, POS tags
for tok in doc:
    print (f"{tok.text} --> {tok.dep_} --> {tok.pos_}")
    
print ()

# Define a function that takes as its input a SpaCy document.  This function
# will iterate through all the tokens in the input document, and check to see
# if the token has a dependency tag that contains "subjpass" (passive subject)
# such as 'nsubjpass' (nominal subject (passive)) (remember you can use
# spacy.explain to look up POS and dependency tags such as 'nsubjpass').  If
# it does, it will store the text of the token in y.  It will then iterate
# through all of the tokens to look for an object (there are different types
# of object, so this will look for any dependency tags that end with "obj").
# Once it finds one, it will store the text of the token in x.  The function
# will then return both x (the object) and y (the passive subject).
#
# Note - this function will only work properly if there is one object and one
# passive subject (so realistically a single sentence).  More than one object
# or passive subject would cause only the last one in the text to be returned.
# So this would need adapting if that's what you need.
#
# A nominal is a word or group of words that function together as a noun. A
# nominal gives more specific details than a simple noun.  E.g. "nice cup of
# tea" is an example of a nominal - it gives more description than the head
# noun (cup) - we now know that it is a cup filled with tea, and that it is
# nice.  See https://www.thoughtco.com/nominal-in-grammar-1691431
# Because nominals function as nouns, they can do whatever nouns can - be a
# subject, an object or a predictive nominative.
# A nominal subject (passive) is therefore one in which the nominal is acting
# as the thing to which the action is being done.  In our example sentence
# "Tableau was recently acquired by Salesforce", Tableau is a nominal subject
# passive ('nsubjpass') because it is the thing to which the action of 
# acquiring was being done.
def subtree_matcher_old(doc):
    x = ''
    y = ''
    
    # Iterate through all the tokens in the input document
    for i, tok in enumerate(doc):
        # extract subject
        if tok.dep_.find("subjpass") == True:
            y = tok.text
            
    # Extract object
    if tok.dep_.endswith("obj") == True:
        x = tok.text
        
    # Return object and passive subject
    return x,y

# Call the function above to grab out the object and passive subject of doc
obj, subj = subtree_matcher_old(doc)

# Print the identified subject and object
print (f"Subject : {subj}, Object: {obj}")
print ()

# Do the same with this text
text_2 = "Careem, a ride hailing major in middle east was aquired by Uber"

doc_2 = nlp(text_2)

obj_2, subj_2 = subtree_matcher_old(doc_2)

print (f"Subject : {subj_2}, Object: {obj_2}")
print ()

# Do the same with this text.  You'll note in this example, things don't work
# properly.  This sentence is an active version of the first example sentence.
# Therefore, the subject and object have been interchanged, and the dependency
# tag for the subject is no longer "nsubjpass" but is now "nsubj" - ie a
# subject in a sentence in the active voice (rather than the passive voice).
# So we need to update our logic to accomodate this (see below)
text_3 = "Salesforce recently acquired Tableau."

doc_3 = nlp(text_3)

obj_3, subj_3 = subtree_matcher_old(doc_3)

print (f"Subject : {subj_3}, Object: {obj_3}")
print ()

for tok in doc_3:
    print (f"{tok.text} --> {tok.dep_} --> {tok.pos_}")
    
print ()

# This new function is similar to the one above, but this time we check first
# to see whether the sentence is in the active or passive voice.  Then,
# if it's passive, we do what we did before, but if it's active, then we look
# for the dependency tag "subj" instead of "subjpass".
def subtree_matcher(doc):
    subjpass = False
    
    for i, tok in enumerate(doc):
        # Find dependency tag that contains the text "subjpass"
        if tok.dep_.find("subjpass") == True:
            subjpass = True
            
    x = ''
    y = ''
    
    # if sentence is passive
    if subjpass == True:
        for i, tok in enumerate(doc):
            if tok.dep_.find("subjpass") == True:
                y = tok.text
                
            if tok.dep_.endswith("obj") == True:
                x = tok.text
                
    # if sentence is not passive
    else:
        for i, tok in enumerate(doc):
            if tok.dep_.endswith("subj") == True:
                x = tok.text
                
            if tok.dep_.endswith("obj") == True:
                y = tok.text
                
    return x,y

# If we try the new function above with this active voice sentence, we can
# see that it now correctly pulls out the subject and object
text_3 = "Salesforce recently acquired Tableau."

doc_3 = nlp(text_3)

obj_3, subj_3 = subtree_matcher(doc_3)

print (f"Subject : {subj_3}, Object: {obj_3}")
print ()

doc = nlp(text)

obj, subj = subtree_matcher(doc)

print (f"Subject : {subj}, Object: {obj}")
print ()

# Now let's try with another sentence.  This time we find a new problem - here
# we've got a single subject (Father) but two objects (victim and meal).
# Looking at the dependency tree / tags, we see that victim has a tag of "dobj"
# and meal has a tage of "pobj".  "dobj" is a Direct Object - this is one that
# answers the question "whom?" or "what?" after an action verb.  So in this
# case, the father "took" - and who did he take?  The victim.  Therefore,
# victim is the Direct Object.  "pobj" is an Object of Preposition - this is
# one that answers "whom?" or "what?" after a preposition in a prepositional
# phrase.  Remember, a preposition governs a noun or pronoun to express a
# relation with another element in the clause (words such as by, to, at etc).
# In this case, the preposition is "for" - it identifies the reason why the
# father took the victim out (for a meal).  So, the Object of Preposition here
# is "meal" - it's the object in the prepositional phrase. See :
# https://webapps.towson.edu/ows/nouns.htm
# So, our simple functions above won't cut the mustard, because there are two
# objects here, and so the last one in the sentence (in this case, the
# object of preposition) would be returned as THE object.  But in reality, we
# probably want the direct object, or at least to be able to choose between
# them.  See below for how we can do this.
text_4 = "Father took victim out for meal"

doc_4 = nlp(text_4)

for tok in doc_4:
    print (f"{tok.text} --> {tok.dep_} --> {tok.pos_}")
    
displacy.serve(doc_4, style='dep')

obj_4, subj_4 = subtree_matcher(doc_4)

print (f"Subject : {subj_4}, Object: {obj_4}")
print ()

# A new version of our subtree matcher function.  Here, rather than returning
# a single subject and a single object, we return a list of subjects and
# objects.  For the list of objects, we actually return a list of tuples,
# where the first element of the tuple is the text of the token identified as
# an object, and the second is the dependency tag, so we can identify what
# type of object it is.  This would allow us, for example, to filter only
# direct objects, if that is all we're interested in.
def subtree_matcher_listver(doc):
    subjpass = False
    
    for i, tok in enumerate(doc):
        # Find dependency tag that contains the text "subjpass"
        if tok.dep_.find("subjpass") == True:
            subjpass = True
            
    object_list = []
    subject_list = []
    
    # if sentence is passive
    if subjpass == True:
        for i, tok in enumerate(doc):
            if tok.dep_.find("subjpass") == True:
                subject_list.append(tok.text)
                
            if tok.dep_.endswith("obj") == True:
                obj_text = tok.text
                obj_dtag = tok.dep_
                object_list.append((obj_text, obj_dtag))
                
    # if subjpass == 0 then sentence is not passive
    else:
        for i, tok in enumerate(doc):
            if tok.dep_.endswith("subj") == True:
                subject_list.append(tok.text)
                
            if tok.dep_.endswith("obj") == True:
                obj_text = tok.text
                obj_dtag = tok.dep_
                object_list.append((obj_text, obj_dtag))
                
    return object_list, subject_list

obj_l, subj_l = subtree_matcher_listver(doc_4)

print (f"Subject(s) : {subj_l}")
print (f"Object(s) : {obj_l}")
print ()

# WE CAN USE spacy.explain('x') where x is a dependency tag or a POS tag and
# it'll tell you what it means

# See https://webapps.towson.edu/ows/nouns.htm for explanation of direct
# object vs object of preposition




