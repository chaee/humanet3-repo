# an independent script for converting pdf files in the directory 'documents' to text files
# and create metadata json file
import os
import json
import PyPDF2
import csv
def pdf_to_txt(directory):
    '''
    One-off script to convert pdf files in the directory to text files
    input: directory of pdf files
    output: txt converted files
    '''
    # get all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('pdf') and os.path.isfile(os.path.join(directory, f))]
    for file in files:
        # open the pdf file
        pdf = open(os.path.join(directory, file), 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf)
        # create a text file with the same name if it does not exist yet
        if not os.path.exists(os.path.join(directory, file + '.txt')):
            txt = open(os.path.join(directory, file + '.txt'), 'w')
            # write the text to the file
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                txt.write(page.extract_text())
            # close the files
            pdf.close()
            txt.close()


def txt_to_json(dir, file_path):
        # create json file to save meta data per pdf on if it does not exist yet
        json_path = os.path.join(file_path[:-4] + '.json')

        meta_data = {}
        with open(os.path.join(dir, 'metadata.csv'), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['File name'] == file:
                    meta_data = row
                    break

        if meta_data:
            json_data = {
            'file_name': file,
            'date': meta_data.get('date', ''),
            'authority': meta_data.get('authority', ''),
            'jurisdiction': meta_data.get('jurisdiction', ''),
            'legally_binding': meta_data.get('legally_binding', '').lower() == 'true',
            'citations': meta_data.get('citations', '').split(';') if meta_data.get('citations') else [],
            'description': meta_data.get('description', ''),
            'title': meta_data.get('title', ''),
            'url': meta_data.get('url', '')
            }
        else:
            json_data = {
            'file_name': file,
            'date': '',
            'authority': '',
            'jurisdiction': '',
            'legally_binding': False,
            'citations': [],
            'description': '',
            'title': '',
            'url': ''
            }

        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        # # create json file to save meta data per pdf on if it does not exist yet

           

        # if not os.path.exists(json_path):
        #     json.dump(
        #         {
        #             'file_name': file, 
        #             'num_pages': len(pdf_reader.pages),
        #             'date': '',
        #             'authority': '',
        #             'jurisdiction': '',
        #             'legally_binding': False,
        #             'citations': [],
        #             'description': '',
        #             'title': '',
        #             'url': ''
        #         }, 
        #         open(json_path, 'w'), indent=4)
        

if __name__ == '__main__':
    # convert pdf to txt
    dir = 'h3_repo/documents'
    pdf_to_txt(dir)
    files = [f for f in os.listdir(dir) if f.endswith('pdf') and os.path.isfile(os.path.join(dir, f))]

    # create json for each doc
    for file in files:
        if not os.path.exists(os.path.join(dir, file + '.json')):
            txt_to_json(dir, os.path.join(dir, file + '.txt'))
