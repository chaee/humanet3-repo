import networkx as nx
import requests
from bs4 import BeautifulSoup

from extract_url import get_html_from_url

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
    children = list() # documents that are referenced within the page
    urls = get_html_from_url(seed_url)
    for url in urls:
        celex_num = find_celex(url)
        # read_celex_write_html(celex_num)
        children.append({celex_num:url})
    return children

if __name__ == '__main__':

    ai_act_url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689&qid=1734617122196'
    children = find_child_docs(ai_act_url)
    print(children)