tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}


def dls(tree, start, goal, depth_limit):
    stack = []
    visited = []

    stack.append((start, 0))  # Store (node, depth)
    visited.append(start)

    while stack:
        current, depth = stack.pop()  # Unpack node and depth
        print(f"Visiting: {current} at depth {depth}")

        if current == goal:
            print("Goal Reached")
            return
        
        if depth < depth_limit:  # Only explore if within depth limit
            for neighbour in reversed(tree[current]):
                if neighbour not in visited:
                    visited.append(neighbour)
                    stack.append((neighbour, depth + 1))  # Increment depth
    
    print("Goal not found within depth limit")


dls(tree, 'A', 'I', depth_limit=3)
