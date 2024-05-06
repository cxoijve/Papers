# Part 1

import os
import urllib.request
import pandas as pd
import json
import re

client_id = " " # Naver API ID
client_secret = " "  # Naver API Password

# List of search terms
search_terms = [
    "Marine Logistics Accident", "Marine safety", "Ship Collision", "Sea Accident",
    "Marine Rescue", "Marine pollution", "Response to marine accidents",
    "Preventing Marine Accidents", "Detecting marine hazards", "Sea Security",
    "Sea Accident Simulation", "Vessel Automation", "Ship IoT System",
    "Analyzing Marine Accident Data", "Monitoring Ships", "AI Maritime Safety",
    "Sea Traffic Management", "Ship Safety", "Ship Navigation Technology", "Ship Tracking System"
]

# settings
display = 100
sort = "sim"

# List to store news data
news_data = []

# Calling API to collect data
for query in search_terms:
    encoded_query = urllib.parse.quote(query)
    for start_index in range(1, 1000, display):
        url = f"https://openapi.naver.com/v1/search/news?query={encoded_query}&display={display}&start={start_index}&sort={sort}"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            response_body = response.read()
            response_dict = json.loads(response_body.decode('utf-8'))
            for item in response_dict['items']:
                clean_data = {
                    "Title": re.sub('<.*?>', '', item['title']),
                    "Original Link": item['originallink'],
                    "Link": item['link'],
                    "Description": re.sub('<.*?>', '', item['description']),
                    "Publication Date": item['pubDate']
                }
                news_data.append(clean_data)
        else:
            print("Error Code:", response.getcode())

# Convert data into a DataFrame
all_news_df = pd.DataFrame(news_data)
all_news_df = all_news_df.drop_duplicates(subset=["Title", "Original Link"])

# Save results to a CSV file
csv_file_name = "marine_news_data.csv"
all_news_df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

print(f"CSV 파일 저장 완료: {csv_file_name}")


# Part 2

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def load_and_preprocess_data(file_path):
    """Load CSV file and preprocess the data"""
    news_df = pd.read_csv(file_path)
    news_df['Description'] = news_df['Description'].astype(str)
    news_df = news_df.drop_duplicates(subset=['Description'])
    news_df = news_df[~news_df['Description'].str.contains('[ㄱ-ㅎㅏ-ㅣ가-힣]', regex=True)]
    return news_df


def scrape_article_contents(news_df):
    """Scrape article content from each link"""
    article_contents = []
    for link in news_df['Link']:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                article_content = soup.find('div', class_='article-body')
                article_contents.append(article_content.get_text(strip=True) if article_content else "내용 없음")
            else:
                article_contents.append("No content")
        except Exception as e:
            article_contents.append(f"Error: {str(e)}")
    return article_contents


def save_articles_to_files(news_df, save_folder):
    """Save each article content to individual files"""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for index, row in news_df.iterrows():
        if row['Article Content'] != "No content":
            file_path = os.path.join(save_folder, f"article_{index}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(row['Article Content'])


# File path and folder setup
file_path = 'marine_news_data.csv'
save_folder = 'path_to_local_directory/folder_name'

# Load and preprocess data
news_df = load_and_preprocess_data(file_path)

# Scrape article contents via web scraping
news_df['Article Content'] = scrape_article_contents(news_df)

# Save results to a new CSV file
news_df.to_csv('marine_news_data_with_content.csv', index=False, encoding='utf-8-sig')

# Save each article to individual files
save_articles_to_files(news_df, save_folder)


"""
The 'Link' column of the CSV file was iterated over to store the main content of the articles in one column.
During the web scraping process to extract the main text, the HTML structure of each news article was examined
and additional preprocessing was implemented. After web scraping, the news article data was saved in text format (.txt)
and uploaded to GitHub.
"""
