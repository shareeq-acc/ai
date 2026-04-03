maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

path = [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4), (4, 4)]

print("Maze (0 = walkable, 1 = wall):")
for i, row in enumerate(maze):
    print(f"Row {i}: {row}")

print("\n" + "="*50)
print("Verifying path step by step:")
print("="*50)

for i, pos in enumerate(path):
    row, col = pos
    cell_value = maze[row][col]
    
    if cell_value == 1:
        print(f"❌ Step {i}: {pos} - INVALID! This is a wall (value = 1)")
    else:
        print(f"✓ Step {i}: {pos} - Valid (value = {cell_value})")
    
    # Check if move is adjacent to previous position
    if i > 0:
        prev_row, prev_col = path[i-1]
        row_diff = abs(row - prev_row)
        col_diff = abs(col - prev_col)
        
        if row_diff + col_diff != 1:
            print(f"  ⚠️  WARNING: Not adjacent to previous position!")
        elif row_diff == 1 and col_diff == 0:
            direction = "down" if row > prev_row else "up"
            print(f"  → Moved {direction}")
        elif col_diff == 1 and row_diff == 0:
            direction = "right" if col > prev_col else "left"
            print(f"  → Moved {direction}")

print("\n" + "="*50)
print("Visual representation of path:")
print("="*50)

# Create visual maze
visual = []
for i, row in enumerate(maze):
    visual_row = []
    for j, cell in enumerate(row):
        if (i, j) in path:
            idx = path.index((i, j))
            if (i, j) == (0, 0):
                visual_row.append('S')  # Start
            elif (i, j) == (4, 4):
                visual_row.append('E')  # End
            else:
                visual_row.append('*')  # Path
        elif cell == 1:
            visual_row.append('█')  # Wall
        else:
            visual_row.append('.')  # Empty
    visual.append(visual_row)

for row in visual:
    print(' '.join(row))

print("\nLegend: S=Start, E=End, *=Path, █=Wall, .=Empty")
print(f"\nPath length: {len(path)} steps")
print(f"Start: {path[0]}, End: {path[-1]}")
