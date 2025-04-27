import matplotlib.pyplot as plt

# Set parameters
max_turns = 25
turns = list(range(0, 100))  # simulate up to 120 turns
randomness = []

for turn in turns:
    prob = max(0.2, 0.8 * (1 - turn / max_turns))
    randomness.append(prob)

# Plotting
plt.plot(turns, randomness)
plt.xlabel('Turn Count')
plt.ylabel('Randomness Probability')
plt.title('Randomness Decay Over Turns')
plt.grid(True)
plt.show()
