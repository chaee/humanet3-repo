import os
import json
import csv
import networkx as nx
from h3_repo.url_utils import extract_doc_data


def save_child_info(celex, urls, save_path): #before: find_child_celex
    '''
    celex : celex number of the parent document (parent_celex)
    urls : all the oj notes found in the parent document (children_urls)
    find matching celex numbers for the children urls found in the parent html
    '''
    print(f'Looking for celex of child documents of {celex}...')
    
    # check if the file already exists
    children_file = os.path.join(save_path, f'{celex}.json')
    if os.path.isfile(children_file):
        # if it does, read the file
        print(f'Reading existing children file at >> {children_file}')
        with open(children_file, 'r') as file:
            children = json.load(file)

    else:
        # if not, create a new children list json file
        children = list() # documents that are referenced within the page
        errors = []
        csv_file = os.path.join(save_path, f'{celex}.csv')

        for idx, url in enumerate(urls):
            try:
                print(f'{idx}th child url in process: {url}')
                doc_data = extract_doc_data(celex, url) 
                if doc_data:
                    # doc_data['url'] = url
                    children.append(doc_data) # saving json file with celex number and url
                    # Save doc_data as a CSV file
                    with open(csv_file, 'a', newline='') as file:
                        fieldnames = doc_data.keys()
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        if file.tell() == 0:  # Check if the file is empty
                            writer.writeheader()
                        writer.writerow(doc_data)


                else:
                    errors.append(url)
            except Exception as e:
                print(f'Error processing URL {url}: {e}')
                errors.append(url)
        with open(children_file, 'w') as file:
            json.dump(children, file, indent=4)

        if errors:
            error_file = os.path.join(save_path, f'{celex}_errors.json')
            with open(error_file, 'w') as file:
                json.dump(errors, file)
        # write into json file

        # with open(children_file, 'w') as file:
        #     json.dump(children, file)

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
            children = find_child_celex(current_url)
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
    # for url in initial_urls:
    #     bfs_find_child_docs(url)
    
    search_graph(ai_act_url)