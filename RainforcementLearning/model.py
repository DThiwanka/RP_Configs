import gym
import numpy as np

env = gym.make('Taxi-v3')

# Initialize Q-table
Q = np.zeros([env.observation_space.n, env.action_space.n])

# Set hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1
num_episodes = 10000

# Run Q-learning algorithm
for i in range(num_episodes):
    state = env.reset()
    done = False
    
    while not done:
        # Choose action using epsilon-greedy policy
        if np.random.uniform() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[state, :])
        
        # Take action and observe next state and reward
        next_state, reward, done, info = env.step(action)
        
        # Update Q-table
        Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))
        
        state = next_state

# Evaluate performance
total_reward = 0
num_episodes = 100

for i in range(num_episodes):
    state = env.reset()
    done = False
    
    while not done:
        action = np.argmax(Q[state, :])
        next_state, reward, done, info = env.step(action)
        total_reward += reward
        state = next_state

print("Average reward over {} episodes: {}".format(num_episodes, total_reward / num_episodes))