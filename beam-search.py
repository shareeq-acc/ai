import heapq

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


def beam_search(graph, start, goal, beam_width=2):
    """
    Beam Search: Explores multiple paths in parallel but only keeps
    the best 'beam_width' paths at each step.
    
    Parameters:
    - graph: adjacency list with edge costs
    - start: starting node
    - goal: goal node
    - beam_width: number of best paths to keep at each level
    
    Returns:
    - path: list of nodes from start to goal
    - total_cost: cumulative cost of the path
    """
    
    # Initialize beam with start node
    # Each entry: (cumulative_cost, path)
    current_beam = [(0, [start])]
    
    print(f"Starting Beam Search from {start} to {goal}")
    print(f"Beam width: {beam_width}")
    print("="*60)
    
    level = 0
    
    while current_beam:
        level += 1
        print(f"\nLevel {level}:")
        print(f"Current beam: {[(cost, path) for cost, path in current_beam]}")
        
        next_candidates = []
        
        # Expand each path in the current beam
        for cumulative_cost, path in current_beam:
            current_node = path[-1]
            
            # Check if goal reached
            if current_node == goal:
                print(f"\n✓ Goal reached!")
                return path, cumulative_cost
            
            # Generate all successors
            neighbors = graph.get(current_node, [])
            print(f"  Expanding {current_node}: neighbors = {neighbors}")
            
            for neighbor, edge_cost in neighbors:
                new_cost = cumulative_cost + edge_cost
                new_path = path + [neighbor]
                next_candidates.append((new_cost, new_path))
                print(f"    → {neighbor}: cost = {new_cost}, path = {new_path}")
        
        if not next_candidates:
            print("\n✗ No more candidates to explore")
            break
        
        # Select top beam_width paths with lowest cost
        current_beam = heapq.nsmallest(beam_width, next_candidates, key=lambda x: x[0])
        
        print(f"\n  Selected top {beam_width} paths:")
        for cost, path in current_beam:
            print(f"    Cost {cost}: {' → '.join(path)}")
    
    print("\n✗ No path found to goal")
    return None, float('inf')


def verify_beam_search():
    """Test beam search with different beam widths"""
    
    print("\n" + "="*60)
    print("BEAM SEARCH VERIFICATION")
    print("="*60)
    
    start = 'S'
    goal = 'L'
    
    # Test with different beam widths
    for width in [1, 2, 3, 5]:
        print("\n" + "="*60)
        print(f"Testing with beam width = {width}")
        print("="*60)
        
        path, cost = beam_search(graph, start, goal, beam_width=width)
        
        if path:
            print(f"\n✓ Path found: {' → '.join(path)}")
            print(f"  Total cost: {cost}")
            
            # Verify the path
            print(f"\n  Verification:")
            total = 0
            for i in range(len(path) - 1):
                current = path[i]
                next_node = path[i + 1]
                
                # Find edge cost
                edge_found = False
                for neighbor, edge_cost in graph.get(current, []):
                    if neighbor == next_node:
                        total += edge_cost
                        print(f"    {current} → {next_node}: cost = {edge_cost}")
                        edge_found = True
                        break
                
                if not edge_found:
                    print(f"    ✗ ERROR: No edge from {current} to {next_node}")
            
            print(f"  Verified total cost: {total}")
            
            if total == cost:
                print(f"  ✓ Cost matches!")
            else:
                print(f"  ✗ Cost mismatch!")
        else:
            print(f"\n✗ No path found with beam width {width}")


# Run the main example
print("\n" + "="*60)
print("BEAM SEARCH EXAMPLE")
print("="*60)

start_node = 'S'
goal_node = 'L'
beam_width = 3

path, cost = beam_search(graph, start_node, goal_node, beam_width=beam_width)

if path:
    print(f"\n{'='*60}")
    print(f"FINAL RESULT")
    print(f"{'='*60}")
    print(f"Path: {' → '.join(path)}")
    print(f"Total cost: {cost}")
else:
    print("\nNo path found.")

# Run verification with different beam widths
verify_beam_search()

# Explanation
print("\n" + "="*60)
print("KEY CONCEPTS")
print("="*60)
print("""
1. Beam Width: Limits how many paths are kept at each level
   - Smaller width = faster but may miss optimal path
   - Larger width = more thorough but slower

2. Greedy Selection: At each level, only keeps the beam_width
   paths with lowest cumulative cost

3. Pruning: Paths not in top-k are permanently discarded

4. No Backtracking: Once a path is pruned, it's never reconsidered

5. Trade-off: Beam search balances between breadth-first search
   (explores everything) and greedy search (explores only one path)
""")
