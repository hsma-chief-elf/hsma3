import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from relearn.bandit_world.Ui_basic_casino import Ui_MainWindow
from relearn.bandit_world.environments import (BernoulliBandit, 
                                               BernoulliCasino, 
                                               standard_bandit_problem,
                                               custom_bandit_problem,
                                               small_bandit_problem)


    
       

#handler for the signal aka slot
def pull_bandit1(self):
    pull_bandit(self, 0)
    complete_round(self)

def pull_bandit2(self):
    pull_bandit(self, 1)
    complete_round(self)

def pull_bandit3(self):
    pull_bandit(self, 2)
    complete_round(self)

def pull_bandit4(self):
    pull_bandit(self, 3)
    complete_round(self)

def pull_bandit5(self):
    pull_bandit(self, 4)
    complete_round(self)
   
def pull_bandit(ui, index):
    pulls = int(ui.tableWidget.item(index, 0).text())
    pulls += 1
    ui.tableWidget.item(index, 0).setText(str(pulls))

def complete_round(ui):
    pulls = int(ui.lbl_pull_count.value())
    pulls += 1
    ui.lbl_pull_count.display(str(pulls))


def init(ui, table):
    for column_index in range(4):
        init_column_to_zero(ui, table, column_index)
    
def init_column_to_zero(ui, table, column_index):
    for i in range(5):
        item = QtWidgets.QTableWidgetItem()
        item.setText("0")
        ui.tableWidget.setItem(i, column_index, item)

def connect_buttons(ui, agent):
    
    #ui.pull_arm1.clicked.connect(ui.pull_bandit1)
    ui.pull_arm1.clicked.connect(agent.pull_bandit1)
    ui.pull_arm2.clicked.connect(agent.pull_bandit2)
    ui.pull_arm3.clicked.connect(agent.pull_bandit3)
    ui.pull_arm4.clicked.connect(agent.pull_bandit4)
    ui.pull_arm4_2.clicked.connect(agent.pull_bandit5)


def experiment():
    '''
    simple example experiment of the MAB
    '''

    app = QtWidgets.QApplication(sys.argv)
    
    #to reproduce the result set a random seed
    np.random.seed(99)

    bandit_arms = custom_bandit_problem(0.2, 0.5, 0.3, 0.75, 0.3)
    
    environment = BernoulliCasino(bandits=bandit_arms)

    agent = HumanCasinoInterface(50, environment, QtWidgets.QMainWindow())
    agent.solve()

    #print_reward(agent)
    #visualise_agent_actions(agent)
    sys.exit(app.exec_())



class HumanCasinoInterface(object):
    def __init__(self, budget, environment, main_window):
        environment.register_observer(self)
        self._main_window = main_window
        self._environment = environment
        self._total_rounds = budget
        self._total_reward = 0
        self._current_round = 0
        self._actions = np.zeros(environment.number_of_arms, np.int32)
        self._means = np.zeros(environment.number_of_arms, np.float64)
        self._arm_wins = np.zeros(environment.number_of_arms, np.int32)
        monkeypatch_ui()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(main_window)
        init(self._ui, self._ui.tableWidget)
        connect_buttons(self._ui, self)

    def __del__(self):
        QtWidgets.qApp.quit()
        

    def _get_total_reward(self):
        return self._total_reward

    def _get_action_history(self):
        return self._actions

    def solve(self):
        self._main_window.show()     

    def pull_bandit1(self):
        self._environment.action(0)
        pull_bandit(self._ui, 0)
        complete_round(self._ui)

    def pull_bandit2(self):
        self._environment.action(1)
        pull_bandit(self._ui, 1)
        complete_round(self._ui)

    def pull_bandit3(self):
        self._environment.action(2)
        pull_bandit(self._ui, 2)
        complete_round(self._ui)

    def pull_bandit4(self):
        self._environment.action(3)
        pull_bandit(self._ui, 3)
        complete_round(self._ui)

    def pull_bandit5(self):
        self._environment.action(4)
        pull_bandit(self._ui, 4)
        complete_round(self._ui)
        
    def pull_bandit(self, index):
        pulls = int(self._ui.tableWidget.item(index, 0).text())
        pulls += 1
        self._ui.tableWidget.item(index, 0).setText(str(pulls))

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
        self._means[arm_index] = self._updated_reward_estimate(arm_index, reward)
        self._arm_wins[arm_index] += reward
        self._ui.tableWidget.item(arm_index, 1).setText(str(self._arm_wins[arm_index]))        
        self._ui.tableWidget.item(arm_index, 2).setText(str(round(self._means[arm_index], 2)))
        self._update_total_reward()

    def _updated_reward_estimate(self, arm_index, reward):
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

    def _update_total_reward(self):
        self._ui.lbl_pull_count_2.display(str(self.total_reward))

    total_reward = property(_get_total_reward)
    actions = property(_get_action_history)




def print_reward(agent):
    print('Total reward: {}'.format(agent.total_reward))
    print(agent._means)


def visualise_agent_actions(agent):
    '''
    Visualise the actions taken in a bar chart

    Keyword arguments:
    -----
    actions -- np.ndarray of the count that each 
               arm was pulled
    
    '''
    actions = agent.actions
    x = [i + 1 for i in range(actions.shape[0])]
    plt.bar(x, actions)
    plt.title('Histogram of Actions Taken by Algorithm')
    plt.xlabel('Arm')
    plt.ylabel('Number of times each arm was selected')
    plt.show()

def monkeypatch_ui():
    #monkey patch the custom functions
    Ui_MainWindow.pull_bandit1 = pull_bandit1
    Ui_MainWindow.pull_bandit2 = pull_bandit2
    Ui_MainWindow.pull_bandit3 = pull_bandit3
    Ui_MainWindow.pull_bandit4 = pull_bandit4
    Ui_MainWindow.pull_bandit5 = pull_bandit5


if __name__ == "__main__":
 
    experiment()
   