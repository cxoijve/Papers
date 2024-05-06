import os
import re
import urllib.request
import pandas as pd
import json

def download_and_extract_files(download_url, extract_path):
    # Download and extract zip files
    os.system(f"wget -q {download_url} -O temp.zip")
    os.system(f"unzip -q temp.zip -d {extract_path}")
    os.remove("temp.zip")

def combine_text_files(directory_path, output_file_path):
    # Combine all text files into one
    combined_contents = ''
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            with open(os.path.join(directory_path, filename), 'r') as file:
                combined_contents += file.read() + "\n\n\n\n\n"
    with open(output_file_path, 'w') as output_file:
        output_file.write(combined_contents.rstrip("\n"))

def normalize_newlines(input_file_path, output_file_path):
    # Normalize newlines in the document
    with open(input_file_path, 'r') as file:
        content = '\n\n\n\n\n'.join(filter(None, file.read().split('\n' * 5)))
    with open(output_file_path, 'w') as output_file:
        output_file.write(content)

def remove_korean(input_file_path, output_file_path):
    # Remove Korean characters from the file
    korean_pattern = re.compile('[가-힣]+')
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            if not korean_pattern.search(line):
                output_file.write(line)

def split_documents(input_file_path):
    # Split documents by multiple newlines
    with open(input_file_path, 'r', encoding='utf-8') as file:
        documents = file.read().split('\n\n\n\n\n')
    print(f"Total documents: {len(documents)}")
    return documents

# Example usage
download_url = "https://github.com/cxoijve/articles/archive/refs/heads/main.zip"
extract_path = "extracted"
download_and_extract_files(download_url, extract_path)
combine_text_files('extracted/articles-main/txtfile', 'combined_file.txt')
normalize_newlines('combined_file.txt', 'normalized_combined_file.txt')
remove_korean('normalized_combined_file.txt', 'English_file.txt')
documents = split_documents('English_file.txt')
