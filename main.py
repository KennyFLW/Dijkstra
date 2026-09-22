import osmnx as ox
import folium
import heapq


def dijkstra(G, source, target):
    
    dist = {source : 0}
    parent = {source: None}
    visited = set()
    pq = [(0, source)]
    
    while pq:
        distance, currentEdges = heapq.heappop(pq)
        if currentEdges in visited:
            continue
        visited.add(currentEdges)
        if currentEdges == target:
            break

        for nextEdges in G.neighbors(currentEdges):
            if nextEdges in visited:
                continue
            length = G[currentEdges][nextEdges][0]["length"]
            newDistance = distance + length
            if newDistance < dist.get(nextEdges, float("inf")):
                dist[nextEdges] = newDistance
                parent[nextEdges] = currentEdges
                heapq.heappush(pq, (newDistance, nextEdges))

    if target not in parent:
        return None, float("inf")
    
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, dist[target]




G = ox.graph_from_point((10.8494, 106.7537), dist=6000, network_type="drive") 
start = ox.distance.nearest_nodes(G, X=106.814846, Y=10.880772) 
end   = ox.distance.nearest_nodes(G, X=106.771666, Y=10.849877)  
path, total = dijkstra(G, start, end)
print("Quãng đường:", round(total), "mét,", len(path), "đỉnh")


m = folium.Map(location=[10.8494, 106.7537], zoom_start=15,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri")


route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in path]
folium.Marker(route_coords[0], icon=folium.Icon(color="green")).add_to(m)
folium.Marker(route_coords[-1], icon=folium.Icon(color="red")).add_to(m)
folium.PolyLine(route_coords, color="#1a73e8", weight=6).add_to(m)


m.save("map_sample.html")   # xuất ra file HTML