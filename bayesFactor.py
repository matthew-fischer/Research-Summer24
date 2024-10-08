import sys, math
from helpers import read_me, probabilities, count_matrix, transition_matrix, build_seqs
from markov_chain import counts
from geoSemiMarkov import transition_totals, switches, geometric_distribution
from poisSemiMarkov import lambda_state
from nbinomSemiMarkov import create_series, get_mean_var, get_parameters
from binomSemiMarkov import findingN, success_failure_prob
from logSemiMarkov import avg_series, prob
from scipy.stats import nbinom, binom, logser

# GETTING LOG VALUE FOR FREQUENTIST NAIVE MODEL
def data_model_naive(probabilities, counts, length):
    total = 0
    for i in range(length):
        if ((probabilities[i] == 0) or (counts[i] == 0)):
            continue
        else:
            total += (counts[i] * math.log(probabilities[i]))  # P hat j * log(P hate j)
    return total

# GETTING LOG VALUE FOR MARKOV MODEL
def data_model_markov(matrix, probabilities, length):
    total = 0
    for row in range(length):
        for col in range(length):
            if (probabilities[row][col] == 0):
                continue
            else:
                total += matrix[row][col] * math.log(probabilities[row][col])
    return total

# GETTING LOG VALUE FOR SEMI-MARKOV MODEL (USING A GEOMETRIC DISTRIBUTION)
def data_model_geoSemi(x_seq, t_seq, matrix, geo_results):
    total = 0
    for i in range(1, len(x_seq)):
        row = x_seq[i-1] - 1
        col = x_seq[i] - 1
        total += math.log(matrix[row][col])
    for j in range(len(x_seq)):
        index = x_seq[j] - 1
        if (geo_results[index] == 1):
            continue
        else:
            total += ((t_seq[j] - 1) * math.log(1 - geo_results[index]))  # Ti - 1 because the first state is given.
    for x in range(len(x_seq)):
        index = x_seq[x] - 1
        if (geo_results[index] == 0):
            continue
        else:
            total += math.log(geo_results[index])
    return total

# GETTING LOG VALUE FOR SEMI-MARKOV MODEL (USING A POISSON DISTRIBUTION)
def data_model_poisSemi(x_seq, t_seq, matrix, expected_lambdas):
    total = 0
    for i in range(1, len(x_seq)):
        row = x_seq[i-1] - 1
        col = x_seq[i] - 1
        total += math.log(matrix[row][col])
    for j in range(len(x_seq)):
        index = x_seq[j] - 1  # Minus one since x_seq values range from 1-5.
        if (expected_lambdas[index] == 0):
            continue
        else:
            total += ((t_seq[j] - 1) * math.log(expected_lambdas[index])) - expected_lambdas[index] - math.log(math.factorial(t_seq[j] - 1))
    return total

# GETTING LOG VALUE FOR SEMI-MARKOV MODEL (USING A NEGATIVE BINOMIAL DISTRIBUTION)
def data_model_nbinomSemi(x_seq, t_seq, matrix, expected_lambdas, parameters):
    total = 0
    for i in range(1, len(x_seq)):
        row = x_seq[i-1] - 1
        col = x_seq[i] - 1
        total += math.log(matrix[row][col])
    for j in range(len(x_seq)):
        # parameters[i] are [r,p]
        # x_seq[j] is the current state
        index = x_seq[j] - 1
        if (parameters[index][0] > 0 and parameters[index][1] < 1):
            # Negative Binomial Distribution is being used here.
            total += nbinom.logpmf(t_seq[j] - 1, parameters[index][0], parameters[index][1])
        else:
            # Poisson Distribution is being used here.
            if (expected_lambdas[index] == 0):
                continue
            else:
                total += ((t_seq[j] - 1) * math.log(expected_lambdas[index])) - expected_lambdas[index] - math.log(math.factorial(t_seq[j] - 1))
    return total

# GETTING LOG VALUE FOR SEMI-MARKOV MODEL (USING A BINOMIAL DISTRIBUTION)
def data_model_binomSemi(x_seq, t_seq, matrix, probabilities, max_num):
    total = 0
    for i in range(1, len(x_seq)):
        row = x_seq[i-1] - 1
        col = x_seq[i] - 1
        total += math.log(matrix[row][col])
    for j in range(len(x_seq)):
        index = x_seq[j] - 1  # x_seq[j] is the current state
        total += binom.logpmf(t_seq[j] - 1, max_num[index], probabilities[index])
    return total

