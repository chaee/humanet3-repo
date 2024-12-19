import re

def normalize_content(content):
    """
    Remove markdown syntax, extra whitespace, and newlines.
    Returns a list of words for content comparison.
    """
    # Remove markdown elements and extra spaces
    content = re.sub(r'#|\*|\-|`|\[|\]|\(|\)|<|>|:', '', content)  # Strip markdown symbols
    content = re.sub(r'\s+', ' ', content)  # Reduce any whitespace to a single space
    return content.strip().lower().split()  # Return as lowercase word list

def read_and_normalize(filename):
    """Read the contents of a file and return a normalized list of words."""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return normalize_content(content)

def compare_content(file1, file2):
    """Compare normalized content of two files."""
    original_words = read_and_normalize(file1)
    modified_words = read_and_normalize(file2)
    
    # Compare the lists of words
    if original_words == modified_words:
        print("The content matches exactly.")
    else:
        print("Content differences found:")
        # Find and display differences by word position
        differences = [
            (i, original_words[i], modified_words[i]) 
            for i in range(min(len(original_words), len(modified_words))) 
            if original_words[i] != modified_words[i]
        ]
        
        # Print a summary of differences
        for index, orig_word, mod_word in differences[:10]:  # Show only the first 10 differences
            print(f"Difference at word {index}: '{orig_word}' (original) vs '{mod_word}' (modified)")

        # If there are length mismatches
        if len(original_words) != len(modified_words):
            print("\nNote: The files have different lengths.")
            print(f"Original file has {len(original_words)} words.")
            print(f"Modified file has {len(modified_words)} words.")

# Paths to the original and markdown files
original_file = 'path/to/original.txt'  # Replace with actual path to the original .txt file
formatted_file = 'path/to/formatted.md'  # Replace with actual path to the .md file

# Run the comparison
compare_content(original_file, formatted_file)
