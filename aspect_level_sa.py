#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:08:17 2020

@author: dan
"""

# See https://www.tensorflow.org/tutorials/keras/text_classification

# To run this, you need to first install tensorflow :
# pip install tensorflow
# pip install tensorflow-hub
# pip install tensorflow-datasets
# It is recommended that you create a new Anaconda environment and install
# tensorflow into this new environments.  For more on creating and switching
# environments watch this video :
# https://tinyurl.com/y22k5ntn

# You also need to download the Large Movie Review Dataset v1.0 here :
# https://ai.stanford.edu/%7Eamaas/data/sentiment/

import re # library for regular expression functions
import string # library for string functions
import csv

# Import tensorflow and elements of keras (the API to access tensorflow) that
# we need
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import preprocessing
from tensorflow.keras.layers.experimental.preprocessing\
    import TextVectorization
from tensorflow.keras.callbacks import EarlyStopping

# Imports for Aspect-Level Sentiment Analysis
import spacy
import en_core_web_sm
from nltk.tokenize import sent_tokenize

# When we push our data through the neural network, we don't want to push
# everything through at once, as it leads to over-fitting (where the NN gets
# really good at predicting the training examples, but really bad at
# generalising to anything else).  A good initial batch size is 32.
batch_size = 32

# We use a random number seed so we get the same results each time, 
# for testing purposes (the random number generators you typically use on a 
# computer are not truly random but pseudo-random.  
# Using a seed allows us to fix it so the same 'random' numbers come out each 
# time.  This is useful when testing code or we're learning how to do 
# something.  It's also essential when we're using a validation split and
# shuffling the data, as we are here, to ensure there is no overlap between
# the training and validation sets)
seed = 42

# To run this program, you need to have the aclImdb folder in the same
# directory.  This contains the Large Movie Review Dataset that contains
# 50,000 reviews from IMDB, which are split into 25,000 training examples and
# 25,000 test examples.  The data is split into sub-folders 'test' and 'train'
# and within each of these are sub-folders 'pos' and 'neg' containing
# individual text files for each review, with the 'pos' folder containing
# positive reviews, and the 'neg' folder containing negative ones.  We use
# the text_dataset_from_directory utility which allows us to easily load in
# different classes of examples (e.g. "positive" and "negative") as long as
# we have sub-folders for each classification, and individual text files for
# each example within these sub-folders.
# It's best to split our data into three sets - training, validation
# and test.  The training set is the data used to fit the model, the validation
# set is used during training so it can check to see how well its doing and
# fine tune itself to improve, and the testing set is new data not seen during
# training but which has the "answers" like the training and validation sets,
# so the trained model can see how well it generalises to new data.
# The IMDB set is split only into training and test sets.  So let's
# first create a training set from 80% of the training data (so we can save
# back 20% as a validation set).  We'll split it into batches (the size of 
# which we've defined above), and provide the random seed we specified above.
raw_train_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'aclImdb/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

# We can print the class names that have been assigned to each label.  You'll
# see that label 0 has been allocated to neg (the neg folder, containing
# negative examples) and label 1 to pos.
print ("Label 0 corresponds to ", raw_train_ds.class_names[0], sep="")
print ("Label 1 corresponds to ", raw_train_ds.class_names[1], sep="")

# Now let's setup our validation set.  Remember, this is the 20% of the
# training set we carved off above.
raw_val_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'aclImdb/train',
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)

# Now let's setup our test set.  We'll just use the test set as-is in the data
# (we don't need to split this up like we did with the training data)
raw_test_ds = tf.keras.preprocessing.text_dataset_from_directory(
    'aclImdb/test',
    batch_size=batch_size)

# Before we can push the data through a neural network, it needs to be
# 'standardized'.  This typically means that we need to remove punctuation,
# convert everything to lower case etc.  In the case of the IMDB data, as 
# these are reviews posted on the web, we also need to get rid of the HTML 
# elements that are in the raw text.
# Therefore, here we set up a function to do this for us.  When called, and
# passed some input data, the function will convert everything to lowercase,
# and then use a regular expression to strip out HTML elements.  It will then
# return the stripped version, with punctuation also stripped out just as it's
# being returned.
def custom_standardization(input_data):
    # convert everything to lowercase
    lowercase = tf.strings.lower(input_data)
    
    # replace html tages in the lowercase data with spaces
    stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
    
    # remove punctuation from the lower-case html-stripped text, and then
    # return it
    return tf.strings.regex_replace(stripped_html,
                                    '[%s]' % re.escape(string.punctuation),
                                    '')

# Next we'll set up a TextVectorization layer ready for when we build our
# neural network.  Vectorization here means converting text into numbers
# as neural networks (and computers generally) have to deal fundamentally with
# numbers, not text.  In our TextVectorization layer, we'll do this, and we'll
# also call the custom_standardization function we declared above to get
# our text prepared before it's turned into numbers.  We store in max_features
# the maximum number of tokens (words) that we want (10,000 will limit us to
# the 10,000 most common.  We don't want to include lots of words that are
# rarely used, as they're not going to help us learn sentiment as there are
# so few examples, and it'll slow down our learning).  We store in
# sequence_length the maximum length of review we want to pass through the
# neural network (250 words (tokens) here).  Everything passed
# through the neural network must be the same length, so anything longer than
# 250 words is truncated (so words beyond that are chopped) and any reviews
# shorter than 250 words are padded out to the required length with a special
# padding value that the neural network ignores for training.  output_mode
# specifies how our text is transformed into numbers - 'int' turns each token
# into an integer.
max_features = 10000
sequence_length = 250

vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Here's where we specify HOW we will map our text into numbers (integers in
# our case, as we specified above when setting up the vectorize_layer).  We
# first extract just the review text (ie not the labels as well) to make a 
# text-only dataset.  We do this by defining and using a 'lambda' function.  
# These are just mini-functions in Python that are anonymous (they don't have
# a name) and are just defined and executed immediately (think of them as
# mini quick disposable functions).  Here our function takes 2 inputs (x and 
# y - x being the review text, and y being the labels) and returns just x.
# Once we've got just the text stored in train_text, we then call the adapt
# method on the preprocessing vectorize_layer we setup above - this creates the
# integers we need from the indices of the strings in the text.  Once this is
# done, each integer will relate to a string of text in our reviews (within
# the top 10,000 words)
train_text = raw_train_ds.map(lambda x, y:x)
vectorize_layer.adapt(train_text)

# Let's create a function that applies the vectorize_layer to preprocess data
# expand_dims reshapes the tensor so it can be applied to the vectorize_layer.
# Don't worry about the details of this for the moment.
def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

# Now we've adapted the preprocessing layer (vectorize_layer) to deal with
# integer representations of our text strings, we'll now apply the layer
# to the training, validation and test data sets we created earlier, and
# store them in new variables (so we can still access the raw unprocessed data
# if needed).  This makes sure that all the datasets are prepared in the 
# format needed to be used in the neural network.  We'll use the 
# vectorize_text function we defined above to do this for us.
train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

# Now let's build the Neural Network - the model.  
# We build the Neural Network by stacking 'layers' of nodes and their
# connections.  We need to consider :
# 1. how to represent the text
# 2. how many layers to use in the model
# 3. how many hidden units for each layer (hidden layers are those in the
# middle that aren't input and output layers; they're doing all the magic!)
# One way to represent text is to convert our reviews into "embedding vectors"
# using an Embedding Layer.  This essentially turns discrete data (e.g. words)
# into continuous data (a bit like distributions).

# We assemble the model by building it up layer by layer.  We use a Sequential 
# model here - a linear stack of layers where each layer has exactly one input 
# tensor and one output tensor.  A tensor is like a multi-dimensional matrix, 
# within which we stuff all of our inputs to feed them through the network.
# 
# The first layer is an embedding layer.  An embedding layer basically
# transforms the numbers we want to feed through our network (which represent
# words here, converted to numbers above) into tensors that can be pushed
# through the network.  Here, we use an untrained embedding layer that will
# learn as the model trains.  However, we can also use a pre-trained
# embedding layer such as "https://tfhub.dev/google/nnlm-en-dim50/2" which
# has been trained on common words.  The advantage of doing that is we can
# use transfer learning where, rather than learn from scratch, we get all the
# training for common stuff from a pre-trained example, and then just build
# up from there, so we just learn stuff that's more specific to our problem.
# To use this in this code, we could use the following code :
# embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
# hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string,
#                            trainable=True)
# and then replace the embedding layer in the model declaration below with
# hub_layer
# 
# Next we have a dropout layer, which randomly sets a % of input units to 0
# at each step during training.  We do this to prevent over-fitting, where
# the model essentially learns how to predict the training data brilliantly,
# but is poor at predicting anything else, because it's picked up too much
# that is specific to the training data.  Here the dropout layer drops 20% of
# input units at each training step.
# 
# Next we have a GlobalAveragePooling1D layer which, in basic terms, squashes
# down the tensor by removing dimensions (it does this by taking pooled
# averages, to reduce the amount of data represented).  They are increasingly
# used as a means of preventing overfitting (less data = less potential to
# overfit).
# 
# Next we have another dropout layer, identical to the second layer.
# 
# Finally, we have a densely connected layer (all nodes from the previous layer
# connect into it) as our output layer, which has a single output node.
# 
# We specify an embedding dimension of 16 for the network, which means that
# all of the layers (other than the final layer) will have 16 hidden units.
embedding_dim = 16

model = tf.keras.Sequential([
    layers.Embedding(max_features+1, embedding_dim),
    layers.Dropout(0.2),
    layers.GlobalAveragePooling1D(),
    layers.Dropout(0.2),
    layers.Dense(1)])

# Let's print a summary of the model (the neural network) so we can see how
# it's structured
print (model.summary())

# Now let's compile the model.  We need to specify an optimizer, a loss
# function, and the metrics to assess performance.
# An Optimizer is an algorithm that changes the values of the Neural Network
# (such as weights and learning rate) to reduce losses over time.  Adam is one
# of the most commonly used Optimizers.
# A loss function calculates the difference between the model's prediction
# and the correct answer.  Here we use a Binary Crossentropy loss function
# because we're dealing with a binary classification problem (two 
# classifications - positive or negative), and Binary Crossentropy is good
# at dealing with probabilities, as it measures the distance between
# probability distributions - here, that's the distance between the "correct"
# classification and the prediction.  from_logits=True just means normalise
# the outputs so they're between 0 and 1 (rather than +/- infinity).
# Metrics determine how we measure success.  Here, we use Accuracy as our
# metric, which determines the number of predictions the machine got correct
# out of the total number of predictions.
model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Now we'll train the model.  When we ran this before (in sa_with_own_data.py)
# we saw that, whilst loss decreased and accuracy increased in each new epoch,
# validation loss and accuracy seemed to peak early and not improve much.
# This indicates overfitting - where the model has learned things that are
# too specific to the training data, and loses its ability to generalise.
# One way to combat this is to stop training before this happens.  We could
# just manually reduce the epochs to try to cut off before the point when 
# validation accuracy is no longer increasing.  But a better way is to use an
# EarlyStopping callback, which monitors a given metric, and will
# automatically terminate the training when that metric no longer seems to be
# improving.
# Here, we set up the EarlyStopping callback and ask it to monitor the
# validation accuracy.  We specify a min_delta, which is the minimum amount
# accuracy must improve, and if it doesn't improve by at least this amount
# then the training is terminated.  patience represents the number of epochs
# to wait until training is stopped, so a patience value of 1 would terminate
# the training after 1 epoch of no improvement.  Don't forget to import
# EarlyStopping from tensorflow.keras.callbacks at the start of the code too.
earlystop_callback = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0.01,
    patience=1)

# Once we've set up the EarlyStopping callback we can proceed as before,
# except we need to add it as a callback when we call the function to fit the
# model
epochs = 10

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[earlystop_callback],
    verbose=1)

# Now let's evaluate the model on the test dataset (which it hasn't seen yet).
# This will give us an indication of how well it generalises.
loss, accuracy = model.evaluate(test_ds)
print ("EVALUATION ON TEST DATASET")
print ("Loss : ", loss, sep="")
print ("Accuracy : ", accuracy, sep="")

# If we want the model to be able to process new raw strings of text (rather
# than having to vectorize them using the vectorize_layer first to convert
# them to numbers), we can export a version of our model by creating a new
# model using the weights we've just trained, and which includes the text
# vectorization layer.  We'll add a sigmoid activation function as an
# additional layer at the end.  An activiation function transforms the summed
# weighted input into a node into the output (or "activation") of that node.
# The sigmoid activation function will return a floating point number
# between 0 and 1 which will represent the probability / confidence that the
# output is 0 (negative review) or 1 (positive review).  The closer it is to
# these values, the higher the confidence.  We can then apply a threshold to
# determine when we declare it one or the other.
# So, the new model is a vectorization layer, followed by all the layers of
# the trained model (complete with the weights following training), and a
# sigmoid output layer.
export_model = tf.keras.Sequential([
    vectorize_layer,
    model,
    layers.Activation('sigmoid')])

# Now let's compile our new model.  We use from_logits=False here because
# the sigmoid activation function will normalise the outputs to between 0 and
# 1 anyway
export_model.compile(
    optimizer='adam',
    loss=losses.BinaryCrossentropy(from_logits=False),
    metrics=['accuracy'])

# EXERCISE 1 SOLUTION
# Let's read in some new reviews from csv
list_of_new_reviews = []

with open("ex_1_reviews.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    
    for row in reader:
        list_of_new_reviews.append(row[0])
        
for review in list_of_new_reviews:
    predicted_sentiment = export_model.predict([review])
    
    print ("REVIEW : ")
    print (review)
    print ("PREDICTED SENTIMENT : ")
    
    if predicted_sentiment[0] < 0.25:
        print ("Confident NEGATIVE : ", predicted_sentiment[0], sep="")
    elif predicted_sentiment[0] < 0.5:
        print ("Possible NEGATIVE : ", predicted_sentiment[0], sep="")
    elif predicted_sentiment[0] < 0.75:
        print ("Possible POSITIVE : ", predicted_sentiment[0], sep="")
    else:
        print ("Confident POSITIVE : ", predicted_sentiment[0], sep="")
        
# ASPECT-LEVEL SENTIMENT ANALYSIS
# Let's load the pre-trained en_core_web_sm model into SpaCy
nlp = en_core_web_sm.load()

# We'll set up a dictionary to store the noun chunks from each review
dict_noun_chunks = {}

# And we'll have a review index so we can store each list of noun chunks
# against a review number
review_index = 0

# For each review, apply the SpaCy NLP pre-trained model (en_core_web_sm in
# this case).  Then grab each identified noun-chunk found (stored in 
# article.noun_chunks) and add it to our list of noun chunks for this review.
# Once they've all been grabbed, add the list of noun chunks to the dictionary
# against the review number, and increment the review number by 1.
for review in list_of_new_reviews:
    article = nlp(review)
    
    list_of_noun_chunks_in_this_review = []
    
    for chunk in article.noun_chunks:
        list_of_noun_chunks_in_this_review.append(chunk)
        
    dict_noun_chunks[review_index] = list_of_noun_chunks_in_this_review
    
    review_index += 1
    
# Now we'll go through each review, and print out the identified noun-chunks,
# along with the sentence to which each belongs, and predict the sentiment
# of each sentence. We'll use the sent_tokenize method from the Natural 
# Language Toolkit (NLTK) - note we need the import statement 
# "from nltk.tokenize import sent_tokenize" at the top of our code to do this.
# We can then use the sent_tokenize method to split each review into separate 
# sentences, and look for our noun-chunks in each sentence.  Then, we use
# the exported model to make a prediction of the sentiment of that sentence.
review_index = 0

for review in list_of_new_reviews:
    print (f"Review {review_index} identified noun-chunks : ")
    
    list_of_sentences_in_this_review = sent_tokenize(review)
    
    for sentence in list_of_sentences_in_this_review:
        for chunk in dict_noun_chunks[review_index]:
            if str(chunk) in sentence:
                print (f"{str(chunk)} : {sentence}")
                
                predicted_sentiment = export_model.predict([sentence])
                
                if predicted_sentiment[0] < 0.25:
                    print ("Sentence predicted to be confident NEGATIVE")
                    print (f"Output value : {predicted_sentiment}")
                elif predicted_sentiment[0] < 0.5:
                    print ("Sentence predicted to be possible NEGATIVE")
                    print (f"Output value : {predicted_sentiment}")
                elif predicted_sentiment[0] < 0.75:
                    print ("Sentence predicted to be possible POSITIVE")
                    print (f"Output value : {predicted_sentiment}")
                else:
                    print ("Sentence predicted to be confident POSITIVE")
                    print (f"Output value : {predicted_sentiment}")
                
                print ("-----")
                
    review_index += 1
    
    print ()

# Portions of this code are taken from 
# https://www.tensorflow.org/tutorials/keras/text_classification
# MIT License
#
# Copyright (c) 2017 François Chollet
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

