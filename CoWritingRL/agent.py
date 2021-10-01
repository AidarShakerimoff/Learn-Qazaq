import numpy as np
import time
import random
import math 
from collections import defaultdict
from state import State
from env import CoWriting

class QLearningAgent:
  def __init__(self, gender, adapt_to_gender = False):
    self.actions = [0, 1, 2, 3, 4]    # actions: 0 - keep the theme and keep learning the problematic letter
                                      # 1 - keep the theme and explore words with new letters
                                      # 2 - change the theme and keep learning the problematic letter
                                      # 3 - change the theme and explore words with new letters
                                      # 4 - ask advice from adult

    self.qValues = defaultdict(float) # table of action-values (values of state x action pair)
    self.env = CoWriting(gender, adapt_to_gender)      # set the CoWriting environment. Specify the gender of a student and whether it needs to be considered as a pre-advice
 
  def act(self, state, epsilon):
     # this is an implementation of epsilon-greedy policy
    if random.random() < epsilon:
      return random.randint(0, 4)
 
    qValues = [self.qValues.get((state, action), 0) for action in self.actions]
 
    if np.all((qValues == 0)):
      return random.radom(5)
    else:
      return np.argmax(qValues)
 
  def train(self, iterNum = 500, epsilon = 0.2, discount = 0.99, alpha = 0.9):
    self.epsilon = epsilon    # hyperparameter used for epsilon-greedy policy. Indicates the probability of selecting a random action to explore
    self.discount = discount  # hypermarameter used for action-value update. Indicates how much future values are important to be considered
    self.alpha = alpha        # hyperparameter used for action-value update. Indicates how strongly will old values be overritten 
    done = False              # boolean variable indicating whether an episode (10 words) is ended
    # iteration of episodes
    for i in range(iterNum):
      state = self.env.start()
      print("--------------------end of iteration---------------------------")
      gameIter = []           # this is a list where transitions are stored in order to be updated again at the end of an episode
      while True:
        action = self.act(state, self.epsilon)
        next_state, changed_action, changed, reward, done = self.env.step(action)
        if changed:
          self.qValues[(state, action)] = -math.inf
          action = changed_action
          
        gameIter.append((state, action, reward, next_state))    # store the transition
        state = next_state
        print("--------------------end of iteration---------------------------")
        if done:
          print("-----------------------end of episode--------------------------")
          break
      add_reward = self.env.end()
      for (state, action, reward, nextState) in gameIter[::-1]:    
        reward = reward + add_reward
        nextQValues = [self.qValues.get((nextState, nextAction), 0) for nextAction in self.actions]
        nextValue = max(nextQValues)
        self.qValues[(state, action)] = (1 - self.alpha) * self.qValues.get((state, action), 0) \
                                        + self.alpha * (reward + self.discount * nextValue)
      input("Press Enter to continue...")   # to start new episode user have to activate it
