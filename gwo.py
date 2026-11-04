
import random

# Number of roads
N = 4

# Number of wolves
num_wolves = 10

# Maximum iterations
max_iterations = 50

# Number of vehicles on each road
vehicles = [40, 20, 60, 30]

# Green signal time limits
min_time = 10
max_time = 90

# Fitness function
def fitness(wolf):
    total_waiting = 0

    for i in range(N):
        # More vehicles need more green time
        waiting = max(0, vehicles[i] - wolf[i])
        total_waiting += waiting

    return total_waiting

# Initialize wolves randomly
wolves = [
    [random.uniform(min_time, max_time) for _ in range(N)]
    for _ in range(num_wolves)
]

# GWO algorithm
for iteration in range(max_iterations):

    # Sort wolves based on fitness
    wolves.sort(key=fitness)

    alpha = wolves[0]
    beta = wolves[1]
    delta = wolves[2]

    a = 2 - (2 * iteration / max_iterations)

    for wolf in wolves:
        for j in range(N):

            r1, r2 = random.random(), random.random()
            r3, r4 = random.random(), random.random()
            r5, r6 = random.random(), random.random()

            A1 = 2 * a * r1 - a
            C1 = 2 * r2

            A2 = 2 * a * r3 - a
            C2 = 2 * r4

            A3 = 2 * a * r5 - a
            C3 = 2 * r6

            D1 = abs(C1 * alpha[j] - wolf[j])
            D2 = abs(C2 * beta[j] - wolf[j])
            D3 = abs(C3 * delta[j] - wolf[j])

            X1 = alpha[j] - A1 * D1
            X2 = beta[j] - A2 * D2
            X3 = delta[j] - A3 * D3

            # Update position
            wolf[j] = (X1 + X2 + X3) / 3

            # Boundary checking
            wolf[j] = max(min_time,
                          min(max_time, wolf[j]))

# Find best solution
wolves.sort(key=fitness)
best = wolves[0]

print("SMART TRAFFIC SIGNAL OPTIMIZATION")
print("--------------------------------")

roads = ["North", "South", "East", "West"]

for i in range(N):
    print(roads[i], "Green Time:",
          round(best[i], 2), "seconds")

print("Fitness:", round(fitness(best), 2))
