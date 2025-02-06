# draw graph based on previous search
# Create one graph for each folder in graph_data
# Each file represents the first child of the parent (the parent is the name of the folder, which is the id from metadata.csv)
# the json objects within the file represents the second child of the parent (children of the first child)

import os
import networkx as nx
import matplotlib.pyplot as plt
import json


# create a graph for each folder
# parent = folder name
# first children = files in the folder
# second children = json objects in the files

def draw_graph():
    graph_dir = 'h3_repo/graph_data'
    for folder in os.listdir(graph_dir):
        G = nx.DiGraph()
        parent = folder
        G.add_node(parent)
        for file in os.listdir(f'{graph_dir}/{folder}'):
            first_child = file.split('.')[0]
            G.add_node(first_child)
            G.add_edge(parent, first_child)
            with open(f'{graph_dir}/{folder}/{file}', 'r') as f:
                children = json.load(f)
                for child in children:
                    for celex_num, url in child.items():
                        G.add_node(celex_num)
                        G.add_edge(first_child, celex_num)

        pos = {}
        pos[parent] = (0, 0)
        first_level_y = -1
        second_level_y = -2
        x_offset = 1

        for i, first_child in enumerate(G.successors(parent)):
            pos[first_child] = (i * x_offset, first_level_y)
            for j, second_child in enumerate(G.successors(first_child)):
                pos[second_child] = (i * x_offset + j * 0.5, second_level_y)

        plt.figure(figsize=(12, 8))  # Increase the size of the graph
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=8, font_color='black', edge_color='gray', linewidths=1.5, arrowsize=15, width=1.5)

        plt.savefig(f'h3_repo/graph/{parent}.jpg')
        # serve this .jpg file in the corresponding html path
        # create a html file for each graph
        with open(f'h3_repo/graph/{parent}.html', 'w') as f:
            f.write(f'<img src="{parent}.jpg" alt="{parent}" width="1000" height="1000>')

        print('save image!')
        plt.clf()  # Clear the current figure for the next graph

if __name__ == '__main__':
    draw_graph()
    print('Graph page created successfully!')