
import random

# Locations: A, B, C, D, E
cities = ["A", "B", "C", "D", "E"]
n = len(cities)

# Road distances between locations (km)
distance = [
    [0,  4,  2,  0,  0],
    [4,  0,  1,  5,  0],
    [2,  1,  0,  8, 10],
    [0,  5,  8,  0,  2],
    [0,  0, 10,  2,  0]
]

# Traffic congestion multipliers
traffic = [
    [0, 1.5, 1.0, 0,   0],
    [1.5, 0, 1.0, 1.2, 0],
    [1.0, 1.0, 0, 1.5, 1.2],
    [0, 1.2, 1.5, 0,   1.0],
    [0, 0,   1.2, 1.0, 0]
]

# Effective travel cost: distance affected by traffic
cost = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if distance[i][j] > 0:
            cost[i][j] = distance[i][j] * traffic[i][j]

# ACO parameters
ants = 10
iterations = 50
alpha = 1.0       # Pheromone importance
beta = 2.0        # Distance importance
evaporation = 0.5
Q = 100

# Initialize pheromones on existing roads
pheromone = [[0.0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if cost[i][j] > 0:
            pheromone[i][j] = 1.0

def choose_next(current, unvisited):
    choices = []
    total = 0

    for city in unvisited:
        if cost[current][city] > 0:
            value = (
                pheromone[current][city] ** alpha
                * (1 / cost[current][city]) ** beta
            )
            choices.append((city, value))
            total += value

    if not choices:
        return None

    pick = random.random() * total
    running = 0

    for city, value in choices:
        running += value
        if running >= pick:
            return city

    return choices[-1][0]

best_route = None
best_cost = float("inf")

for iteration in range(iterations):
    all_routes = []

    for ant in range(ants):
        route = [0]  # Start at A
        unvisited = set(range(1, n))
        current = 0
        total_cost = 0

        while unvisited:
            next_city = choose_next(current, unvisited)

            if next_city is None:
                break

            total_cost += cost[current][next_city]
            route.append(next_city)
            unvisited.remove(next_city)
            current = next_city

        # Return to A to complete the tour
        if len(route) == n and cost[current][0] > 0:
            total_cost += cost[current][0]
            route.append(0)

            all_routes.append((route, total_cost))

            if total_cost < best_cost:
                best_cost = total_cost
                best_route = route[:]

    # Evaporate pheromones
    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= (1 - evaporation)

    # Reinforce better routes
    for route, route_cost in all_routes:
        deposit = Q / route_cost

        for i in range(len(route) - 1):
            a, b = route[i], route[i + 1]
            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

if best_route is not None:
    print("Best route:", " -> ".join(cities[i] for i in best_route))
    print("Total travel cost:", round(best_cost, 2))
else:
    print("No complete route found.")
