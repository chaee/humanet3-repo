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

def save_html_from_url(celex, url):
    '''
    Retrieve and save html from celex number or url
    '''
    print("getting html from f'{url}'")
    #url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.1985.210.01.0029.01.ENG&toc=OJ%3AL%3A1985%3A210%3ATOC'
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if os.path.exists(os.path.join(script_dir, 'celex_data')) == False:
            os.makedirs(os.path.join(script_dir, 'celex_data'))
        file_path = os.path.join(script_dir, 'celex_data', f'{celex}.html')

        with open(file_path, 'w', encoding='utf-8') as file:
            print("writing the html file >> at f'{file_path}'")
            file.write(html_content)
        return file_path
        # return extract_urls_from_html(file_path) # should separate 1. transform url into html -> 2. get child urls from html
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
        return save_html_from_url(celex_num, url_format)

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
            # document_title.text example:
            celex_num = document_title.text.strip()[9:] # TBD: Find regex with pattern (not hardcoded like now?)
            return celex_num
        else:
            print(f'Failed to find CELEX number for url: {url}')
            return None
    else:
        print(f'request error:{url}')          

if __name__ == '__main__':
    # html_path = 'h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
    html_path = '/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
    urls = extract_urls_from_html(html_path)

    with open('eu_ai_act_refs.csv', 'w') as file:
        for url in urls:
            file.write(url + '\n')

    for url in urls:
        print('url')
        celex_num = find_celex(url)
        read_celex_write_html(celex_num)
        extract_urls_from_url(ai_act_url)

    ai_act_url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689&qid=1734617122196'
    html_from_url_path = '/Users/yun/Dev/humanet3/human-centered-repo/aiact_from_url.html' #/Users/yun/Dev/humanet3/human-centered-repo/
    
    extract_urls_from_url(ai_act_url)
    from_url = extract_urls_from_html(html_from_url_path)
    with open('eu_ai_act_refs_from_url.csv', 'w') as file:
        for url in from_url:
            file.write(url + '\n')

    
    children = find_child_docs(ai_act_url)
    print(children)

    



