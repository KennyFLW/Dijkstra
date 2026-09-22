import tkinter as tk
import tkintermapview
import osmnx as ox
import heapq

# ---------- DIJKSTRA (ghi lại các CẠNH duyệt qua để animate) ----------
def dijkstra(G, source, target):
    dist = {source: 0}
    parent = {source: None}
    visited = set()
    pq = [(0, source)]
    explored_edges = []              # các cạnh (cha -> đỉnh) theo thứ tự duyệt

    while pq:
        distance, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        # ghi lại cạnh từ cha tới đỉnh này
        if parent[current] is not None:
            p = parent[current]
            explored_edges.append((
                (G.nodes[p]["y"], G.nodes[p]["x"]),
                (G.nodes[current]["y"], G.nodes[current]["x"])
            ))
        if current == target:
            break
        for nxt in G.neighbors(current):
            if nxt in visited:
                continue
            length = G[current][nxt][0]["length"]
            nd = distance + length
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                parent[nxt] = current
                heapq.heappush(pq, (nd, nxt))

    if target not in parent:
        return None, float("inf"), explored_edges

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, dist[target], explored_edges

# ---------- TẢI ĐỒ THỊ ----------
print("Đang tải bản đồ...")
G = ox.graph_from_point((10.8494, 106.7537), dist=3000, network_type="drive")
print("Xong:", G.number_of_nodes(), "đỉnh")

# ---------- BIẾN TRẠNG THÁI ----------
points = []
markers = []
route_path = [None]
explore_lines = []      # các nét minh họa quá trình duyệt
last_result = [None]    # lưu (path, total, edges) của lần tìm gần nhất

# ---------- BẤM CHUỘT CHỌN ĐIỂM ----------
def on_click(coords):
    lat, lon = coords
    if len(points) >= 2:
        return
    color = "green" if len(points) == 0 else "red"
    text = "Điểm đầu" if len(points) == 0 else "Điểm đích"
    marker = map_widget.set_marker(lat, lon, text=text, marker_color_circle=color)
    markers.append(marker)
    points.append((lat, lon))
    if len(points) == 2:
        tim_duong()

# ---------- TÌM ĐƯỜNG ----------
def tim_duong():
    start = ox.distance.nearest_nodes(G, X=points[0][1], Y=points[0][0])
    end   = ox.distance.nearest_nodes(G, X=points[1][1], Y=points[1][0])
    path, total, edges = dijkstra(G, start, end)
    last_result[0] = (path, total, edges)
    if path is None:
        label.configure(text="Không tìm được đường!")
        return
    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in path]
    route_path[0] = map_widget.set_path(coords, color="blue", width=5)
    label.configure(text=f"Quãng đường: {round(total)} mét — {len(path)} đỉnh")

# ---------- ANIMATE: vẽ dần các con đường đã duyệt ----------
def xem_thuat_toan():
    if last_result[0] is None:
        label.configure(text="Hãy chọn 2 điểm trước!")
        return
    path, total, edges = last_result[0]
    # xóa tuyến cũ và các nét cũ
    if route_path[0]:
        route_path[0].delete()
        route_path[0] = None
    for ln in explore_lines:
        ln.delete()
    explore_lines.clear()

    btn_anim.configure(state="disabled")

    step = [0]
    BATCH = 20    # mỗi khung vẽ thêm 20 đoạn đường
    def animate():
        i = step[0]
        for k in range(i, min(i + BATCH, len(edges))):
            p1, p2 = edges[k]
            line = map_widget.set_path([p1, p2], color="#ff8c00", width=2)  # nét cam mảnh
            explore_lines.append(line)
        step[0] += BATCH
        label.configure(text=f"Đang duyệt... {min(step[0], len(edges))}/{len(edges)} đoạn")
        if step[0] < len(edges):
            root.after(30, animate)      # 30 ms mỗi khung
        else:
            coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in path]
            route_path[0] = map_widget.set_path(coords, color="blue", width=5)
            label.configure(text=f"Xong! Quãng đường: {round(total)} m — duyệt {len(edges)} đoạn")
            btn_anim.configure(state="normal")
    animate()

# ---------- XÓA ----------
def xoa():
    for mk in markers:
        mk.delete()
    markers.clear()
    points.clear()
    for ln in explore_lines:
        ln.delete()
    explore_lines.clear()
    if route_path[0]:
        route_path[0].delete()
        route_path[0] = None
    last_result[0] = None
    label.configure(text="Bấm 2 điểm trên bản đồ.")

# ---------- GIAO DIỆN ----------
root = tk.Tk()
root.title("Tìm đường ngắn nhất - Dijkstra")
root.geometry("900x680")

label = tk.Label(root, text="Bấm 2 điểm trên bản đồ (đầu = xanh, đích = đỏ).", font=("Arial", 12))
label.pack(pady=6)

frame = tk.Frame(root)
frame.pack(pady=2)
tk.Button(frame, text="Xóa / Chọn lại", command=xoa).pack(side="left", padx=5)
btn_anim = tk.Button(frame, text="▶ Xem thuật toán chạy", command=xem_thuat_toan)
btn_anim.pack(side="left", padx=5)

map_widget = tkintermapview.TkinterMapView(root, width=880, height=560)
map_widget.pack(fill="both", expand=True)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}", max_zoom=22)
map_widget.set_position(10.8494, 106.7537)
map_widget.set_zoom(14)
map_widget.add_left_click_map_command(on_click)

root.mainloop()