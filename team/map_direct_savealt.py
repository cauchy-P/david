import matplotlib.pyplot as plt
import pandas as pd
import heapq
from collections import defaultdict

# Read the CSV data into a DataFrame
df = pd.read_csv("merged_area.csv")

# Create a grid for obstacles
grid_size = 15
obstacles = set()
start = None
goals = set()  # Multiple possible goals for BandalgomCoffee

for _, row in df.iterrows():
    x = int(row['x'])
    y = int(row['y'])
    construction = row['ConstructionSite']
    category = row['category'].strip() if pd.notna(row['category']) else ''
    
    pos = (x, y)
    
    if category == 'MyHome':
        start = pos
    elif category == 'BandalgomCoffee':
        goals.add(pos)
    
    if construction == 1 or category in ['Apartment', 'Building']:
        obstacles.add(pos)

# Dijkstra Algorithm
def dijkstra(start, goals, obstacles, grid_size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left
    
    def neighbors(pos):
        x, y = pos
        return [(x+dx, y+dy) for dx, dy in directions if 1 <= x+dx <= grid_size and 1 <= y+dy <= grid_size and (x+dx, y+dy) not in obstacles]
    
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    
    open_set = []
    heapq.heappush(open_set, (0, start))  # (g_score, pos)
    
    while open_set:
        current_g, current = heapq.heappop(open_set)
        
        if current in goals:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(open_set, (tentative_g, neighbor))
    
    return None  # No path found

# Find the path
path = dijkstra(start, goals, obstacles, grid_size)

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 10))

# Set limits
ax.set_xlim(0.5, 15.5)
ax.set_ylim(15.5, 0.5)  # Invert y-axis so (1,1) is top-left, y increases downward

# Draw grid lines
ax.grid(True, which='both', linestyle='-', linewidth=1)
ax.set_xticks(range(1, 16))
ax.set_yticks(range(1, 16))

# Plot the symbols
for _, row in df.iterrows():
    x = row['x']
    y = row['y']
    construction = row['ConstructionSite']
    category = row['category'].strip() if pd.notna(row['category']) else ''

    if construction == 1:
        # Gray square for construction site
        ax.plot(x, y, marker='s', markersize=20, color='gray')
    elif category:
        if category in ['Apartment', 'Building']:
            # Brown circle
            ax.plot(x, y, marker='o', markersize=20, color='brown')
        elif category == 'BandalgomCoffee':
            # Green square
            ax.plot(x, y, marker='s', markersize=20, color='green')
        elif category == 'MyHome':
            # Green triangle
            ax.plot(x, y, marker='^', markersize=20, color='green')

# Plot the path if found
if path:
    path_x, path_y = zip(*path)
    ax.plot(path_x, path_y, color='blue', linewidth=2, marker='*', markersize=10)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

plt.savefig("map_direct_savealt.png", dpi=300)