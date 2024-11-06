from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import file_to_table

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"GET request received for path: {self.path}")
        # Serve different pages based on the path
        if self.path == '/' or self.path == '/index':
            # self.serve_page('index.html')
            self.serve_table()
        elif self.path == '/graph':
            self.serve_page('graph.html')
        elif self.path.endswith('.pdf'):
            self.serve_pdf(self.path) 
        else:
            self.send_error(404, "Page Not Found")  # 404 for unknown paths
    
    def serve_pdf(self, pdf_filename):
        # Path to the PDF file in the "files" directory
        if os.path.exists(pdf_filename):
            # Set headers to serve the file as a PDF
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f'inline; filename="{pdf_filename}"')
            self.end_headers()
            
            # Open and read the PDF file in binary mode
            with open(pdf_filename, 'rb') as pdf_file:
                self.wfile.write(pdf_file.read())
        else:
            self.send_error(404, f"PDF File {pdf_filename} Not Found")


    def serve_table(self): 
        # get all files in the directory
        content = file_to_table.get_table_html(os.path.join(os.path.dirname(__file__), "documents"))
        # Send HTTP response headers
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Write the table to the response
        self.wfile.write(content.encode('utf-8'))


    def serve_page(self, page):
        file_path = os.path.join(os.path.dirname(__file__), "webpages", page)
        try:
            # Check if the file exists
            if os.path.exists(file_path):
                # Read the HTML file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Send HTTP response headers
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Write the content to the response
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, f"File {file_path} Not Found")
        except Exception as e:
            self.send_error(500, "Server Error: {}".format(str(e)))

# Server settings
host = "localhost"
port = 8000

# Create and start the server
httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
print(f"Server started at http://{host}:{port}")
httpd.serve_forever()
