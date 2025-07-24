import pandas as pd

# 1. Load CSV files
area_map = pd.read_csv('area_map.csv')
area_struct = pd.read_csv('area_struct.csv')
area_category = pd.read_csv('area_category.csv')

# 2. Print loaded data for inspection
print("=== area_map Data ===")
print(area_map)
print("\n=== area_struct Data ===")
print(area_struct)
print("\n=== area_category Data ===")
print(area_category)

mapping = area_category.set_index("category")[" struct"]     
area_struct["category"] = area_struct["category"].map(mapping).fillna("")
print(area_struct)

area_merged = pd.merge(area_map, area_struct, on=["x","y"], how="left")

print("\n=== Merged Area Data ===")

print(area_merged)

area_merged.to_csv("merged_area.csv", index=False)

area_filtered = area_merged.query("area == 1")

print("\n=== Filtered Area Data ===")
print(area_filtered)


area_filtered.to_csv("filtered_area.csv", index=False)
