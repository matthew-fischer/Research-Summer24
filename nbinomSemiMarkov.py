import sys, pandas as pd, numpy as np
from helpers import read_me, build_seqs
from poisSemiMarkov import lambda_state
from scipy.stats import nbinom

def create_series(x_seq, t_seq):
    series = [[], [], [], [], []]
    for i in range(len(x_seq)):
        series[x_seq[i] - 1].append(t_seq[i] - 1)  # t_seq[i] - 1 cause the first is given.

    return series

def print_series(series):
    for i in range(len(series)):
        print(f"State {i+1} and remained in state: {series[i]} times.")
        total = 0
        for j in series[i]:
            total += j
        print(f"State {i+1} average stay in state is: {total / len(series[i])} times.")

def get_mean_var(series):
    array = []
    # Distribution can be parameterized in terms of its mean and variance
    for i in range(len(series)):
        values = pd.Series(series[i])
        mean = values.mean()
        var = values.var()
        array.append([mean, var])
    return array

def get_parameters(mean_var_array):
    parameters = []
    for i in range(len(mean_var_array)):
        mean = mean_var_array[i][0]
        var = mean_var_array[i][1]
        p = mean / var
        r = (mean ** 2) / (var - mean)
        parameters.append([r, p])
    return parameters

def failure(x_seq, t_seq, state, paras, amount):
    if ((paras[0] > 0) and (paras[1] < 1)):
        # nbinom.rvs gives the number of failures that occur before achieving n successes.
        sim = nbinom.rvs(paras[0], paras[1], size=amount)
    else:
        # use a poisson distribution here.
        STATE_RANGE = [1,2,3,4,5]
        expected_lambdas = lambda_state(x_seq, t_seq, STATE_RANGE)
        remain = expected_lambdas[state]
        sim = np.random.poisson(lam=remain, size=amount)
    return sim

def prob_mass_func(x_seq, t_seq, paras):
    likelihoods = []
    for i in range(len(t_seq)):
        likelihood = nbinom.logpmf(t_seq[i] - 1, paras[x_seq[i] - 1][0], paras[x_seq[i] - 1][1])
        #print(f"Value for {x_seq[i]} is {likelihood} and t_seq[i] - 1 is {t_seq[i] - 1}.")
        likelihoods.append(likelihood)
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
    mean_var = get_mean_var(series)
    parameters = get_parameters(mean_var)
    for i in range(len(parameters)):
        sim = failure(x_seq, t_seq, i, parameters[i], 10)
        print(f"Simulated values are: {sim}")
        total = 0
        for i in sim:
            total += i
        print(f"Average simulated value is {total / len(sim)}.")
    
    likelihoods = prob_mass_func(x_seq, t_seq, parameters)
    total = 0 
    for likelihood in likelihoods:
        total += likelihood
    print(f"The overall logged PMF total is: {total}.")

    return

if __name__ == "__main__":
    main()