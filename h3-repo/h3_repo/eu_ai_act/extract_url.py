# open html file and extract urls

import os
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

def extract_urls_from_html(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    urls = {}
    for link in soup.find_all('a'):
        urls[link.get('href')] = link.get_text()
    return urls


def find_citation(url_data):
    # find relevant urls
    # exclude urls including "https://data.europa.eu/eli/reg/2024/1689/oj" or "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689" (referring to EU AI Act itself)
    # iterate the dictionary url_data and leave only  that does not contain the above urls
    valid_pair = {}
    for url in url_data.keys():
        if 'https://data.europa.eu/eli/reg/2024/1689/oj' not in url and 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689' not in url:
            valid_pair[url] = url_data[url]
            print(url, '--', url_data[url])
    return valid_pair
             

    # urls = url_data['url']
    # urls = [url for url in urls if 'https://data.europa.eu/eli/reg/2024/1689/oj' not in url and 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689' not in url]
    
    # df = pd.DataFrame(urls, columns=['url'])
    # df.to_csv('h3_repo/eu_ai_act/urls.csv', index=False)


