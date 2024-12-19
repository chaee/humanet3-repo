import requests
from bs4 import BeautifulSoup
import networkx as nx
from extract_url import extract_urls_from_html

def read_url_to_html(url, doc_id):
    # html link: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008R0300
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        document_title = soup.find('p', class_='DocumentTitle pull-left')
        if document_title:
            CELEX_num = document_title.text.strip()[9:]
            print(CELEX_num)
        
        #with open(f'/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/references/{doc_id}.html', 'w') as file:
        #    file.write(html_content)
        #print("HTML content saved to 'downloaded_page.html'")
    else:
        print('error')
          
# html_path = 'h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
html_path = '/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
urls = extract_urls_from_html(html_path)

with open('eu_ai_act_refs.csv', 'w') as file:
    for url in urls:
        file.write(url + '\n')

for url in urls:
    doc_id = url.split('uriserv:')[1].split('&')[0]
    read_url_to_html(url, doc_id)