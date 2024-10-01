import networkx as nx
import requests
import folium

# Fetch Elevation Data from OpenElevation API (optional)
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()['results'][0]['elevation']
        else:
            print(f"Elevation API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve elevation data: {e}")
        return None

# Create Graph with or without Elevation
def create_graph(target_coords, base_coords):
    G = nx.Graph()
    
    # Try to fetch elevation data, but proceed without it if not available
    target_elevation = get_elevation(*target_coords)
    base_elevation = get_elevation(*base_coords)

    if target_elevation is None:
        target_elevation = 0  # Default elevation if not available
    if base_elevation is None:
        base_elevation = 0  # Default elevation if not available

    # Add nodes with elevation data or without
    G.add_node('target', pos=target_coords, elevation=target_elevation)
    G.add_node('base', pos=base_coords, elevation=base_elevation)

    # Add edge with weight based on distance and elevation difference (if available)
    G.add_edge('target', 'base', weight=calculate_weight(G, 'target', 'base'))

    return G

# Calculate weight based on distance and elevation (if available)
def calculate_weight(G, node1, node2):
    lat1, lon1 = G.nodes[node1]['pos']
    lat2, lon2 = G.nodes[node2]['pos']
    elevation_diff = abs(G.nodes[node1]['elevation'] - G.nodes[node2]['elevation'])
    distance = ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
    return distance + elevation_diff / 100  # Reduced impact of elevation difference

# Find the shortest path based on graph
def find_shortest_path(G):
    if 'target' in G.nodes and 'base' in G.nodes:
        return nx.dijkstra_path(G, 'target', 'base', weight='weight')
    else:
        raise nx.NodeNotFound("Either 'target' or 'base' node is missing from the graph.")

# Display Path on the Folium Map
def display_path(G, path):
    path_coords = [G.nodes[node]['pos'] for node in path]
    map_center = path_coords[0]
    folium_map = folium.Map(location=map_center, zoom_start=12)

    # Add the polyline for the path
    folium.PolyLine(path_coords, color="blue", weight=2.5).add_to(folium_map)

    # Add markers with custom icons
    target_icon = folium.CustomIcon('https://cdn-icons-png.flaticon.com/128/13169/13169618.png', icon_size=(35, 45))
    base_icon = folium.CustomIcon('https://cdn-icons-png.flaticon.com/128/2181/2181353.png', icon_size=(35, 45))

    # Add the "Target" marker
    folium.Marker(
        location=path_coords[0],
        popup="Target",
        icon=target_icon
    ).add_to(folium_map)

    # Add the "Base" marker
    folium.Marker(
        location=path_coords[-1],
        popup="Base",
        icon=base_icon
    ).add_to(folium_map)

    # Save the map to an HTML file
    folium_map.save("tracking_map.html")
    print("Map saved as tracking_map.html")

# Main function to run pathfinding
def main(target_coords, base_coords):
    try:
        G = create_graph(target_coords, base_coords)
        path = find_shortest_path(G)
        display_path(G, path)
        return path
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    # Example target (manual coordinates) and base (drone coordinates)
    target_coords = (29.39, 79.46)  # Target coordinates
    base_coords = (29.60, 79.60)    # Base coordinates
    main(target_coords, base_coords)







