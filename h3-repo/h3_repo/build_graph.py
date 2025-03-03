import os
import json
import networkx as nx
from h3_repo.url_utils import save_html_from_url, find_celex

def find_child_docs(celex, urls):
    print("Looking for child documents in f'{seed_url}'....")
    # check if the file already exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    children_file = os.path.join(script_dir, 'children_data', f'{celex}.json')
    if os.path.exists(children_file):
        # if it does, read the file
        print('Reading existing children file at >> {children_file}')
        with open(children_file, 'r') as file:
            children = json.load(file)

    else:
        # if not, create a new children list json file
        children = list() # documents that are referenced within the page
        for url in urls:
            celex_num = find_celex(url)
            # read_celex_write_html(celex_num)
            children.append({celex_num:url})
        # write into json file

        with open(children_file, 'w') as file:
            json.dump(children, file)

    return children



# def bfs_find_child_docs(seed_url):
#     queue = [seed_url]
#     visited = set()
#     all_children = []

#     while queue:
#         current_url = queue.pop(0)
#         if current_url not in visited:
#             visited.add(current_url)
#             children = find_child_docs(current_url)
#             all_children.extend(children)
#             for child in children:
#                 for celex_num, url in child.items():
#                     if url not in visited:
#                         queue.append(url)

#     with open('bfs_children.json', 'w') as f:
#         json.dump(all_children, f, indent=4)

#     return all_children

def search_graph(seed_url):   
    G = nx.DiGraph()
    queue = [(seed_url, None)]  # (current_url, parent_url)
    visited = set()

    while queue:
        current_url, parent_url = queue.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            if parent_url:
                G.add_edge(parent_url, current_url)
            children = find_child_docs(current_url)
            for child in children:
                for celex_num, url in child.items():
                    if url not in visited:
                        queue.append((url, current_url))

    nx.write_gml(G, 'url_relationships.gml')
    return G


if __name__ == '__main__':
    # html_path = 'h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
    html_path = '/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
    ai_act_url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689&qid=1734617122196'
    
    html_from_url_path = '/Users/yun/Dev/humanet3/human-centered-repo/aiact_from_url.html' #/Users/yun/Dev/humanet3/human-centered-repo/
    
    # Load initial URLs from 'ai_act_children.json' if exists
    try:
        with open('ai_act_children.json', 'r') as f:
            initial_urls = json.load(f)
            initial_urls = [list(child.values())[0] for child in initial_urls]
    except FileNotFoundError:
        initial_urls = [ai_act_url]
    # Perform BFS to find child documents
    for url in initial_urls:
        bfs_find_child_docs(url)
    
    search_graph(ai_act_url)