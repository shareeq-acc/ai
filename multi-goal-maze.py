from queue import PriorityQueue
from itertools import permutations

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.cost_from_start = 0
        self.distance_to_goal = 0
        self.priority = 0
    
    def __lt__(self, other):
        return self.priority < other.priority


def calculate_distance(current_pos, goal_pos):
    """Manhattan distance heuristic"""
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])


def best_first_search(maze, start, goal):
    """Find path from start to a single goal"""
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    
    to_explore = PriorityQueue()
    to_explore.put(start_node)
    visited = set()
    
    while not to_explore.empty():
        current = to_explore.get()
        current_pos = current.position
        
        if current_pos == goal:
            # Reconstruct path
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        visited.add(current_pos)
        
        # Check all 4 directions
        for row_change, col_change in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_pos = (current_pos[0] + row_change, current_pos[1] + col_change)
            
            if (0 <= neighbor_pos[0] < rows and 
                0 <= neighbor_pos[1] < cols and 
                maze[neighbor_pos[0]][neighbor_pos[1]] == 0 and 
                neighbor_pos not in visited):
                
                neighbor = Node(neighbor_pos, current)
                neighbor.cost_from_start = current.cost_from_start + 1
                neighbor.distance_to_goal = calculate_distance(neighbor_pos, goal)
                neighbor.priority = neighbor.distance_to_goal
                to_explore.put(neighbor)
                visited.add(neighbor_pos)
    
    return None  # No path found


def find_path_length(maze, start, goal):
    """Helper to get just the path length between two points"""
    path = best_first_search(maze, start, goal)
    return len(path) - 1 if path else float('inf')


def multi_goal_search_greedy(maze, start, goals):
    """
    APPROACH 1: Greedy - Visit nearest unvisited goal
    Fast but may not be optimal
    """
    current_pos = start
    remaining_goals = set(goals)
    complete_path = [start]
    total_distance = 0
    
    print("\n--- Greedy Approach ---")
    print(f"Starting at {start}")
    
    while remaining_goals:
        # Find nearest goal
        nearest_goal = None
        shortest_distance = float('inf')
        
        for goal in remaining_goals:
            distance = find_path_length(maze, current_pos, goal)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_goal = goal
        
        if nearest_goal is None:
            print("Cannot reach all goals!")
            return None
        
        # Get path to nearest goal
        path_segment = best_first_search(maze, current_pos, nearest_goal)
        if not path_segment:
            print(f"No path to goal {nearest_goal}")
            return None
        
        # Add to complete path (skip first point to avoid duplicates)
        complete_path.extend(path_segment[1:])
        total_distance += len(path_segment) - 1
        
        print(f"Visited goal {nearest_goal}, distance: {len(path_segment) - 1}")
        
        current_pos = nearest_goal
        remaining_goals.remove(nearest_goal)
    
    print(f"Total distance: {total_distance}")
    return complete_path


def multi_goal_search_optimal(maze, start, goals):
    """
    APPROACH 2: Try all permutations - Find optimal order
    Slower but guarantees shortest path
    """
    if len(goals) > 8:
        print("Too many goals for optimal search (>8), use greedy instead")
        return None
    
    print("\n--- Optimal Approach (trying all orders) ---")
    
    best_path = None
    best_distance = float('inf')
    best_order = None
    
    # Try all possible orderings of goals
    for goal_order in permutations(goals):
        current_pos = start
        total_distance = 0
        valid = True
        
        # Calculate total distance for this ordering
        for goal in goal_order:
            distance = find_path_length(maze, current_pos, goal)
            if distance == float('inf'):
                valid = False
                break
            total_distance += distance
            current_pos = goal
        
        if valid and total_distance < best_distance:
            best_distance = total_distance
            best_order = goal_order
    
    if best_order is None:
        print("Cannot reach all goals!")
        return None
    
    # Build the actual path using best order
    current_pos = start
    complete_path = [start]
    
    print(f"Best order: {best_order}")
    for goal in best_order:
        path_segment = best_first_search(maze, current_pos, goal)
        complete_path.extend(path_segment[1:])
        print(f"Visited goal {goal}, distance: {len(path_segment) - 1}")
        current_pos = goal
    
    print(f"Total distance: {best_distance}")
    return complete_path


def visualize_path(maze, path, goals, start):
    """Display the maze with the path"""
    visual = []
    for i, row in enumerate(maze):
        visual_row = []
        for j, cell in enumerate(row):
            pos = (i, j)
            if pos == start:
                visual_row.append('S')
            elif pos in goals:
                visual_row.append('G')
            elif pos in path:
                visual_row.append('*')
            elif cell == 1:
                visual_row.append('█')
            else:
                visual_row.append('.')
        visual.append(visual_row)
    
    for row in visual:
        print(' '.join(row))
    print("\nLegend: S=Start, G=Goal, *=Path, █=Wall, .=Empty")


# Example maze with dead ends
maze = [
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goals = [(2, 6), (4, 2), (6, 6)]  # Three goal points

print("="*60)
print("MULTI-GOAL MAZE NAVIGATION")
print("="*60)
print(f"\nStart: {start}")
print(f"Goals: {goals}")
print(f"Number of goals: {len(goals)}")

# Try greedy approach
greedy_path = multi_goal_search_greedy(maze, start, goals)

if greedy_path:
    print("\n--- Greedy Path Visualization ---")
    visualize_path(maze, greedy_path, goals, start)
    print(f"Path length: {len(greedy_path)} steps")

# Try optimal approach
optimal_path = multi_goal_search_optimal(maze, start, goals)

if optimal_path:
    print("\n--- Optimal Path Visualization ---")
    visualize_path(maze, optimal_path, goals, start)
    print(f"Path length: {len(optimal_path)} steps")

# Compare results
if greedy_path and optimal_path:
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)
    print(f"Greedy path length: {len(greedy_path)} steps")
    print(f"Optimal path length: {len(optimal_path)} steps")
    difference = len(greedy_path) - len(optimal_path)
    if difference > 0:
        print(f"Optimal is {difference} steps shorter!")
    elif difference < 0:
        print(f"Greedy found a better path by {-difference} steps!")
    else:
        print("Both approaches found the same path!")
