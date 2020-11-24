#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HSMA Multi-arm bandit code-along

In this python notebook you will learn about 

* The exploration-exploitation dilemma in reinforcement learning
* How multi-arm bandits 'home-in' on the best solution over time.

Notes:
    
    This python file has been setup to run in Spyter using its 'cell' approach
    to execution.  Click your cursor anywhere in a cell (indicated by the 
    dividing lines) and press Shift-Return.

"""

#%%
# Standard Imports

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


#%%

#import multi-arm bandit agents
from relearn.bandit_world.agents import (EpsilonGreedy, 
                                         AnnealingEpsilonGreedy)

#
from relearn.bandit_world.environments import (custom_bandit_problem,
                                               BernoulliCasino)


#%%

# Step 1: Create some bandits

bandit_arms = custom_bandit_problem(0.2, 0.5, 0.3, 0.75, 0.3)

#how many bandit arms to we have?
print(f'No. of bandits: {len(bandit_arms)}')

#%%
# Step 2: pull a bandit arm
chosen_arm = 3

#bandits return either a 0 or 1.
result = bandit_arms[chosen_arm].play()

if result == 1:
    print('you won!')
else:
    print('you lost')

#%%
# Step 3: Create a casino environment for an agent to interact with

environment = BernoulliCasino(bandits=bandit_arms)


#%%
# Step 4: Create an instance of an EpsilonGreedy Agent and solve!

agent = EpsilonGreedy(epsilon=0.2, budget=50, environment=environment)
agent.solve()


#%%

print(f'Total reward: {agent.total_reward}')
print('Action taken:')
print(agent.actions)


#%%

# Let's look at how we would organise our code to that we can run experiments

# First some simple utility functions to help us print out results...

def print_reward(agent):
    '''
    Utility function to print formatted results
    
    Parameters
    ----------
    agent : object
        Multi arm bandit agent.

    Returns
    -------
    None.

    '''
    print(f'Total reward: {agent.total_reward}')
    print('\nFinal Model:\n------')
    for bandit_index in range(len(agent._means)):
        print(f'Bandit {bandit_index + 1}:\t{agent._means[bandit_index]:.2f}')


def visualise_agent_actions(agent):
    '''
    Visualise the actions taken in a bar chart

    Params:
    -----
    agent : object
        Multi arm bandit agent.
    
    '''
    actions = agent.actions
    x = [i + 1 for i in range(actions.shape[0])]
    plt.bar(x, actions)
    plt.title('Histogram of Actions Taken by Algorithm')
    plt.xlabel('Arm')
    plt.ylabel('Number of times each arm was selected')
    plt.show()


#%%

def epsilon_greedy_experiment(epsilon=0.1, budget=1000, random_seed=None):
    '''
    Simple example experiment of the MAB
    
    Params:
    -------
    epsilon: float
       exploration parameter.  percentage of bandit rounds that are random
    
    budget: int
        Total number of rounds the agent will play
        
    random_seed: int
        Parameter to control random sampling to ensure you get a repeated 
        result
        
    Returns:
    -------
        None.
    
    '''
    print('------\nAgent: Epsilon-Greedy')
    
    #to reproduce the result set a random seed
    np.random.seed(seed=random_seed)

    #create environment
    bandit_arms = custom_bandit_problem(0.2, 0.5, 0.3, 0.75, 0.3)
    environment = BernoulliCasino(bandits=bandit_arms)

    #create agent and solve
    agent = EpsilonGreedy(epsilon=0.1, budget=budget, environment=environment)
    agent.solve()
    
    #print out formatted results
    print_reward(agent)
    visualise_agent_actions(agent)

#%%

#run out experiment
epsilon_greedy_experiment(random_seed=42)

#%%
#Let's try a different experiment using an annealing epsilon greedy agent
#This type of agent starts of very exploratative, but gradually starts to 
#exploit more as the budget runs out.

def anneal_experiment(budget=1000, random_seed=None):
    '''
    simple example experiment of the MAB
    using AnnealingEpsilonGreedy
        
    Params:
    -------    
    budget: int
        Total number of rounds the agent will play
        
    random_seed: int
        Parameter to control random sampling to ensure you get a repeated 
        result
        
    Returns:
    -------
        None.
    
    '''
    print('--------\nAgent:\tAnnealing Epsilon-Greedy')
    #to reproduce the result set a random seed
    np.random.seed(seed=random_seed)

    bandit_arms = custom_bandit_problem(0.2, 0.5, 0.3, 0.75, 0.3)

    environment = BernoulliCasino(bandits=bandit_arms)

    agent = AnnealingEpsilonGreedy(budget=budget, environment=environment)
    agent.solve()
    
    print_reward(agent)
    visualise_agent_actions(agent)


#%%

#run an annealing experiment.
anneal_experiment(random_seed=42)

#%%