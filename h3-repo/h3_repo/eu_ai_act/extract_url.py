# open html file and extract urls

from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_urls_from_html(html_file):
    completed_urls = []
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    all_urls = {} # url : page data pair (ex: https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=OJ:C:2021:517:TOC & OJ C 517, 22.12.2021, p. 56)
    for link in soup.find_all('a'):
        all_urls[link.get('href')] = link.get_text().strip()
        
    # find relevant urls
    # exclude urls including "https://data.europa.eu/eli/reg/2024/1689/oj" or "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689" (referring to EU AI Act itself)
    # iterate the dictionary url_data and leave only  that does not contain the above urls
    print("all urls:", len(all_urls))
    for url in all_urls.keys():
        if 'https://data.europa.eu/eli/reg/2024/1689/oj' not in url and 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689' not in url:
            completed_urls.append(complete_url(url, all_urls[url]))
    print("after removing self-reference:", len(completed_urls))
    return completed_urls


def complete_url(url, url_data):
    pattern = r'OJ\s(?P<doc_type>\w+)\s(?P<doc_num>\d+),\s(?P<date>\d{1,2}\.\d{1,2}\.\d{4}),\sp\.\s(?P<page_num>\d+)'
    match = re.search(pattern, url_data)
    if match:
        doc_type = match.group("doc_type")
        doc_num = f'{int(match.group("doc_num")):03}'
        date = match.group("date")
        page_num = f'{int(match.group("page_num")):04}'
        final_url = f'https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=uriserv:OJ.{doc_type}_.{date.split(".")[2]}.{doc_num}.01.{page_num}.01.ENG&toc=OJ:{doc_type}:{date.split(".")[2]}:{doc_num}:TOC'
    #    print('matched:', url_data)
    else:
        #print(f'>{url_data}<')
        # print('not matched:', url_data)
        final_url = url
    return final_url

# # complete_url("https://eur-lex.europa.eu/legal-content/EN/AUTO/?uri=OJ:L:2018:151:TOC", "OJ L 151, 14.6.2018, p. 1")
# html_path = '/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
# urls = extract_urls_from_html(html_path)
# print(urls)