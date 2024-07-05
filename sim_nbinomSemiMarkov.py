import sys, numpy as np, matplotlib.pyplot as plt
from helpers import read_me, build_seqs, transition_matrix
from nbinomSemiMarkov import create_series, get_mean_var, get_parameters, failure

def simulation(x_seq, t_seq, trans_matrix, paras, length):
    sleep_states = []
    current_state = 1  # Starting state is 1
    while (len(sleep_states) < length):
        sleep_states.append(current_state)
        remain = failure(x_seq, t_seq, current_state - 1, paras[current_state - 1], 1)  # This determines how long we stay in current_state. (Following Negative Binomial Distribution).
        for i in range(remain[0]):
            if (len(sleep_states)) < length:
                sleep_states.append(current_state)
        switch_probabilities = trans_matrix[current_state - 1]
        current_state = np.random.choice([1,2,3,4,5], p=switch_probabilities)
    # End state is 1
    sleep_states.append(1)
    return sleep_states

def plotting(sleep_states, length):
    time = []
    for i in range(length):
        time.append(i + 1)

    x_points = np.array(time)
    y_points = np.array(sleep_states)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("Semi Markov Model following Negative Binomial Distribution")
    plt.xlabel("Hours Patient has been Asleep", fontdict = font1)
    plt.ylabel("Each Sleep State", fontdict = font1)
    plt.xticks(np.arange(0, 1400, 200))
    custom_yticks = ["Awake", "REM", "NREM1", "NREM2", "NREM3"]
    plt.yticks(np.arange(1,6,1), custom_yticks)
    plt.plot(x_points, y_points, "o-", mfc = "white")

    plt.show()

    return

def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    filename = sys.argv[1]
    states = read_me(filename)
    seq = build_seqs(states)
    x_seq = seq[0]
    t_seq = seq[1]

    semi_markov_matrix = transition_matrix(x_seq)
    series = create_series(x_seq, t_seq)
    mean_var = get_mean_var(series)
    parameters = get_parameters(mean_var)
    sim_sleep_states = simulation(x_seq, t_seq, semi_markov_matrix, parameters, len(states))

    sim_matrix = transition_matrix(sim_sleep_states)
    print("Transition matrix using simulated sleep states:")
    for row in sim_matrix:
        print(row)
    print("\n")
    matrix = transition_matrix(states)
    print("Transition matrix using sleep states from patient:")
    for row in matrix:
        print(row)
    print("\n")

    plotting(sim_sleep_states, len(sim_sleep_states))

    return

if __name__ == "__main__":
    main()