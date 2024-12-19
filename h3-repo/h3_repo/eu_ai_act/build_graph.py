import networkx as nx
from extract_url import find_citation, extract_urls_from_html

# html_path = 'h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'
html_path = '/Users/yun/Dev/humanet3/human-centered-repo/h3-repo/h3_repo/eu_ai_act/L_202401689EN.000101.fmx.xml.html'

urls = extract_urls_from_html(html_path)
find_citation(urls)
