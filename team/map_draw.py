import matplotlib.pyplot as plt
import pandas as pd

#
# Read the CSV data into a DataFrame
df = pd.read_csv("merged_area.csv")

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

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

plt.savefig("map_draw1.png", dpi=300)