import random

traffic = {
    "North-South": 40,
    "East-West": 25
}

CYCLE_TIME = 90
MIN_GREEN = 15
POPULATION_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.1

def gene_expression(genes):
    total = sum(genes)

    available_time = CYCLE_TIME - 2 * MIN_GREEN

    green_ns = MIN_GREEN + available_time * genes[0] / total
    green_ew = MIN_GREEN + available_time * genes[1] / total

    return green_ns, green_ew

def fitness(genes):
    green_ns, green_ew = gene_expression(genes)

    cost = (
        traffic["North-South"] ** 2 / green_ns
        + traffic["East-West"] ** 2 / green_ew
    )

    return cost

def create_population():
    return [
        [random.uniform(0.1, 1),
         random.uniform(0.1, 1)]
        for _ in range(POPULATION_SIZE)
    ]

def selection(population):
    candidates = random.sample(population, 3)
    return min(candidates, key=fitness)

def crossover(parent1, parent2):
    child = []

    for i in range(2):
        if random.random() < 0.5:
            child.append(parent1[i])
        else:
            child.append(parent2[i])

    return child

# Mutation
def mutation(genes):
    genes = genes.copy()

    for i in range(2):
        if random.random() < MUTATION_RATE:
            genes[i] = random.uniform(0.1, 1)

    return genes

# Gene Expression Algorithm
def gene_expression_algorithm():

    random.seed(42)

    population = create_population()

    best_gene = min(population, key=fitness)

    for generation in range(GENERATIONS):

        population.sort(key=fitness)

        # Preserve the best two individuals
        new_population = population[:2]

        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)

            child = mutation(child)

            new_population.append(child)

        population = new_population

        current_best = min(population, key=fitness)

        if fitness(current_best) < fitness(best_gene):
            best_gene = current_best.copy()

    return best_gene


# Main program
if __name__ == "__main__":

    best_gene = gene_expression_algorithm()

    # Express genes into signal timings
    green_ns, green_ew = gene_expression(best_gene)

    print("SMART TRAFFIC SIGNAL OPTIMIZATION")
    print("----------------------------------")

    print("North-South Vehicles:",
          traffic["North-South"])

    print("East-West Vehicles:",
          traffic["East-West"])

    print("----------------------------------")

    print("Optimized Green Signal Timing:")

    print("North-South:",
          round(green_ns, 2), "seconds")

    print("East-West:",
          round(green_ew, 2), "seconds")

    print("----------------------------------")

    print("Total Signal Cycle:",
          CYCLE_TIME, "seconds")

    print("Minimum Green Time:",
          MIN_GREEN, "seconds")

    print("Optimized Fitness:",
          round(fitness(best_gene), 2))