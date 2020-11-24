'''
Agents that are designed to solve an instance of multi-arm bandit problem

Classes:
--------
EpsilonGreedy --    Epsilon-Greedy tackles the explore-exploit dilemma by acting greedy
                    1 - epsilon of the time and explore epsilon of the time.  

'''
import numpy as np 


class EpsilonGreedy(object):
    '''
    Encapsulates an Epsilon-Greedy based agent for reinforcement learning
    in multu-arm bandit problems.  The agent interacts and learns from  
    an environment consisting of multiple bandit arms

    Epsilon-Greedy tackles the explore-exploit dilemma by acting greedy
    1 - epsilon of the time and explore epsilon of the time.  

    Note: Implements the observer pattern to recieve feedback from the 
    environment

    Public properties:
    -------
    total_reward -- float, the cumulative reward recieved from the environment
    actions -- np.ndarry (vector), a record of the actions (arms) that have been 
               taken by the agent.
            
    Public methods:
    --------
    solve() -- initiates the algorithm for the budget specified
    feedback() -- observer pattern notification method.  This is called by the
                  environment when the result of an action is ready to be reported.

    '''

    def __init__(self, epsilon, budget, environment):
        '''
        Epsilon-Greedy Algorithm constructor method

        Keyword arguments:
        ------
        epsilon -- float, proportion of time to explore the environment.
                   1 - epsilon = the proportion of time to exploit 
                   (make greedy decisions) about the environment

        budget -- int, number of iterations of the algorithm to run

        environment -- object implementing action interface...to add.
        '''
        self._validate_init(epsilon, budget, environment)
        environment.register_observer(self)
        self._env = environment
        self._epsilon = epsilon
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(environment.number_of_arms, np.int32)
        self._means = np.zeros(environment.number_of_arms, np.float64)
        
    def _validate_init(self, epsilon, budget, environment):
        '''
        Validate the arguments passed to the constructor method

        Keyword arguments:
        ------
        epsilon -- float, proportion of time to explore the environment.
                   1 - epsilon = the proportion of time to exploit 
                   (make greedy decisions) about the environment

        budget -- int, number of iterations of the algorithm to run

        environment -- object implementing action interface...to add.
        '''
        self._validate_epsilon(epsilon)
        self._validate_budget(budget)
        
    def _validate_epsilon(self, epsilon):
        if type(epsilon) != float or epsilon < 0.0 or epsilon > 1.0:
            msg = 'epsilon argument must be a float value between 0 and 1'
            raise ValueError(msg)

    def _validate_budget(self, budget):
        if budget < 0:
            msg = 'budget argument must be a int > 0'
            raise ValueError(msg)

    def reset(self):
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(self._env.number_of_arms, np.int32)
        self._means = np.zeros(self._env.number_of_arms, np.float64)

    def _get_epsilon(self):
        return self._epsilon
    
    def _set_epsilon(self, epsilon):
        self._epsilon = epsilon
        
    def _get_budget(self):
        return self._total_rounds
        
    def _set_budget(self, budget):
        self._total_rounds = budget
        
    def _get_total_reward(self):
        return self._total_reward

    def _get_action_history(self):
        return self._actions
    
    def solve(self):
        '''
        Run the epsilon greedy algorithm in the 
        environment to find the best arm 
        '''
        for i in range(self._total_rounds):
            sample = np.random.uniform()
            if sample > self._epsilon:
                self._exploit()  
            else:
                self._explore()
            self._current_round += 1

    def _exploit(self):
        '''
        Exploit the best arm found
        Interacts with environment and 
        performs the best know action
        '''
        best_index = self._best_arm()
        self._env.action(best_index)  
        

    def _best_arm(self):
        '''
        Return the index of the arm 
        with the highest expected value

        Returns:
        ------
        int, Index of the best arm
        '''
        return np.argmax(self._means)

    def _explore(self):
        '''
        Explore the environment.
        Take a random action and learn from it
        '''
        self._env.random_action()  


    def feedback(self, *args, **kwargs):
        '''
        Feedback from the environment
        Recieves a reward and updates understanding
        of an arm

        Keyword arguments:
        ------
        *args -- list of argument
                 0  sender object
                 1. arm index to update
                 2. reward

        *kwards -- dict of keyword arguments:
                   None expected!

        '''
        arm_index = args[1]
        reward = args[2]
        self._total_reward += reward
        self._actions[arm_index] +=1
        self._means[arm_index] = self.updated_reward_estimate(arm_index, reward)

    def updated_reward_estimate(self, arm_index, reward):
        '''
        Calculate the new running average of the arm

        Keyword arguments:
        ------
        arm_index -- int, index of the array to update
        reward -- float, reward recieved from the last action

        Returns:
        ------
        float, the new mean estimate for the selected arm
        '''
        n = self._actions[arm_index]
        current_value = self._means[arm_index]
        new_value = ((n - 1) / float(n)) * current_value + (1 / float(n)) * reward
        return new_value

    total_reward = property(_get_total_reward)
    actions = property(_get_action_history)
    best_arm = property(_best_arm)
    budget = property(_get_budget, _set_budget)
    epsilon = property(_get_epsilon, _set_epsilon)    


