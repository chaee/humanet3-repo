# an independent script for converting pdf files in the directory 'documents' to text files
# and create metadata json file
import os
import json
import PyPDF2
def pdf_to_txt_json(directory):
    # get all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('pdf') and os.path.isfile(os.path.join(directory, f))]
    for file in files:
        # open the pdf file
        pdf = open(os.path.join(directory, file), 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf)
        # create a text file with the same name
        txt = open(os.path.join(directory, file + '.txt'), 'w')
        # write the text to the file
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            txt.write(page.extract_text())
        # close the files
        pdf.close()
        txt.close()
        # create json file to save meta data per pdf
        json.dump(
            {
                'file_name': file, 
                'num_pages': len(pdf_reader.pages),
                'date': '',
                'authority': '',
                'jurisdiction': '',
                'legally_binding': False,
                'citations': {
                    'parents': [],
                    'children': []
                },
                'description': '',
                'title': ''
            }, 
            open(os.path.join(directory, file + '.json'), 'w'), indent=4)
        

if __name__ == '__main__':
    pdf_to_txt_json('h3_repo/documents') 
