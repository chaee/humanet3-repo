# module for creating tables in the database
import os
import json
import pandas as pd
# reads files from directory and sends them as an html table
def get_table_html(directory):
    # get all files in the directory
    
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('pdf')]
    # create the table by reading json files

    headers = ["File Name", "pdf", "text", "Size (bytes)"]
    rows = []
    for file in files:
        # create link for files and fetch the file size
        pdf_link = os.path.join(directory, file)
        txt_link = os.path.join(directory, file + '.txt')
        size = os.path.getsize(os.path.join(directory, file))

        # read json file
        json_path = os.path.join(directory, file + '.json')
        if os.path.exists(json_path):
            meta = json.load(open(json_path))
        else:
            meta = {}
        for key in meta:
            if key not in headers:
                headers.append(key)
        
        row = [file, f'<a href="{pdf_link}">pdf</a>', f'<a href="{txt_link}">text</a>', size]

        for key in headers[4:]:
            row.append(meta.get(key, ''))

        # create a row with the file name and size
        rows.append(row)

    
    table = '<table id="documents-table" class="display"><tr>'
    for header in headers:
        table += f"<th>{header}</th>"
    table += "</tr>"
    for row in rows:
        table += "<tr>"
        for cell in row:
            table += f"<td>{cell}</td>"
        table += "</tr>"
    table += "</table>"
    return table    

def make_table_from_csv(csv_file):
    # read csv file into dataframe except for the last two columns
    df = pd.read_csv(csv_file).iloc[:, :-2]
    # fill NaN with empty strings
    df = df.fillna('')
    # remove file extension in the column 'file_name'
    #df['File name'] = df['File name'].str.replace('.pdf', '')
     # Add hyperlink anchor to the values in column 'PDF URL' and 'HTML URL'
    if 'PDF' in df.columns:
        df['PDF'] = df['PDF'].apply(lambda x: f'<a href="{x}">pdf</a>' if x else '')
    if 'HTML' in df.columns:
        df['HTML'] = df['HTML'].apply(lambda x: f'<a href="{x}">html</a>' if x else '')
    df['Text'] = df['File name'].apply(lambda x: f'<a href="/documents/{x}.txt">text</a>')
    df['Graph'] = df['ID'].apply(lambda x: f'<a href="/graph/{x}.html">graph</a>')
    # Convert DataFrame to HTML
    return df.to_html(escape=False)