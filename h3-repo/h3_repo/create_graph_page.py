# Read the metadata.csv and create a graph page for each entry (based on the title)
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import extract_url

# read the metadata.csv
def create_overview_graph_page(csv_file):
    df = pd.read_csv(csv_file)
    # create a graph with a initial node
    for index, row in df.iterrows():
        G = nx.DiGraph()
        # create separate graph for each title in the metadata
        title = row['Title']
        id = row["ID"]
        G.add_node(title)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        plt.savefig(f'h3_repo/graph/{id}.jpg')
        # serve this .jpg file in the corresponding html path
        # create a html file for each graph
        with open(f'h3_repo/graph/{id}.html', 'w') as f:
            f.write(f'<img src="{id}.jpg" alt="{title}" width="1000" height="1000">')
            

        print('save image!')
        plt.clf()  # Clear the current figure for the next graph
    return G





if __name__ == '__main__':
    metadata = 'h3_repo/documents/metadata.csv'
    create_overview_graph_page(metadata)
    print('Graph page created successfully!')


