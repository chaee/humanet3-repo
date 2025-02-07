from flask import Flask, send_from_directory, render_template
import os
import file_to_table

# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route('/')
@app.route('/table')
def about():
    # create tables using file_to_table module
    doc_dir = 'documents'
    #table = file_to_table.get_table_html(doc_dir)
    table = file_to_table.make_table_from_csv('h3_repo/documents/metadata.csv')
    # adjust table length for better display in the browser (table to fit the length of the text inside)
    table = table.replace('<table', '<table style="width:100%"')
    
    return render_template('table.html', table_html=table)
    # return table
    # reads files from directory and sends them as an html table

    return "<h1>List of documents</h1><p>yes yes</p>"

# Define a route to serve a PDF file
@app.route('/documents/<filename>')
def serve_pdf(filename):
    pdf_directory = os.path.join(app.root_path, 'documents')  # Adjust the directory as needed
    return send_from_directory(pdf_directory, filename)

# Define a route to serve graph files
@app.route('/graph/<filename>')
def serve_graph(filename):
    graph_directory = os.path.join(app.root_path, 'graph')
    return send_from_directory(graph_directory, filename)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
