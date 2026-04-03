def single_point_crossover(parent1, parent2):
    n = len(parent1)
    point = random.randint(1, n - 1)   # pick a random cut point

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

# Example
p1 = [1,2,3,4,5,6,7,8]
p2 = [8,7,6,5,4,3,2,1]
c1, c2 = single_point_crossover(p1, p2)
print("Child1:", c1)
print("Child2:", c2)

### 2. Two-Point Crossover
def two_point_crossover(parent1, parent2):
    n = len(parent1)
    point1 = random.randint(1, n - 2)
    point2 = random.randint(point1 + 1, n - 1)

    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    return child1, child2


### 3. Uniform Crossover
# For **each position**, flip a coin to decide which parent contributes.
def uniform_crossover(parent1, parent2):
    child1 = []
    child2 = []

    for i in range(len(parent1)):
        if random.random() < 0.5:   # 50% chance
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])

    return child1, child2

### 4. Ordered Crossover (OX) — Important for permutations!
# Used when chromosomes are **permutations** (like city routes or queen positions — no repeats allowed).

def ordered_crossover(parent1, parent2):
    n = len(parent1)
    pt1 = random.randint(0, n - 2)
    pt2 = random.randint(pt1 + 1, n - 1)

    # copy the segment from parent1
    child1 = [None] * n
    child1[pt1:pt2] = parent1[pt1:pt2]

    # fill remaining positions from parent2 (in order, skip duplicates)
    remaining = [x for x in parent2 if x not in child1]
    idx = 0
    for i in range(n):
        if child1[i] is None:
            child1[i] = remaining[idx]
            idx += 1

    # child2: same but swap roles of parent1 and parent2
    child2 = [None] * n
    child2[pt1:pt2] = parent2[pt1:pt2]
    remaining2 = [x for x in parent1 if x not in child2]
    idx = 0
    for i in range(n):
        if child2[i] is None:
            child2[i] = remaining2[idx]
            idx += 1

    return child1, child2



def pmx_crossover(parent1, parent2):
    n = len(parent1)
    pt1 = random.randint(0, n - 2)
    pt2 = random.randint(pt1 + 1, n - 1)

    def pmx_child(p1, p2):
        child = [None] * n
        # Step 1: copy segment from p1
        child[pt1:pt2] = p1[pt1:pt2]

        # Step 2: for each element in p2's segment
        for i in range(pt1, pt2):
            val = p2[i]
            if val not in child:
                # find where to place it using the mapping
                pos = i
                while child[pos] is not None:
                    pos = p2.index(p1[pos])
                child[pos] = val

        # Step 3: fill remaining with p2
        for i in range(n):
            if child[i] is None:
                child[i] = p2[i]
        return child

    return pmx_child(parent1, parent2), pmx_child(parent2, parent1)


def cyclic_crossover(parent1, parent2):
    n = len(parent1)
    child1 = [None] * n
    child2 = [None] * n

    # find all cycles
    visited = [False] * n
    cycles = []

    for start in range(n):
        if not visited[start]:
            cycle = []
            idx = start
            while idx not in cycle:
                cycle.append(idx)
                visited[idx] = True
                val = parent2[idx]
                idx = parent1.index(val)
            cycles.append(cycle)

    # alternate cycles between parents
    for i, cycle in enumerate(cycles):
        for idx in cycle:
            if i % 2 == 0:   # even cycles from parent1
                child1[idx] = parent1[idx]
                child2[idx] = parent2[idx]
            else:             # odd cycles from parent2
                child1[idx] = parent2[idx]
                child2[idx] = parent1[idx]

    return child1, child2