class AnnealingEpsilonGreedy(EpsilonGreedy):
    '''
    Encapsulates an Annealing Epsilon-Greedy based agent for reinforcement learning
    in multi-arm bandit problems.  The agent interacts and learns from  
    an environment consisting of multiple bandit arms

    Epsilon-Greedy tackles the explore-exploit dilemma by acting greedy
    1 - epsilon of the time and explore epsilon of the time. 

    A potential drawback of the classical epsilon-greedy algorithm is that
    epsilon is a constant and a hyper-parameter that cannot be known in advance.
    The annealing version of the algorithm starts with a large value of epsilon
    and gradually reduces its value over time.  This means that later experiments
    are more likely to exploit than predict.  

    Note: Implements the observer pattern to recieve feedback from the 
    environment

    Dev notes: Inherits from EpsilonGreedy - this could and probably should be 
    set up by composition.  The downside is that a user has to compose the object
    each time they wish to use it.  This keeps parameterisation lower.  

    Public properties:
    -------
    total_reward -- float, the cumulative reward recieved from the environment
    actions -- np.ndarry (vector), a record of the actions (arms) that have been 
               taken by the agent.
            
    Public methods:
    --------
    solve() -- initiates the algorithm for the budget specified
    feedback() -- observer pattern notification method.  This is called by the
                  environment when the result of an action is ready to be reported.

    '''

    def __init__(self, budget, environment):
        '''
        Constructor method for AnnealingEpsilonGreedy
        '''
        environment.register_observer(self)
        self._env = environment
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(environment.number_of_arms, np.int32)
        self._means = np.zeros(environment.number_of_arms, np.float64)
        self._epsilon = np.inf
        self._anneal_epsilon()

    def _anneal_epsilon(self):
        '''
        Gradual cooling of epsilon so that exploration
        less likely in later rounds of learning
        '''
        t = np.sum(self._actions) + 1
        self._epsilon = 1 / np.log(t + 1e-6)

    def feedback(self, *args, **kwargs):
        '''
        Feedback from the environment
        Recieves a reward and updates understanding
        of an arm.  
        After each learning cycle it 

        Keyword arguments:
        ------
        *args -- list of argument
                 0  sender object
                 1. arm index to update
                 2. reward

        *kwards -- dict of keyword arguments:
                   None expected!

        '''
        arm_index = args[1]
        reward = args[2]
        self._total_reward += reward
        self._actions[arm_index] +=1
        self._means[arm_index] = self.updated_reward_estimate(arm_index, reward)
        self._anneal_epsilon()


