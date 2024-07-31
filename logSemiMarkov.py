import sys
from helpers import read_me, build_seqs
from nbinomSemiMarkov import create_series, print_series
from geoSemiMarkov import transition_totals, count_matrix, switches, geometric_distribution
from scipy.stats import logser

def failure(probability, size):
    sim = logser.rvs(1 - probability, size=size)  # IS IT (1-p) OR IS IT (p)
    return sim

def log_distribution(t_seq, x_seq, probabilities):
    likelihoods = []
    for i in range(len(t_seq)):
        index = x_seq[i] - 1
        likelihoods.append(logser.logpmf(t_seq[i], 1 - probabilities[index]))  # IS IT (1-p) OR IS IT (p)
    return likelihoods

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)
    
    seq = build_seqs(states)
    x_seq = seq[0]
    t_seq = seq[1]

    series = create_series(x_seq, t_seq)
    print_series(series)

    counts = count_matrix(x_seq)
    totals = transition_totals(states)
    switch = switches(counts)
    switch_probabilities = geometric_distribution(totals, switch)

    LENGTH_OF_SIM = 10
    for i in range(len(switch_probabilities)):
        sim = failure(switch_probabilities[i], LENGTH_OF_SIM)
        print(f"State {i + 1} simulated values are: {sim}")
        total = 0
        for j in sim:
            total += j
        print(f"State {i + 1} average simulated value is {total / len(sim)}.")

    likelihoods = log_distribution(t_seq, x_seq, switch_probabilities)
    total = 0
    for likelihood in likelihoods:
        total += likelihood
    print(f"The overall logged PMF total is: {total}.")

    return

if __name__ == "__main__":
    main()