import pandas as pd
import os
from openai import ChatCompletion


def create_chat_completion_dicts(documents, client, categories_str):
    """Create chat completion dictionaries using OpenAI API for each document."""
    chat_completion_dicts = []
    for doc in documents:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    - You will be provided with a corpus on marine accidents articles. And you must to extract keywords(from at least top 1 to top 3) related to marine accident types and the number of casualties from the article.

                    Please output ***keywords*** based on the following conditions:
                    - The keywords should be one of the following: {categories_str}
                    - When extracting keywords, it is necessary to infer from the context to understand what type of maritime accident is being referred to.
                    - Although the categories include 'etc', the keywords must be extracted as related to the maritime accident keyword.
                    - If it is not related to a maritime accident, extract the keyword ‘Not related’.
                    - Only marine accidents that actually occur, such as casualties or ship collisions, are considered 'marine accidents'. For example, articles such as ‘Inspection to prevent accidents’ and ‘Maritime countermeasures meeting’ are not considered marine accidents because they do not result in direct accident damage.
                    - Format the answer succinctly in lowercase with only keywords. Exclude special characters or numbers unrelated to keywords.

                    Please output ***the number of casualties*** based on the following conditions:
                    1. If it's not a maritime 'accident' or there are no casualties:
                       Output Example: 'None'
                    2. If there are casualties:
                       - If there are fatalities or injuries, represent them numerically:
                         Output Example 1: 34(deaths)
                         Output Example 2: 1(injured)
                         Output Example 3: 3(deaths), 2(injured)
                       - If there are fatalities or injuries but not represented numerically:
                         Output Example 1: V

                    Ensure strict adherence to the following format. By default, encapsulate in a list, but if there are two or more keywords or two or more casualty figures, encapsulate in a nested list. It's crucial to adhere to this rigorously, or else you'll face severe penalties.
                    """
                },
                {
                    "role": "user",
                    "content": doc
                }
            ],
            temperature=0.5,
            max_tokens=15,
            top_p=1
        )
        keywords = response.choices[0].message.content
        chat_completion_dicts.append({
            "document": doc,
            "keywords": keywords
        })
    return chat_completion_dicts


def save_to_dataframe(chat_completion_dicts, csv_path, jsonl_path):
    """Convert dictionary list to DataFrame and save to CSV and JSONL."""
    df = pd.DataFrame(chat_completion_dicts)
    df.to_csv(csv_path, index=False)
    df.to_json(jsonl_path, orient='records', lines=True)


def main():
    documents = ["document1 content", "document2 content"]  # Example document content
    categories_str = "collision, sinking, fire"  # Example categories string


    # Set up API client
    client = ChatCompletion(api_key="your_openai_api_key")

    chat_completion_dicts = create_chat_completion_dicts(documents, client, categories_str)
    save_to_dataframe(chat_completion_dicts, 'marineArticles.csv', 'marineArticles.jsonl')


if __name__ == "__main__":
    main()