class OptimisticInitialValues(EpsilonGreedy):
    '''
    Encapsulates an Optimistic Initial Values and Greedy based agent 
    for reinforcement learning in multi-arm bandit problems.  T
    he agent interacts and learns from  an environment consisting of multiple bandit arms

    Epsilon-Greedy tackles the explore-exploit dilemma by acting greedy
    1 - epsilon of the time and explore epsilon of the time. 

    A potential drawback of the classical epsilon-greedy algorithm is that
    epsilon is a constant and a hyper-parameter that cannot be known in advance.
    The annealing version of the algorithm starts with a large value of epsilon
    and gradually reduces its value over time.  This means that later experiments
    are more likely to exploit than predict.  

    Note: Implements the observer pattern to recieve feedback from the 
    environment

    Dev notes: Inherits from EpsilonGreedy - this could and probably should be 
    set up by composition.  The downside is that a user has to compose the object
    each time they wish to use it.  This keeps parameterisation lower.  

    Public properties:
    -------
    total_reward -- float, the cumulative reward recieved from the environment
    actions -- np.ndarry (vector), a record of the actions (arms) that have been 
               taken by the agent.
            
    Public methods:
    --------
    solve() -- initiates the algorithm for the budget specified
    feedback() -- observer pattern notification method.  This is called by the
                  environment when the result of an action is ready to be reported.

    '''

    def __init__(self, budget, environment, init_value=1.0):
        '''
        Constructor method for AnnealingEpsilonGreedy
        '''
        environment.register_observer(self)
        self._env = environment
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(environment.number_of_arms, np.int32)
        self._means = np.full(environment.number_of_arms, init_value, np.float64)
        
    def solve(self):
        '''
        Run the optimistic init values / greedy algorithm in the 
        environment to find the best arm 
        '''
        for i in range(self._total_rounds):
            self._exploit()
            self._current_round += 1
        



class UpperConfidenceBound(object):

    def __init__(self, budget, environment):
        '''
        Constructor method
        '''
        environment.register_observer(self)
        self._validate_budget(budget)
        self._env = environment
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(environment.number_of_arms, np.int32)
        self._means = np.zeros(environment.number_of_arms, np.float64)
        self._upper_bounds = np.zeros(environment.number_of_arms, np.float64)
    
        
    def _validate_budget(self, budget):
        if budget < 0:
            msg = 'budget argument must be a int > 0'
            raise ValueError(msg)
            
    def reset(self):
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(self._env.number_of_arms, np.int32)
        self._means = np.zeros(self._env.number_of_arms, np.float64)
        self._upper_bounds = np.zeros(self._env.number_of_arms, np.float64)

    def _get_total_reward(self):
        return self._total_reward

    def _get_action_history(self):
        return self._actions
    
    def _get_best_arm(self):
        '''
        Return the index of the arm 
        with the highest expected value

        Returns:
        ------
        int, Index of the best arm
        '''
        return np.argmax(self._means)
    
    def solve(self):
        '''
        Run the epsilon greedy algorithm in the 
        environment to find the best arm 
        '''
        for i in range(self._total_rounds):
            
            max_upper_bound_index = np.argmax(self._upper_bounds)
            self._env.action(max_upper_bound_index)            
            
            self._current_round += 1
    
        
    
    def feedback(self, *args, **kwargs):
        '''
        Feedback from the environment
        Recieves a reward and updates understanding
        of an arm

        Keyword arguments:
        ------
        *args -- list of argument
                 0  sender object
                 1. arm index to update
                 2. reward

        *kwards -- dict of keyword arguments:
                   None expected!

        '''
        arm_index = args[1]
        reward = args[2]
        self._total_reward += reward
        self._actions[arm_index] +=1
        self._means[arm_index] = self.updated_reward_estimate(arm_index, reward)
        
        #first run through divides by zero.  In numpy this operation yields inf.
        #the with np.errstate() call/context avoid warning user of the operation 
        with np.errstate(divide='ignore', invalid='ignore'):
            deltas = np.sqrt(3/2 * (np.log(self._current_round + 1) / self._actions))
        
        self._upper_bounds = self._means + deltas
        

    def updated_reward_estimate(self, arm_index, reward):
        '''
        Calculate the new running average of the arm

        Keyword arguments:
        ------
        arm_index -- int, index of the array to update
        reward -- float, reward recieved from the last action

        Returns:
        ------
        float, the new mean estimate for the selected arm
        '''
        n = self._actions[arm_index]
        current_value = self._means[arm_index]
        new_value = ((n - 1) / float(n)) * current_value + (1 / float(n)) * reward
        return new_value

    total_reward = property(_get_total_reward)
    actions = property(_get_action_history)
    best_arm = property(_get_best_arm)


