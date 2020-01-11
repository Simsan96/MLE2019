# coding: utf8
import A5
import sys
import random
import numpy as np

# Game Environment
GAME = A5.BasicGame("MLE Reinforcement Learning Ping Pong")
x_max = GAME.xMax
y_max = GAME.yMax
x_ball_max = GAME.xBallMax
y_ball_max = GAME.yBallMax
paddle_max = GAME.xPaddleMax
max_v = GAME.maxV

PROTOCOL = True

LEARN_RATE = 0.01
DISCOUNT_FACTOR = 0.1
E_GREEDY_PROBABILITY = 0.1

MAX_ACTIONS = 3
REWARD_THRESHOLD = 0.1
MAX_STATES = 13 * 12 * 10 * 2 * 2
MAX_VALUES = [13, 12, 10, 2, 2]

# Setup the Q array
Q = np.zeros(shape=(MAX_STATES, MAX_ACTIONS), dtype=np.float32)


# Initiates the Q collection with random values between 0 and REWARD_THRESHOLD
def init_q_states():
    for i in range(MAX_STATES):
        for j in range(MAX_ACTIONS):
            Q[i][j] = random.uniform(0, REWARD_THRESHOLD)

def next_s():    
    coordinates = (GAME.xBall, GAME.yBall, GAME.xPaddle, GAME.xV + 1, GAME.yV +1)
    state = coordinates[0]
    for i in range(1, len(coordinates)):
        state = state * MAX_VALUES[i] + coordinates[i]
    return state


# Gets an action-index based on e-greedy
def get_action(s):
    if random.uniform(0, 1) < E_GREEDY_PROBABILITY:
        return random.randint(0, 2)
    else:
        return get_best_action(s)


# Returns the best action-index
def get_best_action(s):
    return int(np.argmax(Q[s]))


# Protocols each executed action
def protocol(s, action, reward):
    if reward == 1 or reward == -1:
        print("S:", s, "   Reward:", reward, "   Q:", Q[s][action])
    else:
        print("S:", s)


def run():
    s = next_s()
    while True:
        action = get_action(s)
        # Execute action and obtain reward
        reward = GAME.display(action)
        # Obtain Q(s', a')
        ns = next_s()
        # Q-Learn
        Q[s][action] += LEARN_RATE * (reward + DISCOUNT_FACTOR * Q[ns][get_best_action(ns)] - Q[s][action])
        if PROTOCOL:
            protocol(s, action, reward)
        s = ns


def train(e_count):
    runs = e_count
    s = next_s()

    while runs > 0:
        # Obtain action for Q(s, a) using e-GREEDY
        if random.uniform(0, 1) < E_GREEDY_PROBABILITY:
            action = random.randint(0, 2)
        else:
            action = get_best_action(s)

        # Execute action and obtain reward
        reward = GAME.display(action, True)

        ns = next_s()

        Q[s][action] += LEARN_RATE * (reward + DISCOUNT_FACTOR * Q[ns][get_best_action(ns)] - Q[s][action])

        if PROTOCOL:
            protocol(s, action, reward)

        s = ns

        runs -= 1

    np.save(str(e_count), Q)


# Plays an optimised game
def play(episodes):
    hits = 0
    misses = 0
    cnt = 0
    s = next_s()

    while cnt < episodes:
        action = get_best_action(s)
        reward = GAME.display(action)
        if reward > 0:
            hits += 1
        elif reward < 0:
            misses += 1
        s = next_s()
        cnt += 1
    print("RESULTS:", "Hits:", hits, "  Misses:", misses, "     In", episodes, "episodes.")


'''
GAME MODI:
-----------------------------------------
run -> Runs the game indefinitely, optimises but never saves the resulting Q-Array, good for troubleshooting
       python LearningAgent.py run

train -> Runs the game for a specific number of episodes training the system and saving the resulting Q-Array to file
      python LearningAgent.py train <EPISODES>

play -> Runs the game indefinitely using a previously trained Q-Array
     python LearningAgent.py play <FILENAME> <EPISODES>

-----------------------------------------
'''


# Must be started with ARGS
try:
    called_with = sys.argv[1]
except IndexError:
    sys.exit("Requires argument to specify either run, train or play.")


if called_with == 'run':
    print("Running freely... and indefinitely")
    init_q_states()
    GAME.start()
    run()

elif called_with == 'train':
    try:
        episode_count = int(sys.argv[2])
    except IndexError:
        sys.exit("Training mode must have episode count.")

    print("Training with", str(episode_count), "episodes.")
    init_q_states()
    GAME.start(True)
    train(episode_count)
    print("Training with", str(episode_count), "runs is complete.")
    print("Resulting Q-Array saved as", str(episode_count) + ".npy")

elif called_with == 'play':
    try:
        filename = sys.argv[2]
        episode_count = int(sys.argv[3])
    except IndexError:
        sys.exit("Require the Q-Array filename and the amount of episodes to play.")
    print("Commencing game:", filename, "for", str(episode_count), "episodes.")
    Q = np.load(filename)
    GAME.start()
    play(episode_count)

else:
    sys.exit("Invalid argument " + called_with + " program can either run, train or play")
