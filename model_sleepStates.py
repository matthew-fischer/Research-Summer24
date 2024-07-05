import sys, numpy as np, matplotlib.pyplot as plt
from helpers import read_me

# THIS FUNCTION PLOTS THE SLEEP STATES OF PATIENT
def modelling(state, length):
    time = []
    for i in range(length):
        time.append(i + 1)

    x_points = np.array(time)
    y_points = np.array(state)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("MODELING SLEEP STATES OF PATIENT")
    plt.xlabel("Hours Patient has been Asleep", fontdict = font1)
    plt.ylabel("Each Sleep State", fontdict = font1)
    plt.xticks(np.arange(0, 1400, 200))
    custom_yticks = ["Awake", "REM", "NREM1", "NREM2", "NREM3"]
    plt.yticks(np.arange(1,6,1), custom_yticks)
    plt.plot(x_points, y_points, "o-", mfc = "white")

    plt.show()
    return

# THIS IS THE MAIN FUNCTION
def main():
    # TO RUN THIS FILE: SLEEPSTATE FILE NAME AS A COMMAND LINE ARGUMENT
    file = sys.argv[1]
    states = read_me(file)

    modelling(states, len(states))
    return

if __name__ == "__main__":
    main()