class ThompsonSamplingBeta(object):
    def __init__(self, budget, environment):
        '''
        Constructor method
        '''
        environment.register_observer(self)
        self._validate_budget(budget)
        self._env = environment
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(self._env.number_of_arms, np.int32)
        self._means = np.zeros(self._env.number_of_arms, np.float64)
        
        self._number_of_rewards_1 = np.zeros(self._env.number_of_arms, np.int32)
        self._number_of_rewards_0 = np.zeros(self._env.number_of_arms, np.int32)

    def _validate_budget(self, budget):
        if budget < 0:
            msg = 'budget argument must be a int > 0'
            raise ValueError(msg)
            
    def reset(self):
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(self._env.number_of_arms, np.int32)
        self._means = np.zeros(self._env.number_of_arms, np.float64)
        self._number_of_rewards_1 = np.zeros(self._env.number_of_arms, np.int32)
        self._number_of_rewards_0 = np.zeros(self._env.number_of_arms, np.int32)

    def _get_total_reward(self):
        return self._total_reward

    def _get_action_history(self):
        return self._actions
    
    def _get_best_arm(self):
        '''
        Return the index of the arm 
        with the highest expected value

        Returns:
        ------
        int, Index of the best arm
        '''
        return np.argmax(self._means)

    def solve(self):
        '''
        Run the Thompson Sampling algorithm in the 
        environment to find the best arm 
        '''
        for i in range(self._total_rounds):
            
            random_betas = np.random.beta(self._number_of_rewards_1 + 1, 
                                          self._number_of_rewards_0 + 1)
            
            max_index = np.argmax(random_betas)

            self._env.action(max_index)            
            
            self._current_round += 1

    def feedback(self, *args, **kwargs):
        '''
        Feedback from the environment
        Recieves a reward and updates understanding
        of an arm

        Keyword arguments:
        ------
        *args -- list of argument
                 0  sender object
                 1. arm index to update
                 2. reward

        *kwards -- dict of keyword arguments:
                   None expected!

        '''
        arm_index = args[1]
        reward = args[2]
        self._total_reward += reward

        if reward == 1:
            self._number_of_rewards_1[arm_index] += 1
        else:
            self._number_of_rewards_0[arm_index] += 1
            
        self._actions[arm_index] +=1
        self._means[arm_index] = self.updated_reward_estimate(arm_index, reward)
        

    def updated_reward_estimate(self, arm_index, reward):
        '''
        Calculate the new running average of the arm

        Keyword arguments:
        ------
        arm_index -- int, index of the array to update
        reward -- float, reward recieved from the last action

        Returns:
        ------
        float, the new mean estimate for the selected arm
        '''
        n = self._actions[arm_index]
        current_value = self._means[arm_index]
        new_value = ((n - 1) / float(n)) * current_value + (1 / float(n)) * reward
        return new_value

    total_reward = property(_get_total_reward)
    actions = property(_get_action_history)
    best_arm = property(_get_best_arm)



    
    def thompson_sampling(self, simulated_data):
        '''
        Thompson Sampling Algorithm for reinforcement learning in the
        online bernouli multi-arm bandit problem
        
        Keyword arguments:
        simulated_data -- the simulated_data to use in the learning
                        problem
        
        Returns:
        ------
        Tuple with 2 items
        0: np.ndarray (vector), ads selected at each round
        1: int, total reward
        '''
        total_rounds = simulated_data.shape[0]
        bandits_n = simulated_data.shape[1]
        
        ads_selected = np.zeros(total_rounds, np.int32)
        
        number_of_rewards_1 = np.zeros(bandits_n, np.int32)
        number_of_rewards_0 = np.zeros(bandits_n, np.int32)
        total_reward = 0

        for round_n in range(total_rounds):
        
            random_betas = np.random.beta(number_of_rewards_1 + 1, 
                                        number_of_rewards_0 + 1)
            
            max_index = np.argmax(random_betas)
            
            ads_selected[round_n] = max_index
            reward = simulated_data.values[round_n, max_index]  
            
            if reward == 1:
                number_of_rewards_1[max_index] += 1
            else:
                number_of_rewards_0[max_index] += 1
            
            total_reward += reward
            
        return ads_selected, total_reward


