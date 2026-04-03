# Graph — each node maps to its neighbours and the EDGE COST to reach them
graph = {
    'A': {'B': 4, 'C': 3},   # from A: go to B costs 4, go to C costs 3
    'B': {'E': 12, 'F': 5},  # from B: go to E costs 12, go to F costs 5
    'C': {'D': 7, 'E': 10},  # from C: go to D costs 7, go to E costs 10
    'D': {'E': 2},            # from D: go to E costs 2
    'E': {'G': 5},            # from E: go to G costs 5
    'F': {'G': 16},           # from F: go to G costs 16
    'G': {}                   # G is the goal, no outgoing edges
}

# Heuristics — estimated cost from each node TO the goal (G)
# These are given to you, not calculated — they are guesses/estimates
heuristic = {
    'A': 14,   # A is estimated 14 away from G
    'B': 12,
    'C': 11,
    'D': 6,
    'E': 4,    # E is very close to G
    'F': 11,
    'G': 0     # G is the goal — distance to itself is always 0
}


def a_star(graph, start, goal):
    # Nodes to explore
    to_explore = [(start, heuristic[start])]
    
    # Nodes already visited
    visited = set()
    
    # Cost to reach each node
    cost = {start: 0}
    
    # Track where we came from
    parent = {start: None}

    while to_explore:
        # Sort to get best node
        to_explore.sort(key=lambda x: x[1])
        
        # Get best node
        current, score = to_explore.pop(0)
        
        # Skip if already visited
        if current in visited:
            continue
        
        # Mark as visited
        visited.add(current)
        
        # Found goal! Build path
        if current == goal:
            path = []
            node = current
            while node:
                path.append(node)
                node = parent[node]
            print("Path:", list(reversed(path)))
            return
        
        # Check all neighbors
        for neighbor, edge_cost in graph[current].items():
            # Cost to reach neighbor
            new_cost = cost[current] + edge_cost
            
            # Total score: actual cost + estimated remaining
            total_score = new_cost + heuristic[neighbor]
            
            # Update if better path found
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                to_explore.append((neighbor, total_score))


# Run the A* algorithm from A to G
a_star(graph, 'A', 'G')
