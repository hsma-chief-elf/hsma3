'''
module simulator

Provides:

1. Monte carlo classes and function to test of agents in MAB environments

'''

import numpy as np
import pandas as pd
from sklearn.model_selection import ParameterGrid

class AgentSimulation(object):
    '''
    Encapsulates a Monte-Carlo simulation framework for agents in 
    multi-arm bandit environment

    Agents must implement the interface

    solve()
    reset()
    '''

    def __init__(self, environment, agent, replications=1000):
        self._env = environment
        self._agent = agent
        self._reps = replications

    def simulate(self):

        best_indexes = np.zeros(self._reps, np.int32)

        for rep in range(self._reps):
            self._agent.reset()
            self._agent.solve()
            best_indexes[rep] = self._agent.best_arm

        return best_indexes

class ExperimentResults(object):
    '''
    Results Container for an Agent Experiment
    '''
    def __init__(self, selections, correct_selections, p_correct_selections):
        self.selections = selections
        self.correct_selections = correct_selections
        self.p_correct_selections = p_correct_selections

class Experiment(object):
    '''
    Test the power of a given configuration of an agent
    at correct selection of a max of min 
    '''
    def __init__(self, env, agent, best_index=0, objective='max', replications=1000):
        self._env = env
        self._agent = agent
        self._sim = AgentSimulation(env, agent, replications=replications)
        self._best_index = best_index
        self._objective = objective
        self._reps = replications
    
    def execute(self):
        '''
        Execute the experiment
        '''
        selections = self._sim.simulate()
        
        correct_selections = (selections == self._best_index).sum()
        
        p_correct_selections = correct_selections / self._reps

        return ExperimentResults(selections, correct_selections, p_correct_selections)
    

class GridExperiment(object):

    def __init__(self, agent, environment, param_grid, 
                 best_index=0, replications=1000):
        self._agent = agent
        self._env = environment
        self._param_grid = ParameterGrid(param_grid)
        self._replications = replications
        self._best_index = best_index

    def fit(self):
        
        #create data frame to store results
        num_rows = len(self._param_grid)
        columns = list(self._param_grid[0].keys())
        columns.append('correct_selections')
        columns.append('p_correct_selections')
        
        df_results = pd.DataFrame(index = np.arange(0, num_rows),
                                  columns=columns)
       
        #simulate each of the agent configurations
        for index in range(len(self._param_grid)):
            for key in self._param_grid[index].keys():
                #set the agents attribute
                setattr(self._agent, key, self._param_grid[index][key])

                df_results.loc[index][key] = self._param_grid[index][key]

           
            experiment = Experiment(self._env, 
                                    self._agent, 
                                    best_index=self._best_index,
                                    replications=self._replications)

            results = experiment.execute()

            df_results.loc[index]['correct_selections'] = results.correct_selections
            df_results.loc[index]['p_correct_selections'] = results.p_correct_selections
            
        return df_results
                

            


                
                







