import os
import networkx as nx
import json
import plotly.graph_objects as go

def draw_interactive_graph():
    graph_dir = 'h3_repo/graph_data'
    for folder in os.listdir(graph_dir):
        # creating graph
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

        pos = nx.spring_layout(G)
        for node in G.nodes():
            G.nodes[node]['pos'] = list(pos[node])

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[node for node in G.nodes()],
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    # titleside='right'
                ),
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f'Interactive Graph for {parent}',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Interactive Graph",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )

        fig.write_html(f'h3_repo/graph/{parent}_interactive.html')
        print(f'Interactive graph for {parent} created successfully!')

if __name__ == '__main__':
    # draw_graph()
    draw_interactive_graph()
    print('Graph pages created successfully!')