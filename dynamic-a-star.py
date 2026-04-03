import random
import time

# Graph with initial edge costs
graph = {
    'A': {'B': 4, 'C': 3},
    'B': {'E': 12, 'F': 5},
    'C': {'D': 7, 'E': 10},
    'D': {'E': 2},
    'E': {'G': 5},
    'F': {'G': 16},
    'G': {}
}

# Heuristics (these stay constant)
heuristic = {
    'A': 14,
    'B': 12,
    'C': 11,
    'D': 6,
    'E': 4,
    'F': 11,
    'G': 0
}


def change_edge_costs(graph, change_probability=0.3):
    """Randomly change some edge costs to simulate dynamic environment"""
    changes = []
    for node in graph:
        for neighbor in list(graph[node].keys()):
            if random.random() < change_probability:
                old_cost = graph[node][neighbor]
                # Change cost by -3 to +5
                new_cost = max(1, old_cost + random.randint(-3, 5))
                graph[node][neighbor] = new_cost
                changes.append((node, neighbor, old_cost, new_cost))
    return changes


def dynamic_a_star(graph, start, goal, max_iterations=100):
    """
    A* Search that adapts to dynamic edge cost changes
    
    Key enhancements:
    1. Tracks iteration count to trigger cost changes
    2. Revalidates paths when costs change
    3. Updates costs for nodes still in queue
    4. Continues search without full restart
    """
    
    # Initialize
    to_explore = [(start, heuristic[start])]
    visited = set()
    cost = {start: 0}
    parent = {start: None}
    iteration = 0
    cost_change_interval = 3  # Change costs every N iterations
    
    print(f"Starting A* from {start} to {goal}")
    print("="*60)
    
    while to_explore and iteration < max_iterations:
        iteration += 1
        
        # Simulate dynamic cost changes at intervals
        if iteration % cost_change_interval == 0:
            print(f"\n⚡ ITERATION {iteration}: Edge costs changing!")
            changes = change_edge_costs(graph, change_probability=0.3)
            
            if changes:
                print("Changes detected:")
                for node, neighbor, old, new in changes:
                    print(f"  {node}→{neighbor}: {old} → {new}")
                
                # ENHANCEMENT 1: Revalidate costs for nodes in queue
                updated_queue = []
                for node, old_f in to_explore:
                    if node in cost:
                        # Recalculate f-score with current costs
                        new_f = cost[node] + heuristic[node]
                        updated_queue.append((node, new_f))
                    else:
                        updated_queue.append((node, old_f))
                to_explore = updated_queue
                
                # ENHANCEMENT 2: Check if visited nodes need reconsideration
                # If a path to a visited node becomes cheaper, remove from visited
                nodes_to_reconsider = set()
                for node in visited:
                    for neighbor, edge_cost in graph[node].items():
                        if neighbor in cost:
                            new_cost_via_node = cost[node] + edge_cost
                            if new_cost_via_node < cost[neighbor]:
                                nodes_to_reconsider.add(neighbor)
                
                if nodes_to_reconsider:
                    print(f"  Reconsidering nodes: {nodes_to_reconsider}")
                    visited -= nodes_to_reconsider
            else:
                print("  No changes this time")
        
        # Sort by f-score
        to_explore.sort(key=lambda x: x[1])
        
        # Get best node
        current, score = to_explore.pop(0)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Goal reached!
        if current == goal:
            print(f"\n✓ Goal reached at iteration {iteration}!")
            
            # Reconstruct path
            path = []
            node = current
            total_cost = cost[current]
            
            while node:
                path.append(node)
                node = parent[node]
            
            path.reverse()
            print(f"Path: {' → '.join(path)}")
            print(f"Total cost: {total_cost}")
            return path, total_cost
        
        # Explore neighbors
        for neighbor, edge_cost in graph[current].items():
            new_cost = cost[current] + edge_cost
            total_score = new_cost + heuristic[neighbor]
            
            # ENHANCEMENT 3: Always update if we found a better path
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                
                # Remove old entry if exists and add new one
                to_explore = [(n, f) for n, f in to_explore if n != neighbor]
                to_explore.append((neighbor, total_score))
                
                # If neighbor was visited but we found better path, reconsider it
                if neighbor in visited and new_cost < cost.get(neighbor, float('inf')):
                    visited.remove(neighbor)
    
    print(f"\n✗ No path found after {iteration} iterations")
    return None, None


def compare_static_vs_dynamic():
    """Compare static A* with dynamic A*"""
    print("\n" + "="*60)
    print("COMPARISON: Static vs Dynamic A*")
    print("="*60)
    
    # Reset graph to original costs
    graph_static = {
        'A': {'B': 4, 'C': 3},
        'B': {'E': 12, 'F': 5},
        'C': {'D': 7, 'E': 10},
        'D': {'E': 2},
        'E': {'G': 5},
        'F': {'G': 16},
        'G': {}
    }
    
    # Run static A* (no cost changes)
    print("\n--- Static A* (no cost changes) ---")
    to_explore = [('A', heuristic['A'])]
    visited = set()
    cost = {'A': 0}
    parent = {'A': None}
    
    while to_explore:
        to_explore.sort(key=lambda x: x[1])
        current, _ = to_explore.pop(0)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == 'G':
            path = []
            node = current
            while node:
                path.append(node)
                node = parent[node]
            print(f"Path: {' → '.join(reversed(path))}")
            print(f"Cost: {cost['G']}")
            break
        
        for neighbor, edge_cost in graph_static[current].items():
            new_cost = cost[current] + edge_cost
            total_score = new_cost + heuristic[neighbor]
            
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                to_explore.append((neighbor, total_score))


# Run the dynamic A* algorithm
print("\n" + "="*60)
print("DYNAMIC A* SEARCH WITH CHANGING EDGE COSTS")
print("="*60)

random.seed(42)  # For reproducible results
path, total_cost = dynamic_a_star(graph, 'A', 'G')

# Show final graph state
print("\n" + "="*60)
print("FINAL GRAPH STATE")
print("="*60)
for node in sorted(graph.keys()):
    if graph[node]:
        print(f"{node}: {graph[node]}")

# Compare with static
compare_static_vs_dynamic()

print("\n" + "="*60)
print("KEY ENHANCEMENTS FOR DYNAMIC A*")
print("="*60)
print("""
1. Cost Change Detection: Monitors and applies edge cost changes at intervals

2. Queue Revalidation: Updates f-scores for nodes still in queue when costs change

3. Visited Node Reconsideration: Removes nodes from visited set if a cheaper 
   path becomes available after cost changes

4. Continuous Adaptation: Algorithm continues without restart, adapting to 
   new costs on-the-fly

5. Better Path Updates: Always updates if a cheaper path is found, even for 
   previously visited nodes
""")
