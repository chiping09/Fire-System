import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, node_pos, edge_colors, start=None, end=None, passed=None):
    plt.figure(figsize=(8, 6))
    plt.title('Nakhon Nayok Fire Station')

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

# เพิ่มเส้นเชื่อมพร้อมกำหนดระยะทาง (เป็นหน่วยกิโลเมตร)
network.add_edge('Station 1', 'Station 2', weight=4.1)

network.add_edge('Station 1', 'ChokNamChai', weight=1)
network.add_edge('ChokNamChai', 'PT4', weight=1)
network.add_edge('PT4', 'PT5', weight=1)
network.add_edge('ChokNamChai', 'Shell1', weight=1)
network.add_edge('Shell1', 'PT-LPG2', weight=1)

network.add_edge('Station 1', 'PTT4', weight=4)

network.add_edge('Station 1', 'Bangchak', weight=4)
network.add_edge('Bangchak', 'Esso3', weight=4)
network.add_edge('Esso3', 'PTT3', weight=4)
network.add_edge('PTT3', 'PT-LPG1', weight=4)
network.add_edge('PT-LPG1', 'PT1', weight=4)
network.add_edge('PT1', 'LPG1', weight=4)
network.add_edge('LPG1', 'PT2', weight=4)
network.add_edge('PT2', 'PT3', weight=4)

network.add_edge('Station 2', 'Esso1', weight=2)
network.add_edge('Station 2', 'PTT1', weight=5)
network.add_edge('PTT1', 'Esso2', weight=2)
network.add_edge('Esso2', 'PTT2', weight=2)


# กำหนดตำแหน่งของโหนด
node_pos = {'Station 1': (2, 0),  
            'ChokNamChai': (3.5, -2.5),
              'PT4': (8, 1), 'PT5': (9, 2),
              'Shell1': (6, -5), 'PT-LPG2': (8, -6),
            'PTT4': (9, 9),
            'Bangchak': (1, -0.5), 'Esso3': (0.5, -1), 'PTT3': (-1, -1.5), 'PT-LPG1': (-3, -2), 'PT1': (-6, -2), 'LPG1': (-8, -0.5), 'PT2': (-9, 0),'PT3': (-9.5, 0.5),  

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
