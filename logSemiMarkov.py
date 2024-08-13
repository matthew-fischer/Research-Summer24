import sys, math, numpy as np
from helpers import read_me, build_seqs
from nbinomSemiMarkov import create_series, print_series
from scipy.stats import logser
from scipy.special import lambertw

def avg_series(series):
    avg = []
    for i in range(len(series)):
        total_sum = 0
        for j in range(len(series[i])):
            total_sum += series[i][j]
        avg.append(total_sum / len(series[i]))
    return avg

def prob(x_bar):
    # p = (b*x_bar) / (1 + b*x_bar)
    probabilities = []
    for i in range(len(x_bar)):
        value = ((-math.e)**(-1/x_bar[i])) / x_bar[i]
        lambert = lambertw(value, -1)  # THE -1 is for W-1.
        b = (-1/x_bar[i]) - lambert
        p = (b*x_bar[i]) / (1 + (b*x_bar[i]))
        probabilities.append(np.real(p))
    return probabilities

def failure(probability, size):
    sim = logser.rvs(probability, size=size)
    return sim

def log_distribution(t_seq, x_seq, probabilities):
    likelihoods = []
    for i in range(len(t_seq)):
        index = x_seq[i] - 1
        likelihoods.append(logser.logpmf(t_seq[i], probabilities[index]))
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
    avgSeries = avg_series(series)  # THIS IS MY X BAR.

    switch_prob = prob(avgSeries)
    print(switch_prob)

    LENGTH_OF_SIM = 10
    for i in range(len(switch_prob)):
        sim = failure(switch_prob[i], LENGTH_OF_SIM)
        #print(f"State {i + 1} simulated values are: {sim}")
        total = 0
        for j in sim:
            total += j
        #print(f"State {i + 1} average simulated value is {total / len(sim)}.")

    likelihoods = log_distribution(t_seq, x_seq, switch_prob)
    total = 0
    for likelihood in likelihoods:
        total += likelihood
    print(f"The overall logged PMF total is: {total}.")

    return

if __name__ == "__main__":
    main()