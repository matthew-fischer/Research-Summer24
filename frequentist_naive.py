import matplotlib.pyplot as plt, numpy as np
from helpers import create_sequence, probabilities

# GETS COUNTS OF EACH SLEEP STATE
def counts(probabilities, normalize):
    count = np.copy(probabilities)
    for i in range(len(count)):
        count[i] = int(count[i] * normalize)
    return count

# CREATES BAR GRAPH, FOR EACH i: #{St = i}
def bars(x_values, y_values):
    x_points = np.array(x_values)
    y_points = np.array(y_values)
    plt.bar(x_points, y_points, width = 0.5)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("Sleep States of Patient", fontdict = font1)
    plt.ylabel("# of Times Patient was in Each Sleep State", fontdict = font1)
    plt.xlabel("Sleep States", fontdict = font1)
    plt.show()
    return

# USING FREQUENTIST NAIVE MODELLING TO PLOT SLEEP STATES
def frequentistNaive(probability, length):
    state = []
    time = []
    current_time = 0  # zero since trial hasn't started
    for i in range(0, length - 1):
        current_time += 1  # Measures every 30 seconds
        state.append(np.random.choice([1,2,3,4,5], p=probability))
        time.append(current_time)
    # END STATE IS STATE 1
    state.append(1)  # This says patient is awake when the trail ends.
    time.append(current_time + 1)

    x_points = np.array(time)
    y_points = np.array(state)
    font1 = {'family':'serif', 'color':'black'}
    plt.title("Naive Model (Assuming Independence Between Sleep States)")
    plt.xlabel("Hours Patient has been Asleep", fontdict = font1)
    plt.ylabel("Each Sleep State", fontdict = font1)
    plt.xticks(np.arange(0, 1400, 200))
    custom_yticks = ["Awake", "REM", "NREM1", "NREM2", "NREM3"]
    plt.yticks(np.arange(1,6,1), custom_yticks)
    plt.plot(x_points, y_points, "o-", mfc = "white")
    plt.show()
    return

# MAIN FUNCTION
def main():
    sequence = create_sequence()
    probability = probabilities(sequence, len(sequence))
    count = counts(probability, len(sequence))

    #bars(states, count)
    frequentistNaive(probability, len(sequence))
    return

if __name__ == "__main__":
    main()