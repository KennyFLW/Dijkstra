import osmnx as ox

G = ox.graph_from_point((10.8494, 106.7537), dist=2000, network_type="drive")  # radius 2km

# Print the graph size
print("Nodes:", G.number_of_nodes(), "\nEdges:", G.number_of_edges())

# Plot and save the road-network graph as an image
ox.plot_graph(G, save=True, filepath="map.png", show=False, close=True)



