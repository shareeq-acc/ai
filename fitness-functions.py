# N-Queens Fitness Function
# chromosome = [row positions of queen in each column]
# e.g. [2, 0, 3, 1] means: col 0 → row 2, col 1 → row 0, etc.

def fitness_nqueens(chromosome):
    """
    Counts non-attacking queen pairs. Higher fitness = better solution.
    Returns: number of queen pairs that don't attack each other.
    """
    n = len(chromosome)
    attacks = 0

    for col1 in range(n):
        for col2 in range(col1 + 1, n):
            row1, row2 = chromosome[col1], chromosome[col2]
            
            # Check if queens attack each other (same row or diagonal)
            if row1 == row2 or abs(row1 - row2) == abs(col1 - col2):
                attacks += 1

    max_pairs = n * (n - 1) // 2
    return max_pairs - attacks

# Test
chrom = [2, 0, 3, 1]   # a valid solution for 4-queens
print("Fitness:", fitness_nqueens(chrom))  # should be 6 (no clashes)

# Maze Fitness Function
# maze: 0 = open path, 1 = wall
maze = [
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]
start = (0, 0)
goal  = (3, 3)

def fitness_maze(chromosome):
    """
    Evaluates a sequence of moves through the maze.
    chromosome = list of moves: 0=up, 1=down, 2=left, 3=right
    Returns: 100 if goal reached, otherwise negative Manhattan distance.
    """
    current_row, current_col = start
    num_rows = len(maze)
    num_cols = len(maze[0])
    
    # Direction mappings: up, down, left, right
    directions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

    for move_direction in chromosome:
        row_delta, col_delta = directions[move_direction]
        next_row = current_row + row_delta
        next_col = current_col + col_delta

        # Move only if valid (in bounds and not a wall)
        if (0 <= next_row < num_rows and 
            0 <= next_col < num_cols and 
            maze[next_row][next_col] == 0):
            current_row, current_col = next_row, next_col

        # Check if we reached the goal
        if (current_row, current_col) == goal:
            return 100

    # Calculate Manhattan distance from current position to goal
    distance_to_goal = abs(current_row - goal[0]) + abs(current_col - goal[1])
    return -distance_to_goal

# Test
moves = [1, 3, 1, 3, 1, 3]   # some random moves
print("Fitness:", fitness_maze(moves))



# 8-Puzzle Fitness Function
# Goal state (flat list): 0 = empty space
goal_state = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]

def fitness_8puzzle(chromosome):
    """
    Counts how many tiles are in their correct position.
    Returns: number of correctly placed tiles (excluding empty space).
    """
    correct_tiles = 0
    for position in range(len(chromosome)):
        if chromosome[position] == goal_state[position] and chromosome[position] != 0:
            correct_tiles += 1
    return correct_tiles

# Test
state1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]   # perfect
state2 = [1, 2, 3, 4, 0, 6, 7, 5, 8]   # 2 tiles wrong
print("Fitness state1:", fitness_8puzzle(state1))   # 8
print("Fitness state2:", fitness_8puzzle(state2))   # 6