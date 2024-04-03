import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, node_pos, edge_colors, start=None, end=None, passed=None):
    plt.figure(figsize=(8, 6))
    plt.title('Fire Station')

    # วาดกราฟของเส้นทาง
    nx.draw(graph, pos=node_pos, with_labels=True, node_color='skyblue', edge_color=edge_colors, width=2)

    # ตั้งเน้นโหนดที่เป็นจุดเริ่มต้นและจุดสิ้นสุด
    if start:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=[start], node_color='red', node_size=1000)
    if end:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=[end], node_color='red', node_size=1000)

    # กำหนดโหนดที่ผ่านเป็นสีเขียว
    if passed:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=passed, node_color='lime', node_size=300)

    plt.show()

def set_start_end_nodes(graph):
    # รับค่าจุดที่เกิดเหตุไฟไหม้
    end = input("โปรดระบุโหนดที่เกิดเหตุไฟไหม้: ")

    # หาสถานีที่ใกล้ที่สุดกับจุดเกิดเหตุเพื่อเป็นจุดเริ่มต้น
    min_dist = float('inf')
    nearest_station = None
    for station in ['Station 1', 'Station 2']:
        dist = nx.shortest_path_length(graph, source=station, target=end, weight='weight')
        if dist < min_dist:
            min_dist = dist
            nearest_station = station

    return nearest_station, end

# สร้างกราฟ
network = nx.Graph()

# เพิ่มโหนด
network.add_nodes_from(['Station 1', 'Station 2', 'Esso1', 'PTT1', 'E', 'F'])

# เพิ่มเส้นเชื่อมพร้อมกำหนดระยะทาง (เป็นหน่วยกิโลเมตร)
network.add_edge('Station 1', 'Station 2', weight=4.1)

network.add_edge('Station 1', 'E', weight=1)

network.add_edge('Station 1', 'F', weight=4)

network.add_edge('Station 2', 'Esso1', weight=2)
network.add_edge('Station 2', 'PTT1', weight=5)
network.add_edge('PTT1', 'Esso2', weight=2)
network.add_edge('Esso2', 'PTT2', weight=2)


# กำหนดตำแหน่งของโหนด
node_pos = {'Station 1': (2, 0),  
            'E': (3, -3), 

            'F': (1, -0.5),  

            'Station 2': (0, 1),
            'Esso1': (0.5, 2),'PTT1': (-1, 1.5), 'Esso2': (-2, 2),'PTT2': (-3, 2.5),
           }

# แสดงเมนูเพื่อเลือกจุดต้นทางและปลายทาง
start, end = set_start_end_nodes(network)

# หาเส้นทางที่ใกล้ที่สุดโดยใช้ shortest_path
shortest_path = nx.shortest_path(network, source=start, target=end, weight='weight')

print("เส้นทางที่ใกล้ที่สุดเมื่อมีไฟไหม้:")
print(shortest_path)

# สร้างลิสต์ของสีสำหรับเส้นทาง
edge_colors = ['green' if (u, v) in zip(shortest_path[:-1], shortest_path[1:]) else 'black' for u, v in network.edges()]

# วาดกราฟ
draw_graph(network, node_pos, edge_colors, start, end, shortest_path)
