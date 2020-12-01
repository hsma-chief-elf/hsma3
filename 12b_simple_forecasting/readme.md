# Simple forecasting with Prophet
# HSMA 2020

-----

**Welcome to the second in our series of HSMA forecasting classes**.  In this 3 hour class you will be introduced to forecasting applied to operational problems in health and social care.  We will make use of the forecasting package Prophet.

## Course structure

1. A lecture introducting the theory of forecasting with Prophet
2. A series of short code-along lectures in Jupyter notebooks
3. A 45 minute practice exercise to give you experience of preprocessing data ready to use in prophet and a how to automatically fit prophet models

## Learning outcomes

**By the end of the class you will have**

* New tools to appraise and question forecasting studies
* Hands on experience of manipulating time series in python
* Hands on experience of producing simple forecasts using Prophet.

## Setup for the course

You are provided with a conda environment (see environment.yml) that you can use to install the dependencies.  To install follow these instructions.

1. Open an anaconda prompt (or terminal on Mac and Linux) in the same directory as the course files.  Run the following command

   * `conda env create -f environment.yml`

2. Conda will resolve the enviornment and ask if you wish to install it.  Answer 'y'. Installation will take several minutes.  It installs an environment called `hsma_forecast`.  You need to activate it.

   * `conda activate hsma_forecast2`

3. To follow the code along lectures and complete the exercises please use Jupyter-Lab.  To run it enter the following command into your anaconda prompt or terminal (making sure you are in the same directory as the files)

   * `jupyter-lab`

Jupyter will then open.


# Launch Notebooks in Google Colab

If you are experiencing issues with Jupyter-Lab on your personal computer then you can also run the notebooks in google colab.  Use the links below to launch them

## Code along lectures
* Code along 1: Preprocessing data to Prophet format [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_1_LIVE.ipynb)

* Code along 2: Using a basic Prophet model for forecasting [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_2_LIVE.ipynb)

* Code along 3: Adding special events to the forecast [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_3_LIVE.ipynb)


## Practical Exercises

* Prophet Exercises: [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/exercises/prophet_exercises.ipynb)

## Solutions to Exercises

> These notebooks provide example solutions to the problems set.  Feel free to work through them.  We all learn in different ways. It is up to you how you choose to learn either by having a go at the exercises or by working through the code provided.  Remember you can always try the code with your own data!  Good luck.

* Code along 1 (with SOLUTIONS): Preprocessing data to Prophet format [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_1_SOLUTIONS.ipynb)

* Code along 2 (with SOLUTIONS): Using a basic Prophet model for forecasting [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_2_SOLUTIONS.ipynb)

* Code along 3 (with SOLUTIONS): Adding special events to the forecast [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/code_along_lectures/code_along_3_SOLUTIONS.ipynb)

* Prophet Exercises (with SOLUTIONS): [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hsma-master/hsma/blob/master/12b_simple_forecasting/exercises/prophet_exercises_SOLUTIONS.ipynb)


