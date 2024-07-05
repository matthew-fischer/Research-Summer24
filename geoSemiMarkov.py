import sys
from helpers import read_me, build_seqs, count_matrix, transition_matrix

# THIS RETURNS THE TOTAL NUMBER OF TIMES PATIENT TRANSITIONED IN EACH STATE
def transition_totals(states):
    totals = [0,0,0,0,0]
    count = 0
    for state in states:
        if (count == 0):  # WE ARE COUNTING TRANSITIONS SO THE FIRST ONE DOESN'T COUNT
            count += 1
        else:
            totals[state - 1] += 1
    return totals

def switches(matrix):
    switch = []
    for row in matrix:
        total = 0
        for count in row:
            total += count
        switch.append(total)
    return switch

def geometric_distribution(totals, switch):
    probabilities = []
    for state in range(len(switch)):
        if (totals[state] == 0 or switch[state] == 0):  # If you never go to state i, the probability of switching out of state i is 0.
            probabilities.append(0)
        else:
            probabilities.append(round(switch[state] / totals[state], 4))
    return probabilities

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)

    # BUILDING THE X AND T SEQUENCES
    sequences = build_seqs(states)
    x_sequence = sequences[0]  # The transition between states.

    # COUNTS OF TRANSITION FOR EACH STATE USING X_SEQUENCE:
    counts_x = count_matrix(x_sequence)
    # TRANSITION MATRIX USING X_SEQUENCE:
    print("TRANSITION MATRIX USING X_SEQUENCE DATA.")
    transitions_x = transition_matrix(x_sequence)
    for row in transitions_x:
        print(row)
    print("\n")

    # TOTAL TRANSITIONS FROM STATE i
    totals = transition_totals(states)
    # HOW MANY TIMES THE PATIENT SWITCHED OUT OF STATE i
    switch = switches(counts_x)

    # THE GEOMETRIC DISTRIBUTION OF TRANSITIONING OUT OF EACH STATE
    geometric_results = geometric_distribution(totals, switch)
    print("THE GEOMETRIC DISTRIUBTION OF TRANSITIONING OUT OF EACH STATE.")
    print(geometric_results)

if __name__ == "__main__":
    main()