# ROULETTE WHEEL SELECTION
# Like spinning a wheel where fitter individuals get bigger slices
def roulette_wheel_selection(population):
    # Step 1: Calculate how fit each individual is
    fitnesses = [fitness(ind) for ind in population]
    total_fitness = sum(fitnesses)

    # Step 2: Pick a random number between 0 and total fitness
    pick = random.uniform(0, total_fitness)

    # Step 3: Go through population and add up fitness until we reach 'pick'
    current = 0
    for i, ind in enumerate(population):
        current += fitnesses[i]
        if current >= pick:
            return ind  # Found the selected individual!


# TOURNAMENT SELECTION
# Pick a few random individuals and choose the best one (like a mini competition)
def tournament_selection(population, tournament_size=3):
    # Step 1: Randomly pick some individuals for the tournament
    tournament = random.sample(population, tournament_size)

    # Step 2: Find who has the best fitness in this tournament
    best = max(tournament, key=fitness)
    return best

# RANK SELECTION
# Everyone gets a rank (1st, 2nd, 3rd...) and selection is based on rank, not fitness
# This prevents one super-fit individual from dominating
def rank_selection(population):
    # Step 1: Sort everyone from worst to best
    sorted_pop = sorted(population, key=fitness)

    # Step 2: Give ranks: worst = 1, second worst = 2, ..., best = N
    n = len(sorted_pop)
    ranks = list(range(1, n + 1))  # [1, 2, 3, 4, ..., n]
    total_rank = sum(ranks)

    # Step 3: Use roulette wheel but with ranks instead of fitness
    pick = random.uniform(0, total_rank)
    current = 0
    for i, ind in enumerate(sorted_pop):
        current += ranks[i]
        if current >= pick:
            return ind


# ELITISM
# Keep the best individuals safe - they automatically go to next generation
# This prevents losing your best solutions
def elitism(population, elite_size=2):
    # Step 1: Sort everyone from best to worst
    sorted_pop = sorted(population, key=fitness, reverse=True)

    # Step 2: Take the top individuals
    elites = sorted_pop[:elite_size]
    return elites

# EXAMPLE: Using elitism in a genetic algorithm
def ga_with_elitism(population, pop_size, elite_size=2):
    # Step 1: Keep the best individuals safe
    new_population = elitism(population, elite_size)

    # Step 2: Fill the rest of the population with new children
    while len(new_population) < pop_size:
        # Select two parents
        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)
        
        # Create children by combining parents
        child1, child2 = crossover(parent1, parent2)
        
        # Add some random changes (mutation) and add to new population
        new_population.append(mutate(child1))
        new_population.append(mutate(child2))

    return new_population