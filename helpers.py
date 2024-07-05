import random

# READ IN DATA FROM SLEEPSTATE FILE (CSV FILE)
def read_me(file):
    states = []
    file = open(file, "r")
    file.readline()  # THE FIRST LINE IS THE R HEADER (THROW IT AWAY)
    for line in file:
        index = line.find(",")
        states.append(int(line[index + 1: index + 2]))
    return states

# GET PROBABILTIES OF EACH SLEEP STATE
def probabilities(sequence, length):
    ones = 0
    twos = 0
    threes = 0
    fours = 0
    fives = 0
    for i in sequence:
        if (i == 1):
            ones += 1
        elif (i == 2):
            twos += 1
        elif (i == 3):
            threes += 1
        elif (i == 4):
            fours += 1
        else: # i == 5
            fives += 1
    prob_ones = ones/length
    prob_twos = twos/length
    prob_threes = threes/length
    prob_fours = fours/length
    prob_fives = fives/length

    return [prob_ones, prob_twos, prob_threes, prob_fours, prob_fives]

# CREATE THE RANDOM SEQUENCE OF DATA
def create_sequence():
    sequence = []
    for i in range(0, 1000):
        sequence.append(random.randint(1,5))
    # 1 = Awake, 2 = REM, 3 = NREM1, 4 = NREM2, 5 = NREM3
    return sequence

# BUILDING MATRIX BASED ON TRANSITION COUNTS
def count_matrix(transitions):
    matrix = [[0] * 5 for _ in range(5)]  # CREATING 5x5 Matrix

    for (i,j) in zip(transitions, transitions[1:]):
        matrix[i - 1][j - 1] += 1
    return matrix

# MAKING THE TRANSITION MATRIX
def transition_matrix(transitions):
    matrix = [[0] * 5 for _ in range(5)]

    for (i,j) in zip(transitions, transitions[1:]):
        matrix[i - 1][j - 1] += 1
    
    for row in matrix:  # Make each row a vector summing to one.
        total = sum(row)
        if total > 0:
            row[:] = [round(f/sum(row), 4) for f in row]
    return matrix

# MAKING SURE EACH ROW OF TRANSITION MATRIX ADDS TO ONE
def check_transition_matrix(matrix):
    vector = []
    for row in matrix:
        vector.append(int(sum(row)))
    return vector

# ITERATING THROUGH THE SLEEP STATES
def build_seqs(states):
    x_seq = []  # The transition between states.
    t_seq = []  # Length of time remaining in each state.
    remain = 0
    for index in range(len(states)):
        if (index == 0):
            # STARTING STATE
            pass
        elif (states[index] == states[index - 1]):
            # DID NOT MOVE STATE
            remain += 1
        else:
            # MOVED STATE
            t_seq.append(remain + 1)
            remain = 0
            x_seq.append(states[index - 1])

    x_seq.append(states[index])
    t_seq.append(remain + 1)

    return [x_seq, t_seq]