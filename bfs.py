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
    queue = []
    visited=[]

    queue.append(start)
    visited.append(start)

    while queue:

        current = queue.pop(0)
        print("Visiting: ", current)

        if current == goal:
            print("Goal Reached")
            return
        
        for neighbour in tree[current]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

bfs(tree, 'A', 'I')
    
            
        

