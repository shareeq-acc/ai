# ============================================================
# UCS - Uniform Cost Search
# Always explores the cheapest path first
# ============================================================

graph = {
    'A': {'B': 2, 'C': 1},    # A→B costs 2, A→C costs 1
    'B': {'D': 4, 'E': 3},
    'C': {'F': 1, 'G': 5},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 6},
    'G': {},
    'H': {},
    'I': {}
}

def ucs(graph, start, goal):
    # Priority queue: [(cost, node)]
    queue = [(0, start)]
    visited = set()

    while queue:
        # Always pick the cheapest path
        queue.sort()
        cost, node = queue.pop(0)

        if node in visited:
            continue

        visited.add(node)
        print(f"Visiting: {node} (cost: {cost})")

        if node == goal:
            print(f"Goal found! Total cost: {cost}")
            return

        # Add neighbors with their total cost
        for neighbor, edge_cost in graph[node].items():
            if neighbor not in visited:
                total_cost = cost + edge_cost
                queue.append((total_cost, neighbor))

    print("Goal not found")

ucs(graph, 'A', 'I')
