# open html file and extract urls
import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
import json

def extract_urls_from_html(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    all_urls = [] # url : page data pair (ex: https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=OJ:C:2021:517:TOC & OJ C 517, 22.12.2021, p. 56)
    oj_notes = []
    for note in soup.find_all('p', class_='oj-note'):
        oj_notes.append(note)
    
    for note in oj_notes:
        for link in note.find_all('a'):
            path = link.get('href')
            label = link.get_text().strip()
            if 'legal-content' in path:
                all_urls.append(complete_url(path, label))
        
    # find relevant urls
    # exclude urls including "https://data.europa.eu/eli/reg/2024/1689/oj" or "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689" (referring to EU AI Act itself)
    # iterate the dictionary url_data and leave only  that does not contain the above urls
    print("all urls:", len(all_urls))
    print("all oj notes:", len(oj_notes))

    return all_urls

def get_html_from_url(url):
    #url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.1985.210.01.0029.01.ENG&toc=OJ%3AL%3A1985%3A210%3ATOC'
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        directory = os.getcwd()
        file_name = re.sub(r'\W+', '_', url)[:50]  # Replace non-alphanumeric characters with underscores and limit length
        file_path = os.path.join(directory, f'{file_name}.html')
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w', encoding='utf-8') as file:
            print("writing the file!!", file_path)
            file.write(html_content)
        return extract_urls_from_html(file_path) 
    else:
        print(f'Failed to retrieve content for url number: {url}')
        return None
    

def complete_url(url, url_data):
    pattern = r'OJ\s(?P<doc_type>\w+)\s(?P<doc_num>\d+),\s(?P<date>\d{1,2}\.\d{1,2}\.\d{4}),\sp\.\s(?P<page_num>\d+)'
    match = re.search(pattern, url_data)
    if match:
        doc_type = match.group("doc_type")
        doc_num = f'{int(match.group("doc_num")):03}'
        date = match.group("date")
        page_num = f'{int(match.group("page_num")):04}'
        final_url = f'https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=uriserv:OJ.{doc_type}_.{date.split(".")[2]}.{doc_num}.01.{page_num}.01.ENG&toc=OJ:{doc_type}:{date.split(".")[2]}:{doc_num}:TOC'
    else:
        final_url = url
    return final_url

# # complete_url("https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=OJ:L:2018:151:TOC", "OJ L 151, 14.6.2018, p. 1")
# print(urls)


def read_celex_write_html(celex_num):
    '''
    Retrieve html of each document using CELEX and save the content (text) into a file {celex_num}.html
    '''
    url_format = f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex_num}'
    response = requests.get(url_format)
    if response.status_code == 200:
        html_content = response.text
        file_path = os.path.join('eu_ai_act/references', f'{celex_num}.html')
        if not os.path.exists(file_path):
            if not os.path.exists('references'):
                os.makedirs('references')
            with open(file_path, 'w', encoding='utf-8') as file:
                soup = BeautifulSoup(html_content, 'html.parser')
                text_content = soup.get_text()
                file.write(text_content)
        return html_content
    else:
        print(f'Failed to retrieve content for CELEX number: {celex_num}')
        return None


def find_celex(url):
    '''
    read url to open that page (eur-lex web page)
    '''
    # html link: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008R0300
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        document_title = soup.find('p', class_='DocumentTitle pull-left') 
        if document_title:
            celex_num = document_title.text.strip()[9:]
    else:
        print(f'request error:{url}')          
    return celex_num


def find_child_docs(seed_url):
    seed_celex = find_celex(seed_url)
    children = list()
    urls = get_html_from_url(seed_url)
    for url in urls:
        celex_num = find_celex(url)
        children.append({celex_num: url})
    
    with open(f'{seed_celex}_children.json', 'w') as f:
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
    # urls = extract_urls_from_html(html_path)

    # with open('eu_ai_act_refs.csv', 'w') as file:
    #     for url in urls:
    #         file.write(url + '\n')

    # for url in urls:
    #     print('url')
    #     celex_num = find_celex(url)
    #     read_celex_to_html(celex_num)
        # extract_urls_from_url(ai_act_url)

    ai_act_url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689&qid=1734617122196'
    html_from_url_path = '/Users/yun/Dev/humanet3/human-centered-repo/aiact_from_url.html' #/Users/yun/Dev/humanet3/human-centered-repo/
    
    # extract_urls_from_url(ai_act_url)
    # from_url = extract_urls_from_html(html_from_url_path)
    # with open('eu_ai_act_refs_from_url.csv', 'w') as file:
    #     for url in from_url:
    #         file.write(url + '\n')

    
    # children = find_child_docs(ai_act_url)
    # print(children)

    
# Load initial URLs from 'ai_act_children.json' if exists
    # try:
    #     with open('ai_act_children.json', 'r') as f:
    #         initial_urls = json.load(f)
    #         initial_urls = [list(child.values())[0] for child in initial_urls]
    # except FileNotFoundError:
    #     initial_urls = [ai_act_url]

    # # Perform BFS to find child documents
    # for url in initial_urls:
    #     bfs_find_child_docs(url)

    search_graph(ai_act_url)