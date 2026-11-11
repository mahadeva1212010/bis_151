
import random

# Number of roads and nests
n = 10
Pa = 0.25
MaxT = 100

# Number of vehicles on 4 roads
vehicles = [50, 100, 30, 80]

# Total green signal time
total_time = 120

# Generate random signal timings
def generate_nest():
    times = [random.uniform(10, 60) for i in range(4)]
    s = sum(times)
    return [max(10, x * total_time / s) for x in times]

# Calculate fitness (lower waiting time is better)
def fitness(nest):
    return sum(vehicles[i] / nest[i] for i in range(4))

# Initialize nests
nests = [generate_nest() for i in range(n)]

# Cuckoo Search Algorithm
for t in range(MaxT):

    # Generate a new solution using Levy Flight
    for i in range(n):
        new_nest = nests[i].copy()

        for j in range(4):
            step = random.gauss(0, 1) / (
                abs(random.gauss(0, 1)) ** (1 / 1.5) + 0.01
            )
            new_nest[j] += step * 5

        # Keep timings within limits
        new_nest = [max(10, x) for x in new_nest]

        # Normalize timings
        s = sum(new_nest)
        new_nest = [x * total_time / s for x in new_nest]

        # Select a random nest
        k = random.randint(0, n - 1)

        # Replace if new solution is better
        if fitness(new_nest) < fitness(nests[k]):
            nests[k] = new_nest

    # Abandon worst nests
    nests.sort(key=fitness)

    for i in range(int(Pa * n)):
        nests[-(i + 1)] = generate_nest()

    # Keep best solution
    nests.sort(key=fitness)

# Display result
best = nests[0]

print("Optimized Traffic Signal Timings:")
for i in range(4):
    print("Road", i + 1, ":", round(best[i], 2), "seconds")

print("Best Fitness:", round(fitness(best), 4))
 