import os
import json
import networkx as nx
from h3_repo.url_utils import get_html_from_url, find_celex

def find_child_docs(seed_url):
    seed_celex = find_celex(seed_url)
    children = list()
    urls = get_html_from_url(seed_url)
    for url in urls:
        celex_num = find_celex(url)
        children.append({celex_num: url})
    # make a folder named as seed_celex and save the children as json file
    if not os.path.exists(seed_celex):
        os.makedirs(seed_celex)
    with open(f'{seed_celex}/children.json', 'w') as f:
        json.dump(children, f, indent=4)

    return children


def bfs_find_child_docs(seed_url):
    queue = [seed_url]
    visited = set()
    all_children = []

    while queue:
        current_url = queue.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            children = find_child_docs(current_url)
            all_children.extend(children)
            for child in children:
                for celex_num, url in child.items():
                    if url not in visited:
                        queue.append(url)

    with open('bfs_children.json', 'w') as f:
        json.dump(all_children, f, indent=4)

    return all_children

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
    
    search_graph(ai_act_url)