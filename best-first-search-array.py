# Graph represented as dictionary (keeping original structure)
graph = {
    'S': [('A', 3), ('B', 6), ('C', 5)],
    'A': [('D', 9), ('E', 8)],
    'B': [('F', 12), ('G', 14)],
    'C': [('H', 7)],
    'H': [('I', 5), ('J', 6)],
    'I': [('K', 1), ('L', 10), ('M', 2)],
    'D': [], 'E': [],
    'F': [], 'G': [],
    'J': [], 'K': [],
    'L': [], 'M': []
}

def best_first_search(graph, start, goal):
    visited = set()
    to_explore = []  # Array instead of PriorityQueue: [(priority, node), ...]
    to_explore.append((0, start))
    
    while len(to_explore) > 0:
        # Find and remove the node with minimum priority
        min_idx = 0
        for i in range(1, len(to_explore)):
            if to_explore[i][0] < to_explore[min_idx][0]:
                min_idx = i
        
        priority, current = to_explore.pop(min_idx)
        
        if current not in visited:
            print(current, end=' ')
            visited.add(current)
            
            if current == goal:
                print("\nGoal reached!")
                return True
            
            for neighbor, edge_cost in graph[current]:
                if neighbor not in visited:
                    to_explore.append((edge_cost, neighbor))
    
    print("\nGoal not reachable!")
    return False


# Example usage:
print("Best-First Search Path (Array-based):")
best_first_search(graph, 'A', 'I')
