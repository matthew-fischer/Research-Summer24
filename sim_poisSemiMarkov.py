import sys, matplotlib.pyplot as plt, numpy as np
from helpers import read_me, build_seqs, transition_matrix
from poisSemiMarkov import lambda_state
from sim_geoSemiMarkov import plotting

def simulate(matrix, lamdas, length):
    sleep_states = []
    current = 1  # Start state is 1
    while len(sleep_states) < length:
        sleep_states.append(current)
        remain = lamdas[current - 1]
        poisson = np.random.poisson(lam=remain, size=1)
        for i in range(poisson[0]):
            if (len(sleep_states)) < length:
                sleep_states.append(current)

        switch_probabilities = matrix[current - 1]
        current = np.random.choice([1,2,3,4,5], p=switch_probabilities)
    # End state is 1
    sleep_states.append(1)

    return sleep_states

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    seq = build_seqs(states)
    x_seq = seq[0]
    t_seq = seq[1]
    expected = lambda_state(x_seq, t_seq, [1,2,3,4,5])

    print(f"The Lambda states are: {expected}\n")

    semi_markov_matrix = transition_matrix(x_seq)
    sim_states = simulate(semi_markov_matrix, expected, len(states))

    # PRINTING:
    matrix = transition_matrix(states)
    print("TRANSITION MATRIX USING PATIENTS SLEEP STATES")
    for row in matrix:
        print(row)
    print("\n")
    sim_matrix = transition_matrix(sim_states)
    print("TRANSITION MATRIX FOR SIMULATED SEMI MARKOV MODEL USING POISSON DISTRIBUTION:")
    for row in sim_matrix:
        print(row)
    print("\n")    

    # PLOTTING THE SIMULATED SLEEP STATES:
    plotting(sim_states, len(sim_states), "Semi Markov Model following Poisson Distribution")

if __name__ == "__main__":
    main()