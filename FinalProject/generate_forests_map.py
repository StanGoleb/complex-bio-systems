import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from pathlib import Path
import os

def load_forest_data(input_path):
    df = pd.read_csv(input_path)
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["Longitude"], df["Latitude"]),
        crs="EPSG:4326"
    ).to_crs(epsg=3857)
    return gdf

def plot_forest_locations(gdf, output_path):
    minx, miny, maxx, maxy = gdf.total_bounds
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    width = maxx - minx
    height = maxy - miny

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(center_x - width, center_x + width)
    ax.set_ylim(center_y - height, center_y + height)

    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    gdf.plot(ax=ax, color="red", markersize=50)

    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf["Location"]):
        ax.text(x - 3000, y, label, fontsize=8, ha='right', va='center')

    ax.set_axis_off()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {output_path}")

def main():
    input_path = Path("initial_data/forest_coords.csv")
    output_path = Path("plots/forest_locations_static_map_zoomed2x.png")
    gdf = load_forest_data(input_path)
    plot_forest_locations(gdf, output_path)

if __name__ == "__main__":
    main()
