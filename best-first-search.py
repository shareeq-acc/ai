from queue import PriorityQueue

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
    to_explore = PriorityQueue()
    to_explore.put((0, start))  # (priority, node)
    
    while not to_explore.empty():
        priority, current = to_explore.get()
        
        if current not in visited:
            print(current, end=' ')
            visited.add(current)
            
            if current == goal:
                print("\nGoal reached!")
                return True
            
            for neighbor, edge_cost in graph[current]:
                if neighbor not in visited:
                    to_explore.put((edge_cost, neighbor))
    
    print("\nGoal not reachable!")
    return False


# Example usage:
print("Best-First Search Path:")
best_first_search(graph, 'A', 'I')