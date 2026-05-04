# ================================
# AVIVA CASE STUDY - DATA PREP
# Person 1: End-to-End Pipeline
# ================================

import pandas as pd
import geopandas as gpd
import networkx as nx
import numpy as np
from scipy.spatial import KDTree
import pickle
from shapely.geometry import LineString

# ================================
# CONFIG
# ================================

REPAIRERS_PATH = "Repairers.csv"
POSTCODES_PATH = "Ukpostcodes.csv"
ROADS_PATH = "roads.shp"   # <- update path to shapefile

# ================================
# STEP 1 — LOAD DATA
# ================================

def load_data():
    print("Loading datasets...")
    
    repairers = pd.read_csv(REPAIRERS_PATH)
    postcodes = pd.read_csv(POSTCODES_PATH)
    
    roads = gpd.read_file(ROADS_PATH)
    
    return repairers, postcodes, roads


# ================================
# STEP 2 — CLEAN REPAIRERS
# ================================

def clean_repairers(df):
    print("Cleaning repairers...")
    
    df = df.dropna(subset=["Latitude", "Longitude"])
    df = df.drop_duplicates(subset=["Id"])
    
    return df


# ================================
# STEP 3 — CLEAN POSTCODES
# ================================

def clean_postcodes(df):
    print("Cleaning postcodes...")
    
    df = df[["postcode", "latitude", "longitude"]]
    
    df = df.dropna()
    
    df["postcode"] = df["postcode"].str.strip().str.upper()
    
    # Remove Northern Ireland (BT)
    df = df[~df["postcode"].str.startswith("BT")]
    
    return df


# ================================
# STEP 4 — POSTCODE LOOKUP
# ================================

def build_postcode_lookup(postcodes_df):
    print("Building postcode lookup...")
    
    postcode_dict = {
        row["postcode"]: (row["latitude"], row["longitude"])
        for _, row in postcodes_df.iterrows()
    }
    
    return postcode_dict


def get_coordinates(postcode, postcode_dict):
    postcode = postcode.strip().upper()
    return postcode_dict.get(postcode, None)


# ================================
# STEP 5 — BUILD GRAPH
# ================================

def build_graph(roads_gdf):
    if roads_gdf is None:
        print("⚠️ No roads data — skipping graph")
        return None
    print("Building road network graph...")
    
    G = nx.Graph()
    
    for _, row in roads_gdf.iterrows():
        geom = row.geometry
        
        if isinstance(geom, LineString):
            coords = list(geom.coords)
            
            for i in range(len(coords) - 1):
                start = coords[i]
                end = coords[i + 1]
                
                distance = np.linalg.norm(np.array(start) - np.array(end))
                
                G.add_edge(start, end, weight=distance)
    
    print(f"Graph built: {len(G.nodes)} nodes, {len(G.edges)} edges")
    
    return G


# ================================
# STEP 6 — BUILD KD-TREE
# ================================

def build_kdtree(G):
    if G is None:
        return None, None
    print("Building KDTree...")
    
    nodes = np.array(list(G.nodes))
    tree = KDTree(nodes)
    
    return tree, nodes

def get_nearest_node(point, tree, nodes):
    distance, index = tree.query(point)
    return tuple(nodes[index])


# ================================
# STEP 7 — SNAP REPAIRERS
# ================================

def snap_repairers(repairers_df, tree, nodes):
    print("Snapping repairers to graph...")
    
    def snap(row):
        point = (row["Longitude"], row["Latitude"])
        return get_nearest_node(point, tree, nodes)
    
    repairers_df["nearest_node"] = repairers_df.apply(snap, axis=1)
    
    return repairers_df


# ================================
# STEP 8 — SAVE OUTPUTS
# ================================

def save_outputs(repairers_df, postcodes_df, graph, postcode_dict):
    print("Saving outputs...")
    
    repairers_df.to_csv("clean_repairers.csv", index=False)
    postcodes_df.to_csv("clean_postcodes.csv", index=False)
    
    with open("road_graph.pkl", "wb") as f:
        pickle.dump(graph, f)
    
    with open("postcode_lookup.pkl", "wb") as f:
        pickle.dump(postcode_dict, f)
    
    print("All outputs saved.")

# ================================
# MAIN PIPELINE 
# ================================
def main():
    
    # Load
    repairers, postcodes, roads = load_data()
    
    # Clean
    repairers = clean_repairers(repairers)
    postcodes = clean_postcodes(postcodes)
    
    # Lookup
    postcode_dict = build_postcode_lookup(postcodes)
    
    # Graph
    G = build_graph(roads)
    
    # KDTree
    tree, nodes = build_kdtree(G)
    
    # Snap repairers
    repairers = snap_repairers(repairers, tree, nodes)
    
    # Save
    save_outputs(repairers, postcodes, G, postcode_dict)
    
    print("Pipeline completed successfully!")


# ================================
# RUN
# ================================

if __name__ == "__main__":
    main()