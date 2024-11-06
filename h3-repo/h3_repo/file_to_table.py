# module for creating tables in the database
import os
# reads files from directory and sends them as an html table
def get_table_html(directory):
    # get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # create the table
    headers = ["File Name", "pdf", "text", "Size (bytes)"]
    rows = []
    for file in files:
        # get the file size
        pdf_link = os.path.join(directory, file)
        size = os.path.getsize(os.path.join(directory, file))
        # create a row with the file name and size
        row = [file, f'<a href="{pdf_link}">pdf</a>', f'<a href="{file}.txt">text</a>', size]
        rows.append(row)

    table = "<table><tr>"
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