# Advanced forecasting with Feedforward Neural Networks
# HSMA 2020

-----

**Welcome to the third and final section in our series of HSMA forecasting classes**.  In this 1.5 hour class you will be introduced to forecasting using feedforward neural networks.

## Course structure

1. A lecture introducting the theory of forecasting with Neural Networks
2. Two code-along lectures in Jupyter notebooks 

## Learning outcomes

**By the end of the class you will have**

* New tools to appraise and question forecasting studies
* Hands on experience of manipulating time series in python
* Hands on experience of producing forecasts using Keras and TensorFlow.

## Setup for the course

You are provided with a conda environment (see environment.yml) that you can use to install the dependencies.  To install follow these instructions.

1. Open an anaconda prompt (or terminal on Mac and Linux) in the same directory as the course files.  Run the following command

   * `conda env create -f environment.yml`

2. Conda will resolve the enviornment and ask if you wish to install it.  Answer 'y'. Installation will take several minutes.  It installs an environment called `hsma_forecast3`.  You need to activate it.

   * `conda activate hsma_forecast3`

3. To follow the code along lectures and complete the exercises please use Jupyter-Lab.  To run it enter the following command into your anaconda prompt or terminal (making sure you are in the same directory as the files)

   * `jupyter-lab`

Jupyter will then open.


# Launch Notebooks in Google Colab

If you are experiencing issues with Jupyter-Lab on your personal computer then you can also run the notebooks in google colab.  Use the links below to launch them

## Code along lectures
* Code along 1: Preprocessing data and autoregression basics [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12c_advanced_forecasting/code_along_lectures/01_autoregression.ipynb)

* Code along 2: Forecasting using a feedforward neural network [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12c_advanced_forecasting/code_along_lectures/02_autoregression_keras.ipynb)


