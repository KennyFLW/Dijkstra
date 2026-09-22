import osmnx as ox

# Tải mạng đường ô tô trong bán kính 1500 m quanh trung tâm Quận 1
G = ox.graph_from_point((10.8494, 106.7537), dist=1500, network_type="drive")  # bán kính 6 km quanh Thủ Đức

print("Số đỉnh:", G.number_of_nodes(), "Số cạnh:", G.number_of_edges())
ox.plot_graph(G, save=True, filepath="thuduc.png", show=False, close=True)
