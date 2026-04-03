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


def bfs(tree, start, goal):
    stack = []
    visited=[]

    stack.append(start)
    visited.append(start)

    while stack:

        current = stack.pop()
        print("Visiting: ", current)

        if current == goal:
            print("Goal Reached")
            return
        
        for neighbour in reversed(tree[current]):
            if neighbour not in visited:
                visited.append(neighbour)
                stack.append(neighbour)


bfs(tree, 'A', 'I')
    
            
        



