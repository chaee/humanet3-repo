# open html file and extract urls
import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_urls_from_html(html_file):
    completed_urls = []
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    all_urls = {} # url : page data pair (ex: https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=OJ:C:2021:517:TOC & OJ C 517, 22.12.2021, p. 56)
    for link in soup.find_all('a'):
        path = link.get('href')
        label = link.get_text().strip()
        if 'legal-content' in path:
            all_urls[path] = label
        
    # find relevant urls
    # exclude urls including "https://data.europa.eu/eli/reg/2024/1689/oj" or "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689" (referring to EU AI Act itself)
    # iterate the dictionary url_data and leave only  that does not contain the above urls
    print("all urls:", len(all_urls))
    for url in all_urls.keys():
        if 'https://data.europa.eu/eli/reg/2024/1689/oj' not in url and 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689' not in url:
            if '32024R1689' not in url and '202401689' not in url:
                completed_urls.append(complete_url(url, all_urls[url]))
    print("after removing self-reference:", len(completed_urls))
    return completed_urls


def extract_urls_from_url(url):
    #url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.1985.210.01.0029.01.ENG&toc=OJ%3AL%3A1985%3A210%3ATOC'
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        directory = os.getcwd()
        file_path = os.path.join(directory, 'aiact_from_url.html')
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w', encoding='utf-8') as file:
            print("writing the file!!", file_path)
            file.write(html_content)

        # directory = 'h3_repo/eu_ai_act'
        # file_path = os.path.join(directory, 'aiact_from_url.html')
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     soup = BeautifulSoup(html_content, 'html.parser')
        #     all_urls = {} # url : page data pair
        #     for link in soup.find_all('a'):
        #         all_urls[link.get('href')] = link.get_text().strip()
        #     return all_urls
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





def read_celex_to_html(celex_num):
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
    html_from_url_path = 'aiact_from_url.html' #/Users/yun/Dev/humanet3/human-centered-repo/
    
    # extract_urls_from_url(ai_act_url)
    from_url = extract_urls_from_html(html_from_url_path)
    with open('eu_ai_act_refs_from_url.csv', 'w') as file:
        for url in from_url:
            file.write(url + '\n')
    # Compare the two lists
    
    