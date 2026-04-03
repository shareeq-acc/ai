"""
Travelling Salesman Problem (TSP) - Genetic Algorithm Implementation
Chromosome representation: list of city indices representing the tour order
Example: [0, 2, 1, 3] means visit city 0 → 2 → 1 → 3 → back to 0
"""

import random

# Example: Distance matrix for 5 cities
# distances[i][j] = distance from city i to city j
distances = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]


# ============= FITNESS FUNCTION =============

def fitness_tsp(chromosome):
    """
    Calculate total tour distance. Lower distance = better tour.
    Returns: negative total distance (higher fitness = shorter tour)
    """
    total_distance = 0
    num_cities = len(chromosome)
    
    # Calculate distance for each consecutive pair of cities
    for i in range(num_cities):
        current_city = chromosome[i]
        next_city = chromosome[(i + 1) % num_cities]  # wrap around to start
        total_distance += distances[current_city][next_city]
    
    return -total_distance  # negative so higher fitness = better


# ============= SELECTION CRITERIA =============

def tournament_selection(population, fitness_scores, tournament_size=3):
    """
    Select parent using tournament selection.
    Randomly pick tournament_size individuals and return the best one.
    """
    tournament_indices = random.sample(range(len(population)), tournament_size)
    best_index = max(tournament_indices, key=lambda i: fitness_scores[i])
    return population[best_index]


def roulette_wheel_selection(population, fitness_scores):
    """
    Select parent using roulette wheel (fitness proportionate) selection.
    Adjusts for negative fitness values by shifting to positive range.
    """
    # Shift fitness to positive (add absolute value of minimum)
    min_fitness = min(fitness_scores)
    adjusted_fitness = [f - min_fitness + 1 for f in fitness_scores]
    
    total_fitness = sum(adjusted_fitness)
    pick = random.uniform(0, total_fitness)
    
    current_sum = 0
    for i, fitness in enumerate(adjusted_fitness):
        current_sum += fitness
        if current_sum >= pick:
            return population[i]
    
    return population[-1]  # fallback


# ============= CROSSOVER OPERATORS =============

def order_crossover(parent1, parent2):
    """
    Order Crossover (OX): Preserves relative order of cities.
    1. Select a substring from parent1
    2. Fill remaining positions with cities from parent2 in order
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    # Copy substring from parent1
    child = [None] * size
    child[start:end] = parent1[start:end]
    
    # Fill remaining with cities from parent2 in order
    parent2_filtered = [city for city in parent2 if city not in child]
    
    j = 0
    for i in range(size):
        if child[i] is None:
            child[i] = parent2_filtered[j]
            j += 1
    
    return child


def pmx_crossover(parent1, parent2):
    """
    Partially Mapped Crossover (PMX): Creates mapping between two parents.
    1. Select a substring and swap between parents
    2. Resolve conflicts using mapping
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    child = parent1.copy()
    
    # Create mapping from the crossover segment
    mapping = {}
    for i in range(start, end):
        mapping[parent2[i]] = parent1[i]
    
    # Fill child with parent2's segment
    for i in range(start, end):
        child[i] = parent2[i]
    
    # Fix conflicts outside the segment
    for i in list(range(0, start)) + list(range(end, size)):
        city = parent1[i]
        while city in child[start:end]:
            city = mapping[city]
        child[i] = city
    
    return child


def cycle_crossover(parent1, parent2):
    """
    Cycle Crossover (CX): Each city comes from one parent at the same position.
    Identifies cycles and alternates between parents.
    """
    size = len(parent1)
    child = [None] * size
    
    # Find first cycle
    index = 0
    while child[index] is not None:
        index += 1
        if index >= size:
            break
    
    if index < size:
        # Build cycle starting from this index
        cycle_start = index
        while True:
            child[index] = parent1[index]
            city = parent2[index]
            index = parent1.index(city)
            
            if index == cycle_start:
                break
    
    # Fill remaining positions from parent2
    for i in range(size):
        if child[i] is None:
            child[i] = parent2[i]
    
    return child


# ============= TESTING =============

if __name__ == "__main__":
    # Test chromosome: tour visiting all 5 cities
    tour1 = [0, 1, 2, 3, 4]
    tour2 = [0, 2, 4, 1, 3]
    
    print("=== TSP Genetic Algorithm ===\n")
    
    # Test fitness
    print("Tour 1:", tour1)
    print("Fitness:", fitness_tsp(tour1))
    print("Actual distance:", -fitness_tsp(tour1))
    print()
    
    print("Tour 2:", tour2)
    print("Fitness:", fitness_tsp(tour2))
    print("Actual distance:", -fitness_tsp(tour2))
    print()
    
    # Test crossover
    print("=== Crossover Examples ===")
    print("Parent 1:", tour1)
    print("Parent 2:", tour2)
    print()
    
    child1 = order_crossover(tour1, tour2)
    print("Order Crossover child:", child1)
    
    child2 = pmx_crossover(tour1, tour2)
    print("PMX Crossover child:", child2)
    
    child3 = cycle_crossover(tour1, tour2)
    print("Cycle Crossover child:", child3)
    print()
    
    # Test selection
    population = [tour1, tour2, [0, 3, 1, 4, 2], [0, 4, 3, 2, 1]]
    fitness_scores = [fitness_tsp(tour) for tour in population]
    
    print("=== Selection Examples ===")
    print("Population fitness:", fitness_scores)
    selected = tournament_selection(population, fitness_scores)
    print("Tournament selection:", selected)
    
    selected = roulette_wheel_selection(population, fitness_scores)
    print("Roulette wheel selection:", selected)
