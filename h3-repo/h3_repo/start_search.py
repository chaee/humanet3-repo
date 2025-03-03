import build_graph
import os
import json
from url_utils import read_celex_write_html, extract_urls_from_html

if __name__ == '__main__':
    seed_celex = "32024R1689" #AI ACT "32022R2065" #DSA

    # seed_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065"
    # find children documents urls
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = read_celex_write_html(seed_celex)
    urls = extract_urls_from_html(html_path)
    build_graph.find_child_docs(seed_celex, urls)
    
    children_file = os.path.join(script_dir, 'children_data', f'{seed_celex}.json')
    print(f"Children file path: {children_file}")
    # read json file on the path children_file
    with open(children_file) as file:
        children = json.load(file)
    print(len(children))