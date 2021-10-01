# Learn-Qazaq
# Architecture
The architecture of our system consists of the environment object, the agent object and the user. The agent is a reinforcement learning algorithm that interacts with the environment. It observes its current state and reward from the environment, and returns an action to perform. For evaluating the quality of performed action we use a popular and efficient RL algorithm called Q-learning. The environment represents an intermediate object which connects agent with user by recording information about user's progress and transmitting it to the agent, as well as receiving an action form the agent and projecting it on interaction with user. 

The environment contains a set of variables that we considered to be useful in the learning process. They include list of letters that student has to learn to write, list of letters that are problematic for student, several sets of words with specific theme, word that student have to write in latin transcription, the time variable measuring the duration of current interaction and overall interaction with user during the episode, gender of user, status of adoption to gender (on/off). 

In order to keep the state-space small only part is shown to the agent as state. Therefore, state information involves only progress indicators such as number of unexplored letters and number of problematic errors, quantised time variable measuring the duration of the recent interaction, as well as other two presumably useful parameters: index of the word set (theme) and gender of the user. These parameters vary in a small range of discrete numbers and form discrete number of states. Yet it can provide comprehensive information needed for decision making since it incorporates knowledge about user's speed of learning that contributes the reward. For example, connecting the time variables with the progress variables might help the agent to make decisions that would speed-up learning if it takes too much time or to slow it down if user goes too fast. Also we suppose that the agent might find connection between the gender of the user and the themes at which the user is more active.

# Interaction
The environment has three methods that are callable from outside: "start episode", "perform given action" and "end episode". All three are called from agent side. 

The "start episode" method selects a random word either from a specific (pre-advice is on) or from a random set and presents it to the user. The letters contained in the word are removed from the list of unexplored letters. After receiving the user's answer the environment records errors and time passed from the beginning of the interaction. The resultant state is returned to the agent.

The agent makes the decisions by selecting actions, but it does not implement a selected action. Instead, it calls the "perform given action" method of the environment. There, in accordance with the given action selection, environments presents a new word to the user and records his errors and time. The obtained data from user interaction is returned as a new state and reward to the agent. The options of actions are: a) keep the given theme and learn words with a letter from errors list, b) keep the theme and learn words with yet unexplored letters, c) change the theme but keep learning words with a letter from errors list, d) change the theme and explore words with yet unexplored letters, e) ask advice from the user. If error list is empty, the actions a) and c) are switched automatically to b) and d) respectively. The agent in such cases is also notified. The instantaneous reward that we give to the agent is determined with the following formula.

![1](https://user-images.githubusercontent.com/78028077/135601079-7e7f89e7-ffb9-4f3a-ab94-a46abb2e2c81.png)

At the end of an episode we provide an additional reward by calculating the number of encountered challenges, unsolved errors and unexplored letters:

![2](https://user-images.githubusercontent.com/78028077/135601295-518fe685-d91e-451c-9e99-48043e13a7d9.png)

After the agent performed 10 actions it calls "end episode" function which counts additional reward that considers the number of unsolved problematic letters and overall time spent on interactions during the episode.


# Modelling the behaviour
To generate an optimal behaviour for increasing the reward we implement our agent with Q-learning algorithm. It computes and stores action-values for each state-action pair that it encountered. The action-values represent the estimated optimality of taking a specific action when the specific state is given. They are computed using the formula below.


![index](https://user-images.githubusercontent.com/78028077/135601517-aa8be68c-ade4-4189-b5af-f49d383e0a57.png)

It can be noticed from the formula that we update the action-value by incrementing/decrementing the old value using two inputs: recently obtained reward and highest action-value of the next state. The reward is received from the environment, while the highest action-value of the next state is stored in the memory of the agent. Therefore, formula 1 implies that action-values hold information that combines the previous optimality of the given state-action pair (old value), its current benefit (reward) and possible future benefit (next state's highest action-value). The hyperparameters such as learning rate and discount factor determine the impact of the above mentioned inputs. 



We modify the action-values update process of Q-learning in accordance to teh specifics of our environment. Since our environment returns an additional reward and we add it to rewards for encountered state-action pairs at the end of an episode, the action-values are also updated at that time. Moreover, we perform the updates in backward order because the action-value of next state for each state-action pair would be relevant for the current episode. Otherwise, the update process will consider values from the previous episode which might be obsolete.