# GETTING LOG VALUE FOR SEMI-MARKOV MODEL (USING A LOGARITHMIC DISTRIBUTION)
def data_model_logSemi(x_seq, t_seq, matrix, probabilities):
    total = 0
    for i in range(1, len(x_seq)):
        row = x_seq[i-1] - 1
        col = x_seq[i] - 1
        total += math.log(matrix[row][col])
    for j in range(len(x_seq)):
        index = x_seq[j] - 1  # x_seq[j] is the current state
        if (probabilities[index] != 0):  # AVOIDING NAN PROBLEM
            calculated = logser.logpmf(t_seq[j], probabilities[index])
            if (math.isnan(calculated) == False):  # IS THIS OKAY TO DO.
                total += logser.logpmf(t_seq[j], probabilities[index])
    return total

def log_bayes_factor(model1, model2):
    return (model1 - model2)

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    # FOR NAIVE:
    probability = probabilities(states, len(states))
    count_naive = counts(probability, len(states))
    # FOR MARKOV:
    matrix_markov = count_matrix(states)
    trans_matrix_markov = transition_matrix(states)
    # FOR GEO SEMI MARKOV:
    sequences = build_seqs(states)
    x_sequence = sequences[0]
    t_sequence = sequences[1]
    trans_matrix= transition_matrix(x_sequence)
    counts_matrix = count_matrix(x_sequence)
    totals_geoSemi = transition_totals(states)
    switch_geoSemi = switches(counts_matrix)
    results_geoSemi = geometric_distribution(totals_geoSemi, switch_geoSemi)
    # FOR POIS SEMI MARKOV:
    STATE_RANGE = [1,2,3,4,5]
    expected = lambda_state(x_sequence, t_sequence, STATE_RANGE)
    # FOR NBINOM SEMI MARKOV:
    series = create_series(x_sequence, t_sequence)
    mean_var = get_mean_var(series)
    parameters = get_parameters(mean_var)
    # FOR BINOM SEMI MARKOV:
    max_per_state = findingN(series)
    switch_probability = success_failure_prob(max_per_state, series)
    # FOR LOG SEMI MARKOV:
    avgSeries = avg_series(series)
    switch_prob = prob(avgSeries)

    # CALCULATES P(DATA | MODEL):
    naive = data_model_naive(probability, count_naive, len(probability))
    print(f"Naive log( P(Data|Model) ) is {naive}.")
    markov = data_model_markov(matrix_markov, trans_matrix_markov, len(probability))
    print(f"Markov log( P(Data|Model) ) is {markov}.")
    semi_geo = data_model_geoSemi(x_sequence, t_sequence, trans_matrix, results_geoSemi)
    print(f"Semi Markov Geometric Distribution log( P(Data|Model) ) is {semi_geo}.")
    semi_pois = data_model_poisSemi(x_sequence, t_sequence, trans_matrix, expected)
    print(f"Semi Markov Poisson Distribution log ( P(Data|Model) ) is {semi_pois}.")
    semi_nbinom = data_model_nbinomSemi(x_sequence, t_sequence, trans_matrix, expected, parameters)
    print(f"Semi Markov Negative Binomial Distribution log ( P(Data|Model) ) is {semi_nbinom}.")
    semi_binom = data_model_binomSemi(x_sequence, t_sequence, trans_matrix, switch_probability, max_per_state)
    print(f"Semi Markov Binomial Distribution log ( P(Data|Model) ) is {semi_binom}.")
    semi_log = data_model_logSemi(x_sequence, t_sequence, trans_matrix, switch_prob)
    print(f"Semi Markov Logarithmic Distribution log ( P(Data|Model) ) is {semi_log}.")

    print("\n")

    # CALCULATES LOGGED BAYES FACTOR:
    log_bf_markov_naive = log_bayes_factor(markov, naive)
    print(f"The Logged Bayes Factor Value Between Markov and Naive is {log_bf_markov_naive}.")
    log_bf_geoSemi = log_bayes_factor(markov, semi_geo)
    print(f"The Logged Bayes Factor Value Between the Markov and the Semi Markov(Geometric) is {log_bf_geoSemi}.")
    log_bf_poisSemi = log_bayes_factor(markov, semi_pois)
    print(f"The Logged Bayes Factor Value Between the Markov and the Semi Markov(Poisson) is {log_bf_poisSemi}.")
    log_bf_nbinomSemi = log_bayes_factor(markov, semi_nbinom)
    print(f"The Logged Bayes Factor Value Between the Markov and the Semi Markov(Negative Binomial) is {log_bf_nbinomSemi}.")
    log_bf_binomSemi = log_bayes_factor(markov, semi_binom)
    print(f"The Logged Bayes Factor Value Between the Markov and the Semi Markov(Binomial) is {log_bf_binomSemi}.")
    log_bf_logSemi = log_bayes_factor(markov, semi_log)
    print(f"The Logged Bayes Factor Value Between the Markov and the Semi Markov(Logarithmic) is {log_bf_logSemi}.")

if __name__ == "__main__":
    main()