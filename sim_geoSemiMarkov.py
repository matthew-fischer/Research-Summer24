import sys, matplotlib.pyplot as plt, numpy as np
from helpers import read_me, build_seqs, count_matrix, transition_matrix
from geoSemiMarkov import transition_totals, switches, geometric_distribution

def remain(results, output, state, length):
    while state and (len(output) < length):
        output.append(state)
        state = np.random.choice([state, 0], p=[1 - results[state - 1], results[state - 1]])

def transition(probabilities):
    choice = np.random.choice([1,2,3,4,5], p=probabilities)
    return choice

def simulate(matrix, results, length):
    # START IN STATE 1
    state = 1
    output = []
    while len(output) < length:
        remain(results, output, state, length)
        if (len(output) >= length):
            continue
        else:
            state = transition(matrix[state - 1])
    # END STATE IS STATE 1
    output.append(1)
    return output

def plotting(sleep_states, length):
    time = []
    for i in range(length):
        time.append(i + 1)

    x_points = np.array(time)
    y_points = np.array(sleep_states)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("Semi Markov Model following Geometric Distribution")
    plt.xlabel("Hours Patient has been Asleep", fontdict = font1)
    plt.ylabel("Each Sleep State", fontdict = font1)
    plt.xticks(np.arange(0, 1400, 200))
    custom_yticks = ["Awake", "REM", "NREM1", "NREM2", "NREM3"]
    plt.yticks(np.arange(1,6,1), custom_yticks)
    plt.plot(x_points, y_points, "o-", mfc = "white")

    plt.show()

    return

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    sequences = build_seqs(states)
    x_seq = sequences[0]
    count_x = count_matrix(x_seq)
    trans_matrix_x = transition_matrix(x_seq)
    totals = transition_totals(states)
    switch = switches(count_x)
    geometric_results = geometric_distribution(totals, switch)


    matrix = transition_matrix(states)
    print("TRANSITION MATRIX USING PATIENTS SLEEP STATES:")
    for row in matrix:
        print(row)
    print("\n")


    # SIMULATED SEMI MARKOV MODEL (SINCE WE USE GEOMETRIC RESULTS, IT IS SIMPLY A MARKOV MODEL)
    results = simulate(trans_matrix_x, geometric_results, len(states))
    sim_matrix = transition_matrix(results)
    print("TRANSITION MATRIX FOR SIMULATED SEMI MARKOV MODEL USING GEOMETRIC RESULTS:")
    for row in sim_matrix:
        print(row)
    print("\n")

    plotting(results, len(results))

if __name__ == "__main__":
    main()