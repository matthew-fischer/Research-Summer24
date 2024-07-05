import sys
from helpers import read_me, build_seqs

def totals(state, x_seq, t_seq):
    frequency = 0  # Number of times in specified state
    totalSum = 0  # Sum of time in specified state
    for i in range(len(x_seq)):
        if (x_seq[i] == state):
            frequency += 1
            totalSum += (t_seq[i] - 1)  # The first Ti is given.
    return [frequency, totalSum]

def lambdas(values):
    # This creates a lamda for a given state
    if (values[0] != 0):
        return round((1/values[0]) * (values[1]), 2)
    else:
        return 0

def lambda_state(x_seq, t_seq, state_range):
    lamdas_array = []
    for state in state_range:
        calculated_values = totals(state, x_seq, t_seq)
        lamdas_array.append(lambdas(calculated_values))
    return lamdas_array

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    seq = build_seqs(states)
    x_seq = seq[0]
    t_seq = seq[1]

    # Creating lamda's for each state:
    STATE_RANGE = [1,2,3,4,5]
    expected = lambda_state(x_seq, t_seq, STATE_RANGE)
    print(expected)

if __name__ == "__main__":
    main()