# open html file and extract urls
import os
import re
import requests
from requests.exceptions import RequestException

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
        all_urls.append(note)
    
    for note in all_urls:
        for link in note.find_all('a'):
            path = link.get('href')
            label = str(link.get_text().strip())
            if 'legal-content' in path:
                oj_notes.append(complete_url(path, label))
        
    # find relevant urls
    # exclude urls including "https://data.europa.eu/eli/reg/2024/1689/oj" or "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689" (referring to EU AI Act itself)
    # iterate the dictionary url_data and leave only  that does not contain the above urls
    print("all urls:", len(all_urls))
    print("all oj notes:", len(oj_notes))

    return oj_notes

def save_html_from_url(celex, html_content):
    '''
    Retrieve and save html from celex number or url
    '''
    # check if the file already exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'celex_html_data', f'{celex}.html')
    
    if os.path.exists(html_file):
        print(f'HTML file already exists at >> {html_file}')
        return html_file
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        if os.path.exists(os.path.join(script_dir, 'celex_html_data')) == False:
            os.makedirs(os.path.join(script_dir, 'celex_html_data'))
        file_path = os.path.join(script_dir, 'celex_html_data', f'{celex}.html')

        with open(file_path, 'w', encoding='utf-8') as file:
            print(f"writing the html file >> at '{file_path}'")
            file.write(html_content)
        return file_path

    

def complete_url(url, url_data):
    pattern = r'OJ\s(?P<doc_type>\w+)\s(?P<doc_num>\d+)(?P<edition>\s\w)?,\s(?P<date>\d{1,2}\.\d{1,2}\.\d{4}),\sp\.\s(?P<page_num>\d+)'
    match = re.search(pattern, url_data)
    if match:
        # print("correct pattern>>>>")
        # print(f'{url_data=}')
        # print(f'{url=}')
        doc_type = match.group("doc_type")
        doc_num = f'{int(match.group("doc_num")):03}'
        doc_ed = ''
        if match.group("edition"):
            doc_ed = match.group("edition").strip()
        date = match.group("date")
        page_num = f'{int(match.group("page_num")):04}'
        final_url = f'https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=uriserv:OJ.{doc_type}_.{date.split(".")[2]}.{doc_num}{doc_ed}.01.{page_num}.01.ENG&toc=OJ:{doc_type}:{date.split(".")[2]}:{doc_num}:TOC'
    else:
        # print("different pattern!!!")
        # print(f'{url_data=}')
        # print(f'{url=}')

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
        return save_html_from_url(celex_num, html_content=response.text)

    else:
        print(f'Failed to retrieve content for CELEX number: {celex_num}')
        return None

def extract_celex(soup):
    celex = soup.find('h1')
    if celex:
        celex_num = celex.text.strip()
        return celex_num
    else:
        print("Cannot find CELEX number!")
        return None


def extract_oj_num(soup):
    hd_oj = soup.find('p', class_='hd-oj')
    em = soup.find('em')

    if hd_oj:
        oj_num_head = hd_oj.text.strip() # <p class="hd-oj">L 95/29</p>
        doc_type = oj_num_head.split(' ')[0] # L
        hd_date = soup.find('p', class_='hd-date') #  <p class="hd-date">21.4.1993   </p>
        oj_num = f'{oj_num_head}, {hd_date.text.strip()}'

    elif em: # <br>Official Journal L 011 , 15/01/2002 P. 0004 - 0017<br> </em>
        # if em looks like this: <em>OJ C 286, 16.7.2021, p. 64-69    (BG, ES....)
        em_content = em.get_text().split('(')[0].strip().replace('\u2013', '-')
        #br_content = em.find('br').next_sibling.strip() if em.find('br') else em.get_text().strip()
        # oj_num = em_content.replace("Official Journal", "OJ")
        oj_num = em_content
        doc_type = em_content.split(' ')[1]

        # if em looks like this: <em><br>Official Journal L 011 , 15/01/2002 P. 0004 - 0017<br> </em>... 
    else:
        print("Cannot find OJ number!")
        return None
    return doc_type, oj_num

def extract_title(soup):
    #oj_doc_ti = soup.find('p', class_='oj-doc-ti')
    # if oj_doc_ti:   
    #     title = oj_doc_ti.text.strip().replace('\u2018', "'").replace('\u2019', "'")
    #     return title
    if soup.find('p', id='title', class_='title-bold'):
        title = soup.find('p', id='title', class_='title-bold').text.strip()
        title = title.replace('\u2018', "'").replace('\u2019', "'")
        title = title.replace('\u00a0', ' ')
        title = title.replace("\u2014", "-")
        return title
    else:
        print("Cannot find document title!")
        return None
    

def extract_doc_data(parent_celex, url):
    '''
    used to be find_celex
    read url to open that page (eur-lex web page)
    '''
    # html link: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008R0300
    script_dir = os.path.dirname(os.path.abspath(__file__))
    error_file = os.path.join(script_dir, 'children_data', f'{parent_celex}_errors.json')

    # add option to read html instead of request
    doc_data = {}
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            document_title_celex = soup.find('p', class_='DocumentTitle pull-left')
            if document_title_celex:
                print(f'Processing {document_title_celex.text.strip()}...')
                # document_title.text example:
                # celex_num = document_title.text.strip()[9:] # TBD: Find regex with pattern (not hardcoded like now?)
                doc_data['title'] = extract_title(soup)
                doc_type, oj_num = extract_oj_num(soup)
                doc_data['parent_celex'] = parent_celex
                doc_data['oj_num'] = oj_num
                doc_data['doc_type'] = doc_type
                doc_data['celex_num'] = document_title_celex.text.strip()[9:] # document_title.text.split('\xa0')[1].strip() 
                doc_data['url'] = url
                save_html_from_url(doc_data['celex_num'], html_content)

                return doc_data
            else:
                print(f'Failed to find document title in: {url}')
                return None

    except RequestException as e:
        print(f"Request failed: {e}")
        e = str(e)
        if os.path.exists(error_file) == False:
            with open(error_file, 'w') as file:
                json.dump(e, file)
        else:  
            with open(error_file, 'a') as file:
                json.dump(e, file)

    except Exception as e:
        print(f"Unexpected error: {e}")
        e = str(e)
        if os.path.exists(error_file) == False:
            with open(error_file, 'w') as file:
                json.dump(e, file)
        else:  
            with open(error_file, 'a') as file:
                json.dump(e, file)

          

if __name__ == '__main__':
    
    
    pass

    



