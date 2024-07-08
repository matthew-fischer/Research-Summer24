import sys, numpy as np, matplotlib.pyplot as plt
from helpers import read_me, build_seqs, transition_matrix
from binomSemiMarkov import success_failure_prob, findingN, binomRVS
from nbinomSemiMarkov import create_series
from sim_geoSemiMarkov import plotting

def simulation(states, x_seq, t_seq, trans_matrix, length):
    series = create_series(x_seq, t_seq)
    max_per_state = findingN(series)
    switch_probability = success_failure_prob(states, x_seq)
    print(switch_probability)
    
    sleep_states = []
    current_state = 1  # Starting state is 1
    while ((len(sleep_states)) < length):
        sleep_states.append(current_state)
        remain = binomRVS(current_state, switch_probability, max_per_state[current_state - 1])
        print(f"Sleep State is: {current_state} and the length remained in state is {remain}.")
        for i in range(remain):
            if (len(sleep_states)) < length:
                sleep_states.append(current_state)
        switch_probabilities = trans_matrix[current_state - 1]
        current_state = np.random.choice([1,2,3,4,5], p=switch_probabilities)
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

    semi_markov_matrix = transition_matrix(x_seq)
    sim_states = simulation(states, x_seq, t_seq, semi_markov_matrix, len(states))

    sim_matrix = transition_matrix(sim_states)
    print("Transition matrix based on simulated sleep states:")
    for row in sim_matrix:
        print(row)
    print("\n")
    matrix = transition_matrix(states)
    print("Transition matrix based on patients sleep states:")
    for row in matrix:
        print(row)
    print("\n")

    plotting(sim_states, len(sim_states), "Semi Markov Model following Binomial Distribution")

    return

if __name__ == "__main__":
    main()