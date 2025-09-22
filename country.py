import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon
import sys
import os

SHAPEFILE_PATH = r"F:/python_code/map_app/data/ne_110m_admin_0_countries.shp"
OUTPUT_DIR = r"F:/python_code/map_app/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_country_geometry(country_name):
    world = gpd.read_file(SHAPEFILE_PATH)
    row = world[world['NAME'].str.lower() == country_name.lower()]
    if row.empty:
        raise ValueError(f"Country '{country_name}' not found")
    geom = row.geometry.values[0]
    if geom.geom_type == "MultiPolygon":
        geom = max(geom, key=lambda p: p.area)
    return geom

def plot_mathematical_map(geom, country_name):
    # Project to UTM for accurate distances
    geom_proj = gpd.GeoSeries([geom], crs="EPSG:4326").to_crs("EPSG:32646")  # Bangladesh UTM 46N
    
    fig, ax = plt.subplots(figsize=(10, 10))
    geom_proj.plot(ax=ax, color="#FFCC33", edgecolor="#000000")
    
    ax.set_aspect('equal')  # important for math accuracy
    ax.set_axis_off()
    
    out_path = os.path.join(OUTPUT_DIR, f"{country_name.replace(' ','_')}_math.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved mathematically accurate map: {out_path}")
    return out_path

if __name__ == "__main__":
    country = sys.argv[1] if len(sys.argv) > 1 else input("Enter country name: ")
    geom = get_country_geometry(country)
    plot_mathematical_map(geom, country)
