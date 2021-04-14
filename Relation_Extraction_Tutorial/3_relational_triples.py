#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 08:22:45 2021

@author: dan
"""

# Remember to download spacy model using 
# python -m spacy download en_core_web_sm

import spacy
import pandas as pd

from spacy import displacy

import en_core_web_sm

# Load spacy model
nlp = en_core_web_sm.load()

# A really important and useful aspect of relation extraction is forming a
# "Relational Triple".  A Relational Triple is a tuple of three elements - two
# of which are entities, and the remaining one is the relationship between
# these two entities.  So, for example, if we take the sentence
# "Talented director Christopher Nolan directed the sci-fi film Interstellar" 
# then we want our Relational Triple to be 
# (Christopher Nolan, directed, Interstellar).
# To do this, we can use what we learned before in
# relation_extraction_subtree_dependencies.py and combine this with looking
# for the "root" of a sentence.

# In dependency structures, the root of a sentence is the word (usually a verb)
# that links one part of a sentence with another.

# Let's look at the dependency tree of our example sentence
text = ("Talented director Christopher Nolan directed the sci-fi film " +
        "Interstellar.")

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

# Looking at the dependency tree visualisation, we see that there are two
# sides to this sentence - the bit that talks about Christopher Nolan (and
# that he's a talented director) and the bit that talks about Interstellar 
# (and that it's a sci-fi film).  We can also see that the word "directed"
# links the two semantic sections of this sentence together - it is the root
# from which the dependency paths in the tree begin.  The fact that this is
# the root of the dependency paths suggests that this is the thing that relates
# the two parts of the sentence.  In other words, this is our relation that
# we need for our Relational Triple.
# Of course, it's not practical to manually inspect a dependency tree every
# time we need to find the root / relation.  Fortunately, SpaCy allows us to
# find the root easily

# Here, we only have a single sentence in our text, but we may want to work
# with more than one sentence at a time, and each sentence will have its own
# root.  So let's write our code to deal with multiple sentences to 
# future-proof things.

# Let's set up a dictionary to store sentence texts as keys and the roots as
# values
sentence_root_dictionary = {}

# Individual sentences are stored in doc.sents, so we can iterate through
# them.  For each, we'll grab the sentence and the root (which SpaCy has
# identified for us, so all we need to do is grab .root from the sentence).
# Note that sentences are stored as "spans", so if we want to store the text
# as a string, we need to use .text to grab the text itself out of the span.
for sentence in doc.sents:
    sentence_root_dictionary[sentence.text] = sentence.root.text
    
# Define a function to grab out the subject and object from a sentence.  We
# amend this from the function we built in 
# relation_extraction_subtree_dependencies.py.  We first check if the sentence
# is in the passive or active voice.  Then we set up a string to catch a
# candidate subject, and one to catch a candidate object.  If the sentence is
# passive, then we'll look for a subject with dependency tag containing 
# "subjpass" (passive subject), and an object with dependency tag "pobj"
# (object of preposition).  If the sentence is active, then we'll look for a
# subject with a dependency tag containing "subj" and an object with a
# dependency tag of "dobj" (direct object).  Then we'll return the object and
# subject.
def subject_object_extractor_v1(sentence):
    subjpass = False
    
    for tok in sentence:
        # Find dependency tag that contains the text "subjpass"
        if tok.dep_.find("subjpass") == True:
            subjpass = True
    
    candidate_subject = ''
    candidate_object = ''
    
    # if sentence is passive
    if subjpass == True:
        for tok in sentence:
            if tok.dep_.find("subjpass") == True:
                candidate_subject = tok.text
                
            if tok.dep_ == "pobj":
                candidate_object = tok.text
                
    # if sentence is not passive
    else:
        for tok in sentence:
            if tok.dep_.endswith("subj") == True:
                candidate_subject = tok.text
                
            if tok.dep_ == "dobj":
                candidate_object = tok.text

    return candidate_object, candidate_subject

# Let's have a list that will store our relational triples
relational_triples_list = []

# Now we'll iterate through each sentence (we've only got one at the moment)
# and call the function we wrote above on it to get the object and subject.
# Then we'll add a three element tuple of form (subject, root, object) to our
# list of relational triples
for sentence in doc.sents:
    obj, subj = subject_object_extractor_v1(sentence)
    
    relational_triples_list.append((subj,sentence.root.text,obj))
    
# Now let's print the list of triples (we should only have one)
print (relational_triples_list)

# So, we got a relational triple out, but it isn't quite what we hoped for.
# Remember, we want :
# (Christopher Nolan, directed, Interstellar)
# We got :
# (Nolan, directed, film)
# Not bad for a first attempt, but let's look at the two problems and see if
# we can fix them.
# Problem 1 : We got "Nolan" instead of "Christopher Nolan"
# Problem 2 : We got "film" instead of "Interstellar"
# If we look at our dependency tree visualisation in displacy, we can see
# what's going on.  For problem 1, we see that "Nolan" is picked up as a
# Proper Noun (POS Tag) with a dependency tag of nsubj (nominal subject). But
# if we look to the left of it, we see that "Nolan" is also linked to the
# word "Christopher" (also a Proper Noun), and the dependency tag linking them
# is "compound".  In grammar, a compound is two or more words that link
# together to create a new meaning.  Here, they create the full name of our
# director.  But we need to be careful, because "director" is also linked to
# "Nolan" as a compound.  So, what we want to do is grab any compounds that
# are also Proper Nouns.
# For problem 2, we see that "film" is linked to "Interstellar" with the
# dependency tag "appos" - this indicates an Appositional Modifier.  This is
# a modifier that directly follows a noun to define, modify, name or describe
# that noun.  Here, it's playing the role of naming the film.  So, if there's
# an appositional modifier present, we probably want to grab that instead.

# Let's rewrite our function to try to solve these issues
def subject_object_extractor_v2(sentence):
    # We'll store the text, pos and dependency tags together in a Pandas
    # Dataframe to make it easier to access the tokens before and after the
    # token we're looking at
    token_text_list = [tok.text for tok in sentence]
    token_pos_list = [tok.pos_ for tok in sentence]
    token_dep_list = [tok.dep_ for tok in sentence]

    token_df = pd.DataFrame()
    
    token_df['token_text'] = token_text_list
    token_df['token_pos'] = token_pos_list
    token_df['token_dep'] = token_dep_list
    
    # Let's print the dataframe
    print (token_df)
    
    # Let's check if the sentence is passive
    subjpass = False
    
    for i in range(len(token_df)):
        if token_df.loc[i]['token_dep'].find("subjpass") == True:
            subjpass = True
            
    candidate_subject = ''
    candidate_object = ''
                
    # if sentence is active
    if subjpass == False:
        for i in range(len(token_df)):
            # if the current token has a direct object dependency tag
            if token_df.loc[i]['token_dep'] == "dobj":
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the object as being both of these tokens
                    # together
                    if token_df.loc[i-1]['token_dep'] == "compound":
                        candidate_object = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the object
                    else:
                        candidate_object = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate object.  If not, 
                # just take this token as the object.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate object
                    if (i+1) == len(token_df):
                        candidate_object = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_object = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_object = (
                                token_df.loc[i]['token_text']
                            )
                            
            # if the current token's dependency indicates it is a subject
            if token_df.loc[i]['token_dep'].endswith("subj") == True:
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the subject as being both of these tokens
                    # together
                    if token_df.loc[i-1]['token_dep'] == "compound":
                        candidate_subject = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the subject
                    else:
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate subject.  If not, 
                # just take this token as the subject.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate subject
                    if (i+1) == len(token_df):
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_subject = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_subject = (
                                token_df.loc[i]['token_text']
                            )
                
    # if sentence is passive
    else:
        for i in range(len(token_df)):
            # if the current token has an Object of Prepostion depedency tag
            if token_df.loc[i]['token_dep'] == "pobj":
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the object as being both of these tokens
                    # together
                    if token_df.loc[i-1]['token_dep'] == "compound":
                        candidate_object = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the object
                    else:
                        candidate_object = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate object.  If not, 
                # just take this token as the object.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate object
                    if (i+1) == len(token_df):
                        candidate_object = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_object = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_object = (
                                token_df.loc[i]['token_text']
                            )
                            
            # if the current token's dependency indicates it is passive
            # subject
            if token_df.loc[i]['token_dep'].find("subjpass") == True:
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the subject as being both of these tokens
                    # together
                    if token_df.loc[i-1]['token_dep'] == "compound":
                        candidate_subject = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the subject
                    else:
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate subject.  If not, 
                # just take this token as the subject.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate subject
                    if (i+1) == len(token_df):
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_subject = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_subject = (
                                token_df.loc[i]['token_text']
                            )
            
    return candidate_object, candidate_subject
                 
# Now we've rewritten our function, let's see how well it performs on our
# sentence.  We'll reset the relational triples list, then call the new
# function to extract the object and subject, and then assemble and print our
# relational triple
relational_triples_list = []

for sentence in doc.sents:
    obj, subj = subject_object_extractor_v2(sentence)
    
    relational_triples_list.append((subj,sentence.root.text,obj))
    
print (relational_triples_list)

# Great!  We've got the relational triple we wanted :
# ('Christipher Nolan', 'directed', 'Interstellar')
# Our sentence was an active sentence.  Let's make the sentence passive, and
# then try out our function again
text = ("The sci-fi film Interstellar was directed by the talented director " +
        "Christopher Nolan.")

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

# Let's reset the sentence root dictionary and store the new roots
sentence_root_dictionary = {}

for sentence in doc.sents:
    sentence_root_dictionary[sentence.text] = sentence.root.text
    
# Let's reset the relational triples list
relational_triples_list = []

# Now call the new function on our new sentence.  In assembling the relational
# triple here, we spin around the object and the subject, because the sentence
# is passive
for sentence in doc.sents:
    obj, subj = subject_object_extractor_v2(sentence)
    
    relational_triples_list.append((obj,sentence.root.text,subj))
    
print (relational_triples_list)

# It seems that our function doesn't quite work for the passsive version of
# the sentence - we get the relational triple 
# ('director', 'directed', 'Interstellar').  It's not far off - the second
# and third elements are perfect, but we get 'director' instead of 
# 'Christopher Nolan' for the first element (which is the object here).  If
# we look at our dependency tree (or the print out of the dataframe) we can
# see what the problem is - the token with the Object of Preposition ('pobj')
# dependency tag is 'director', and is a noun, and then after this comes the
# name Christopher Nolan.  Let's write a new function that deals with this.
# We'll also pass out the indicator as to whether the sentence is passive so
# we can order our Relational Triple the correct way for any given sentence.
def subject_object_extractor_v3(sentence):
    # We'll store the text, pos and dependency tags together in a Pandas
    # Dataframe to make it easier to access the tokens before and after the
    # token we're looking at
    token_text_list = [tok.text for tok in sentence]
    token_pos_list = [tok.pos_ for tok in sentence]
    token_dep_list = [tok.dep_ for tok in sentence]

    token_df = pd.DataFrame()
    
    token_df['token_text'] = token_text_list
    token_df['token_pos'] = token_pos_list
    token_df['token_dep'] = token_dep_list
    
    # Let's print the dataframe
    print (token_df)
    
    # Let's check if the sentence is passive
    subjpass = False
    
    for i in range(len(token_df)):
        if token_df.loc[i]['token_dep'].find("subjpass") == True:
            subjpass = True
            
    candidate_subject = ''
    candidate_object = ''
                
    # if sentence is active
    if subjpass == False:
        for i in range(len(token_df)):
            # if the current token has a direct object dependency tag
            if token_df.loc[i]['token_dep'] == "dobj":
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the object as being both of these tokens
                    # together
                    if (i-1 >= 0 and 
                        token_df.loc[i-1]['token_dep'] == "compound"):
                        candidate_object = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the object
                    else:
                        candidate_object = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate object.  If not, 
                # just take this token as the object.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate object
                    if (i+1) == len(token_df):
                        candidate_object = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_object = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_object = (
                                token_df.loc[i]['token_text']
                            )
                            
            # if the current token's dependency indicates it is a subject
            if token_df.loc[i]['token_dep'].endswith("subj") == True:
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the subject as being both of these tokens
                    # together
                    if (i-1 >= 0 and 
                        token_df.loc[i-1]['token_dep'] == "compound"):
                        candidate_subject = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the subject
                    else:
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate subject.  If not, 
                # just take this token as the subject.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate subject
                    if (i+1) == len(token_df):
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_subject = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_subject = (
                                token_df.loc[i]['token_text']
                            )
                
    # if sentence is passive
    else:
        for i in range(len(token_df)):
            # if the current token has an Object of Prepostion depedency tag
            if token_df.loc[i]['token_dep'] == "pobj":
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the object as being both of these tokens
                    # together
                    if (i-1 >= 0 and
                        token_df.loc[i-1]['token_dep'] == "compound"):
                        candidate_object = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the object
                    else:
                        candidate_object = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, check if it is a noun
                elif token_df.loc[i]['token_pos'] == "NOUN":
                    # check if the next token is both a proper noun and a
                    # compound (which would indicate that this is the name of
                    # the noun we found)
                    if (i+1 < len(token_df) and 
                        token_df.loc[i+1]['token_pos'] == "PROPN" and
                        token_df.loc[i+1]['token_dep'] == "compound"):
                        # Check if the next token after this (so two tokens
                        # ahead of the original token) is also a proper noun -
                        # this would indicate that this is likely part of the
                        # name in the token at i+1.  If it is, use both proper
                        # nouns together (with a separating space) as the
                        # candidate object
                        if (i+2 < len(token_df) and
                            token_df.loc[i+2]['token_pos'] == "PROPN"):
                            candidate_object = (
                                token_df.loc[i+1]['token_text'] + " " +
                                token_df.loc[i+2]['token_text']
                                )
                        # if the token at i+2 isn't a proper noun, but the one
                        # at i+1 is, then just use the one at i+1
                        else:
                            candidate_object = (
                                token_df.loc[i+1]['token_text']
                                )
                    # if it's a noun, but the above doesn't apply, then check 
                    # if the token after it is an Appositional Modifier - if it
                    # is, then use the Appositional Modifier as the candidate 
                    # object.  If not, just take this token as the object.
                    else:
                        # Check to make sure there is another token after this 
                        # one first
                        # If there isn't (ie i+1 == length of token_df) then 
                        # just use the current token as the candidate object
                        if (i+1) == len(token_df):
                            candidate_object = (
                                token_df.loc[i]['token_text']
                            )
                        else:
                            if token_df.loc[i+1]['token_dep'] == "appos":
                                candidate_object = (
                                    token_df.loc[i+1]['token_text']
                                )
                            else:
                                candidate_object = (
                                    token_df.loc[i]['token_text']
                                )
                            
            # if the current token's dependency indicates it is passive
            # subject
            if token_df.loc[i]['token_dep'].find("subjpass") == True:
                # if it's also a proper noun
                if token_df.loc[i]['token_pos'] == "PROPN":
                    # check if the token before is a compound, and if it is,
                    # then take the subject as being both of these tokens
                    # together
                    if (i-1 >= 0 and
                        token_df.loc[i-1]['token_dep'] == "compound"):
                        candidate_subject = (
                            token_df.loc[i-1]['token_text'] + " " +
                            token_df.loc[i]['token_text']
                            )
                    # if the token before isn't a compound, just take this
                    # token as the subject
                    else:
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                            )
                # if it's not a proper noun, then check if the token after it
                # is an Appositional Modifier - if it is, then use the 
                # Appositional Modifier as the candidate subject.  If not, 
                # just take this token as the subject.
                else:
                    # Check to make sure there is another token after this one
                    # first
                    # If there isn't (ie i+1 == length of token_df) then just
                    # use the current token as the candidate subject
                    if (i+1) == len(token_df):
                        candidate_subject = (
                            token_df.loc[i]['token_text']
                        )
                    else:
                        if token_df.loc[i+1]['token_dep'] == "appos":
                            candidate_subject = (
                                token_df.loc[i+1]['token_text']
                            )
                        else:
                            candidate_subject = (
                                token_df.loc[i]['token_text']
                            )
            
    return candidate_object, candidate_subject, subjpass

# Let's reset the relational triples list
relational_triples_list = []

# Now call the new function on our sentence.  We can use the boolean storing
# whether the sentence is passive to determine the way we assemble the
# Relational Triple.
for sentence in doc.sents:
    obj, subj, passive = subject_object_extractor_v3(sentence)
    
    if passive == True:
        relational_triples_list.append((obj,sentence.root.text,subj))
    else:
        relational_triples_list.append((subj,sentence.root.text,obj))
    
print (relational_triples_list)

# Hooray!  We've managed to get the extraction from the passive sentence
# working too, and got our desired Relational Triple of
# ('Christopher Nolan','directed','Interstellar')
# Now, for completeness, let's try our new function on both the active and
# passive versions of the sentence at the same time to make sure we haven't
# broken any logic

# Set up a new text with both sentences
text_1 = ("Talented director Christopher Nolan directed the sci-fi film " +
          "Interstellar.")
text_2 = ("The sci-fi film Interstellar was directed by the talented " +
          "director Christopher Nolan")
#text_1 = ("Man repeatedly stabbed victim at home")
#text_2 = ("Father visited victim in evening")

# Apply the loaded SpaCy model to the texts
doc_1 = nlp(text_1)
doc_2 = nlp(text_2)

# Store the sentences in a list
list_of_sentences = []

for sentence in doc_1.sents:
    list_of_sentences.append(sentence)
    
for sentence in doc_2.sents:
    list_of_sentences.append(sentence)
    
# Let's reset the relational triples list
relational_triples_list = []

# Now call the new function on each sentence in our new text and assemble the
# Relational Triples.
for sentence in list_of_sentences:
    obj, subj, passive = subject_object_extractor_v3(sentence)
    
    if passive == True:
        relational_triples_list.append((obj,sentence.root.text,subj))
        print (sentence.text + " (PASSIVE)")
    else:
        relational_triples_list.append((subj,sentence.root.text,obj))
        print (sentence.text + " (ACTIVE)")
    
print ("Relational Triples List : ")
print (relational_triples_list)

# It works! In case you're wondering, I've split the above sentences into 2
# docs and applied the SpaCy model to them separately.  To see why, uncomment
# the following block of code.  You'll see that, because both sentences are
# in the same document, SpaCy will parse the sentences slightly differently,
# because it's considering information from both sentences.  Specifically,
# you'll see that it parses "film" as the root of the second sentence, rather
# "directed".  So you'd need to think about more clever rules if you're
# parsing a multi-sentence block of text.  And indeed, you will need to
# consider rules beyond what we've look at in this code anyway.  You'd also
# likely want to think about building separate functions that do some of the
# checks for certain pos-tags and dependency-tags rather than repeat code,
# particularly if you're building this up.  But hopefully it's given you a bit 
# of an introduction to rules-based extraction of Relational Triples! Also,
# try using the commented out text_1 and text_2 above to see some examples
# of this code working on other sentences.
"""text = ("Talented director Christopher Nolan directed the sci-fi film " +
        "Interstellar. The sci-fi film Interstellar was directed by the " +
        "talented director Christopher Nolan.")

doc = nlp(text)

relational_triples_list = []

for sentence in doc.sents:
    obj, subj, passive = subject_object_extractor_v3(sentence)
    
    if passive == True:
        relational_triples_list.append((obj,sentence.root.text,subj))
    else:
        relational_triples_list.append((subj,sentence.root.text,obj))

print ("Relational Triples List : ")    
print (relational_triples_list)
"""

"""
# Remember : WE CAN USE spacy.explain('x') where x is a dependency tag or a 
# POS tag and it'll tell you what it means

# See https://webapps.towson.edu/ows/nouns.htm for explanation of direct
# object vs object of preposition

"""
