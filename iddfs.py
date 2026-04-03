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
    stack = [(start, 0)]
    visited = []

    while stack:
        current, depth = stack.pop()
        
        if current not in visited:
            visited.append(current)
            print(f"  Visiting: {current} at depth {depth}")

            if current == goal:
                return True
            
            if depth < depth_limit:
                for neighbour in reversed(tree[current]):
                    if neighbour not in visited:
                        stack.append((neighbour, depth + 1))
    
    return False


def iddfs(tree, start, goal, max_depth):
    for depth in range(max_depth + 1):
        print(f"\nTrying depth limit: {depth}")
        if dls(tree, start, goal, depth):
            print("Goal found!")
            return
    
    print("Goal not found within max depth")


iddfs(tree, 'A', 'I', max_depth=5)



