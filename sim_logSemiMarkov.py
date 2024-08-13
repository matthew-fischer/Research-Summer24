import sys, numpy as np
from helpers import read_me, build_seqs
from geoSemiMarkov import transition_matrix
from nbinomSemiMarkov import create_series
from logSemiMarkov import failure, avg_series, prob
from sim_geoSemiMarkov import plotting

def simulation(matrix, switch_probabilities, length, SIZE):
    sleep_states = []
    current_state = 1  # Starting state is 1
    while (len(sleep_states) < length):
        sleep_states.append(current_state)
        remain = failure(switch_probabilities[current_state - 1], SIZE)  # This determines how many times we stay in the current state. (Following a Logarthmic Distribution).
        for i in range(remain[0]):
            if (len(sleep_states) < length):
                sleep_states.append(current_state)
        switch_prob = matrix[current_state - 1]
        current_state = np.random.choice([1,2,3,4,5], p=switch_prob)
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

    series = create_series(x_seq, t_seq)
    avgSeries = avg_series(series)
    switch_prob = prob(avgSeries)

    semi_markov_matrix = transition_matrix(x_seq)
    TRIAL_SIZE = 1

    sim_states = simulation(semi_markov_matrix, switch_prob, len(states), TRIAL_SIZE)

    sim_matrix = transition_matrix(sim_states)
    print("Transition matrix using simulated sleep states:")
    for row in sim_matrix:
        print(row)
    print("\n")
    matrix = transition_matrix(states)
    print("Transition matrix using sleep states from patient:")
    for row in matrix:
        print(row)
    print("\n")

    plotting(sim_states, len(sim_states), "Semi Markov Model following a Logarithmic Distribution")

    return

if __name__ == "__main__":
    main()