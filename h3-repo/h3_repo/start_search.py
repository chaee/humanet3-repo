import build_graph
import os
import json
from url_utils import read_celex_write_html, extract_urls_from_html

def process_single_document(seed_celex,url, save_path):
# find children documents urls
    html_path = read_celex_write_html(seed_celex) # save html (found w celex) content to a file
    children_urls = extract_urls_from_html(html_path) # find all the oj notes in the html

    # exception handling: try with celex first and if not url
    

    # check if the path exists
    children_file = os.path.join(save_path, f'{seed_celex}.json')
    if os.path.isfile(children_file): 
        print(f"Children file path: {children_file}")
        # read json file on the path children_file
        with open(children_file) as file:
            children = json.load(file)
        print(len(children))
    else:
        build_graph.save_child_info(seed_celex, children_urls, save_path) 



def process_children_documents(seed_celex, save_path):
    # read children documents
    script_dir = os.path.dirname(os.path.abspath(__file__))
    children_file = os.path.join(save_path, f'{seed_celex}.json') 
    # TBD: add seed celex in the folder name (so that they don't overwrite when referred by common docs)
    print(f"Children file path: {children_file}")
    # read json file on the path children_file
    with open(children_file) as file:
        children = json.load(file)
    
    for child in children:
        print(f"Processing document {child['celex_num'], child['title']}...")
        process_single_document(child['celex_num'],child['url'],save_path)


if __name__ == '__main__':
    '''
    "32022R2065"=DSA # 41 children 
    "32024R1689"= #AI ACT
    32022R1925 DMA
    '''
    seed_celex = "32022R2065"
    seed_celexes = []
    url=''
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'children_data')
    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    children_path = os.path.join(data_path, seed_celex)
    if not os.path.isdir(children_path):
        os.mkdir(children_path)
    # process_single_document(seed_celex,url,children_path)
    process_children_documents(seed_celex,children_path)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    graph_dir = os.path.join(script_dir, 'children_data')
    
    '''
    for folder in os.listdir(graph_dir):
        seed_celexes.append(folder)
        folder_path = os.path.join(graph_dir, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                celex = str(file).split('.')[0]
                celex = str(celex).split('_')[0]
                if celex not in seed_celexes:
                    save_path = os.path.join(folder_path, celex)
                    if not os.path.exists(save_path):
                        os.mkdir(os.path.join(graph_dir, celex))
                        process_single_document(celex, save_path)

    '''