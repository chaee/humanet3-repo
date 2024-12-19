import re

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def convert_to_markdown(content):
    # Example transformations (you can add more as needed)
    
    '''
    # For US executive order
    content = content.replace('OCTOBER 30, 2023', '# OCTOBER 30, 2023')
    content = content.replace('Executive Order on the Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence', '## Executive Order on the Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence')
    
    # Use regular expressions to find and replace headings
    content = re.sub(r'^(Section \d+\..*)$', r'### \1', content, flags=re.MULTILINE)
    # Add more transformations as needed
    '''
    return content

def write_markdown_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    # convert txt to md

    # Example usage
    txt_file_path = 'documents/CELEX:32016R0679:EN:TXT.pdf.txt'
    md_file_path = txt_file_path.replace('.txt', '.md')

    # Read the .txt file
    txt_content = read_txt_file(txt_file_path)

    # Convert the content to Markdown
    md_content = convert_to_markdown(txt_content)

    # Write the Markdown content to a new file
    write_markdown_file(md_content, md_file_path)
