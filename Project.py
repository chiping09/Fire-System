import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, node_pos, edge_colors, start=None, end=None, passed=None):
    plt.figure(figsize=(8, 6))
    plt.title('Nakhon Nayok Fire Station')

    # สร้างโหนด
    nx.draw(graph, pos=node_pos, with_labels=True, node_color='skyblue', edge_color=edge_colors, width=2)

    # โหนดที่เป็นจุดเริ่มต้นและจุดสิ้นสุด
    if start:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=[start], node_color='red', node_size=600)
    if end:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=[end], node_color='red', node_size=600)

    # เส้นผ่านแต่ละโหนด
    if passed:
        nx.draw_networkx_nodes(graph, pos=node_pos, nodelist=passed, node_color='lime', node_size=300)

    plt.show()

def set_start_ends(graph, end):
    # หาสถานีที่ใกล้ที่สุดกับจุดเกิดเหตุเพื่อเป็นจุดเริ่มต้น
    min_dist = float('inf')
    nearest_station = None
    for station in ['Station 1', 'Station 2']:
        dist = nx.shortest_path_length(graph, source=station, target=end, weight='weight')
        if dist < min_dist:
            min_dist = dist
            nearest_station = station

    return nearest_station, end

def on_submit():
    plt.close()

    network = nx.Graph()

    # สร้างเส้นเชื่อมระหว่างโนหด (หน่วยกิโลเมตร)
    network.add_edge('Station 1', 'Station 2', weight=4.1)

    network.add_edge('Station 1', 'ChokNamChai', weight=1.7)
    network.add_edge('ChokNamChai', 'PT4', weight=3.7)
    network.add_edge('PT4', 'PT5', weight=0.3)
    network.add_edge('PT5', 'PTT5', weight=1.2)

    network.add_edge('ChokNamChai', 'Shell1', weight=2.5)
    network.add_edge('Shell1', 'PT-LPG2', weight=1)

    network.add_edge('Station 1', 'PTT4', weight=6.4)

    network.add_edge('Station 1', 'Bangchak', weight=1.2)
    network.add_edge('Bangchak', 'Esso3', weight=0.12)
    network.add_edge('Esso3', 'PTT3', weight=0.55)
    network.add_edge('PTT3', 'PT-LPG1', weight=0.7)
    network.add_edge('PT-LPG1', 'PT1', weight=0.85)
    network.add_edge('PT1', 'LPG1', weight=2.1)
    network.add_edge('LPG1', 'PT2', weight=0.2)
    network.add_edge('PT2', 'PT3', weight=0.1)

    network.add_edge('Station 2', 'Esso1', weight=2.1)
    network.add_edge('Station 2', 'PTT1', weight=2.7)
    network.add_edge('PTT1', 'Esso2', weight=0.6)
    network.add_edge('Esso2', 'PTT2', weight=0.2)

    # กำหนดตำแหน่งของโหนด
    node_pos = {'Station 1': (2, 0),  
                'ChokNamChai': (3.5, -2.5),
                'PT4': (8, 1), 'PT5': (9, 2),'PTT5': (11, 4),
                'Shell1': (6, -5), 'PT-LPG2': (8, -6),
                'PTT4': (9, 9),
                'Bangchak': (1, -0.5), 'Esso3': (0.5, -1), 'PTT3': (-1, -1.5), 'PT-LPG1': (-3, -2), 'PT1': (-5, -2), 'LPG1': (-8, -0.5), 'PT2': (-9, 0),'PT3': (-9.5, 0.5),  

                'Station 2': (0, 1),
                'Esso1': (0.5, 2),'PTT1': (-1, 1.5), 'Esso2': (-2, 2),'PTT2': (-3, 2.5),
            }
    
    # สร้างกราฟ
    end = end_var.get()
    start, end = set_start_ends(network, end)
    shortest_path = nx.shortest_path(network, source=start, target=end, weight='weight')
    edge_colors = ['green' if (u, v) in zip(shortest_path[:-1], shortest_path[1:]) else 'black' for u, v in network.edges()]
    draw_graph(network, node_pos, edge_colors, start, end, shortest_path)
    print("เส้นทางที่ใกล้ที่สุดเมื่อมีไฟไหม้:")
    print(shortest_path)

# สร้าง GUI
root = tk.Tk()
root.title("Nakhon Nayok Fire Station")
# กำหนด style
style = ttk.Style()
style.configure('TMenubutton', font=('Arial', 14))
style.configure('Submit.TButton', font=('Arial', 14))

# สร้าง menu dropdown 
end_label = ttk.Label(root, text="โปรดระบุสถานที่ที่เกิดเหตุไฟไหม้:", font=("Arial", 14))
end_label.grid(row=0, column=0)

end_options = ['เลือกสถานที่','Bangchak','ChokNamChai','LPG1','PT-LPG1','PT-LPG2','PT1','PT2','PT3','PT4', 'PT5', 'PTT1','PTT2','PTT3','PTT4', 'PTT5', 'Shell1',
               'Esso1','Esso2','Esso3',]
end_var = tk.StringVar(root)
end_var.set(end_options[0])

end_menu = ttk.OptionMenu(root, end_var, *end_options)
end_menu.grid(row=0, column=1)
end_menu["menu"].config(font=("Arial", 14))

submit_button = ttk.Button(root, text="เลือก", command=on_submit, style='Submit.TButton')
submit_button.grid(row=0, column=2)

root.mainloop()
