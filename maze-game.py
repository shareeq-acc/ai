from queue import PriorityQueue

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.cost_from_start = 0  # actual cost from start to this node
        self.distance_to_goal = 0  # estimated distance to goal
        self.priority = 0  # priority for queue (lower = better)
    
    def __lt__(self, other):
        return self.priority < other.priority


def calculate_distance(current_pos, goal_pos):
    # Manhattan distance: sum of horizontal and vertical distance
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])


def best_first_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    goal_node = Node(goal)
    
    to_explore = PriorityQueue()
    to_explore.put(start_node)
    visited = set()
    
    while not to_explore.empty():
        current = to_explore.get()
        current_pos = current.position
        
        if current_pos == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Reverse to get start-to-goal order
        
        visited.add(current_pos)
        
        # Check all 4 directions: down, up, right, left
        for row_change, col_change in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_pos = (current_pos[0] + row_change, current_pos[1] + col_change)
            
            # Check if neighbor is valid: in bounds, walkable, not visited
            if 0 <= neighbor_pos[0] < rows and 0 <= neighbor_pos[1] < cols and maze[neighbor_pos[0]][neighbor_pos[1]] == 0 and neighbor_pos not in visited:
                neighbor = Node(neighbor_pos, current)
                neighbor.cost_from_start = current.cost_from_start + 1
                neighbor.distance_to_goal = calculate_distance(neighbor_pos, goal)
                neighbor.priority = neighbor.distance_to_goal  # Best-First: only use distance to goal
                to_explore.put(neighbor)
                visited.add(neighbor_pos)
    
    return None  # No path found


# Example maze
maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goal = (4, 4)

path = best_first_search(maze, start, goal)
if path:
    print("Path found:", path)
else:
    print("No path found")
