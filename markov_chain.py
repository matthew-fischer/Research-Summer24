import sys, numpy as np, matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from helpers import read_me, probabilities, count_matrix, transition_matrix, check_transition_matrix

# GETS COUNTS OF EACH SLEEP STATE
def counts(probabilities, length):
    count = []
    for i in probabilities:
        count.append(round(i * length))
    return count

# IMPLEMENT THE MARKOV CHAIN USING TRANSITION MATRIX
def markov(matrix, length):
    # STARTING STATE IS STATE 1
    state = [1]
    time = [0]
    current_time = 0  # zero since trial hasn't started
    for i in range(0, length - 1):
        current_time += 1
        current_state = state[-1]
        probability = matrix[current_state - 1]  # Since matrix rows are indexed 0-4 not 1-5
        state.append(np.random.choice([1,2,3,4,5], p=probability))
        time.append(current_time)
    # ENDING STATE IS STATE 1
    state.append(1)
    time.append(current_time + 1)

    x_points = np.array(time)
    y_points = np.array(state)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("Markov Model (1st Order Markov Chain)")
    plt.xlabel("Hours Patient has been Asleep", fontdict = font1)
    plt.ylabel("Each Sleep State", fontdict = font1)
    plt.xticks(np.arange(0, 1400, 200))
    custom_yticks = ["Awake", "REM", "NREM1", "NREM2", "NREM3"]
    plt.yticks(np.arange(1,6,1), custom_yticks)
    plt.plot(x_points, y_points, "o-", mfc = "white")

    return state

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    probability = probabilities(states, len(states))
    count = counts(probability, len(states))
    print(count)

    # THIS BLOCK CREATES THE MATRIX AND TRANSITION MATRIX OF SLEEP STATES FROM PATIENT
    matrix = count_matrix(states)
    print("This counts all transitions between sleep states for our patient.")
    for row in matrix:
        print(row)
    print("\n")
    transition = transition_matrix(states)
    print("This is the transition matrix between sleep states for our patient.")
    for row in transition:
        print(row)
    print("\n")

    vector = check_transition_matrix(transition)
    print(f"Checking to make sure transition matrix rows sum to one: {vector}")  # Should print all ones

    # THIS BLOCK MAKES A MARKOV MODEL BASED ON THE SLEEP STATES FROM PATIENT
    model_states = markov(transition, len(states))
    model_matrix = count_matrix(model_states)
    print("Our model counts of transitions between sleep states.")
    for row in model_matrix:
        print(row)
    print("\n")
    model_transition = transition_matrix(model_states)
    print("Our model transition matrix between sleep states. THIS SHOULD BE SIMILAR TO THE TRANSITION MATRIX BASED ON SLEEP STATES OF THE PATIENT.")
    for row in model_transition:
        print(row)
    print("\n")
    
    # THIS BLOCK DISPLAYS THE PLOT OF OUR MARKOV MODEL BASED ON SLEEP STATES FROM PATIENT
    plt.show()
    return

if __name__ == "__main__":
    main()