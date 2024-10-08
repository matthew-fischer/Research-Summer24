import sys
from helpers import read_me, build_seqs
from nbinomSemiMarkov import create_series, print_series
from scipy.stats import binom

def success_failure_prob(max_per_state, series):
    switch_probability = []
    for state in range(len(series)):
        total = 0
        for index in series[state]:
            if (max_per_state[state] == 0):
                continue
            else:
                total += index / max_per_state[state]
        if (len(series) == 0):
            switch_probability.append(0)
        else:
            total = total / len(series)
            switch_probability.append(total)
    return switch_probability

def findingN(series):
    # This function is determining the values of N for each state. 
    # It sums the amount of time spent in each state based on the patient.
    max_per_state = []
    for state in series:
        total = 0
        for i in state:
            total += i
        max_per_state.append(total)
    return max_per_state

def binomRVS(current_state, switch_prob, max_num):
    sim = binom.rvs(max_num, switch_prob[current_state - 1])
    return sim

def sim_binomRVS(x_seq, switch_prob, max_num):
    simulated = []
    for i in range(len(x_seq)):
        simulated.append(binomRVS(x_seq[i], switch_prob, max_num[x_seq[i] - 1]))
    return simulated

def binomPMF(x_seq, t_seq, switch_prob, max_num):
    simulated = []
    for i in range(len(x_seq)):
        simulated.append(binom.pmf(t_seq[i] - 1, max_num, switch_prob[x_seq[i] - 1]))
    return simulated

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)
    
    seq = build_seqs(states)
    x_seq = seq[0]
    t_seq = seq[1]

    series = create_series(x_seq, t_seq)
    print_series(series)

    max_per_state = findingN(series)
    print(f"N value per state: {max_per_state}.")

    switch_probability = success_failure_prob(max_per_state, series)
    print(f"\nThe Switch Probabilities are: {switch_probability}\n")

    sim_binom = sim_binomRVS(x_seq, switch_probability, max_per_state)
    print(sim_binom)

if __name__ == "__main__":
    main()