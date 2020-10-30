# An introduction to forecasting
# HSMA 2020

-----

**Welcome to the HSMA forecasting class**.  In this 3 hour class you will be introduced to forecasting applied to operational problems in health and social care.

## Course structure

1. A lecture introducting you to the theory and practice of forecasting
2. A series of short code-along lectures in Jupyter notebooks
3. Two short practical exercises to give you experience of visualising time series and producing simple forecasts. 

## Learning outcomes

**By the end of the class you will have**

* New tools to appraise and question forecasting studies
* Hands on experience of manipulating time series in python
* Hands on experience of producing simple benchmark forecasts using the `forecast-tools` python package.

## Setup for the course

You are provided with a conda environment (see binder/environment.yml) that you can use to install the dependencies.  To install follow these instructions.

1. Open an anaconda prompt (or terminal on Mac and Linux) in the same directory as the course files.  Run the following command

   * `conda env create -f environment.yml`

2. Conda will resolve the enviornment and ask if you wish to install it.  Answer 'y'. Installation will take several minutes.  It installs an environment called `hsma_forecast`.  You need to activate it.

   * `conda activate hsma_forecast`

3. To follow the code along lectures and complete the exercises please use Jupyter-Lab.  To run it enter the following command into your anaconda prompt or terminal (making sure you are in the same directory as the files)

   * `jupyter-lab`

Jupyter will then open.


# Launch Notebooks in Google Colab

If you are experiencing issues with Jupyter-Lab on your personal computer then you can also run the notebooks in google colab.  Use the links below to launch them

## Code along lectures
* Code along 1: Loading time series using pandas
* Code along 2: Exploring time series [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12_forecasting/code_along_lectures/02_exploring_ts.ipynb)

* Code along 3: Simple forecasting [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12_forecasting/code_along_lectures/03_benchmark_forecasts.ipynb)


## Exercises
* Exercise 1: Exploring time series [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12_forecasting/exercises/Practical_1.ipynb)
* 
* Exercise 2: Simple forecasting [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12_forecasting/exercises/Practical_2.ipynb)


