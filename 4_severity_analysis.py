# Part 1: Similarity Calculation and Saving
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
keywords_df = pd.read_csv('Normalized_Unique_Keywords_List.csv')
keywords = keywords_df['Normalized Keywords'].tolist()

with open('English_file.txt', 'r', encoding='utf-8') as file:
    articles = file.read().split('\n\n\n\n\n')

# Convert all elements to strings
all_texts = [str(article) for article in articles] + [str(keyword) for keyword in keywords]

# Preprocess and vectorize text
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(all_texts)

# Calculate cosine similarity
articles_tfidf = tfidf_matrix[:len(articles)]
keywords_tfidf = tfidf_matrix[len(articles):]
similarity = cosine_similarity(articles_tfidf, keywords_tfidf)

# Create a DataFrame to store similarity scores
similarity_df = pd.DataFrame(similarity, columns=keywords, index=[f'Article {i+1}' for i in range(len(articles))])

# Save DataFrame to CSV
similarity_df.to_csv('similarity_scores.csv')

print("Similarity scores saved to 'similarity_scores.csv'.")


# Part 2: Victim Information Extraction and Severity Measurement
# Load the CSV file containing the 'victims' data
victims_data_path = 'victims.csv'
victims_df = pd.read_csv(victims_data_path)

# Define a function using regular expressions to extract victim count and type
def extract_victim_info(victim_data):
    victim_data_str = str(victim_data)
    match = re.search(r'(\d+)\((\w+)\)', victim_data_str)
    if match:
        return {'count': int(match.group(1)), 'type': match.group(2)}
    return {'count': 0, 'type': None}

# Apply the extraction function to each entry in the 'victims' column
victims_info = victims_df['victims'].apply(extract_victim_info)

# Convert the resulting series of dictionaries to a DataFrame
victims_info_df = pd.DataFrame(victims_info.tolist())

# Convert DataFrame to CSV file
victims_info_path = 'extracted_victims_info.csv'
victims_info_df.to_csv(victims_info_path, index=False)

print(f"Extracted victims info saved to {victims_info_path}.")


# Severity weights setting
severity_weights = {
    'accident': 0.6, 'adverse weather': 0.4, 'capsized': 0.7,
    'coastal isolation': 0.3, 'collision': 0.7, 'discharge of contaminated water': 0.5,
    'disruption': 0.4, 'drifting': 0.4, 'drunken driving': 0.5,
    'engine damage': 0.5, 'engine failure': 0.5, 'exceeding capacity': 0.6,
    'explosion': 1.0, 'fire': 0.7, 'flooding': 0.5,
    'inspection': 0.3, 'marine': 0.5, 'marine accident': 0.6,
    'marine pollution': 0.5, 'maritime countermeasures meeting': 0.4, 'maritime pollution': 0.5,
    'maritime safety threat': 0.5, 'mechanical defects': 0.5, 'minor contact': 0.4,
    'missing': 0.6, 'nuclear': 0.7, 'nuclear power plants': 0.7,
    'oil spill': 0.6, 'overloading': 0.6, 'overturning': 0.5,
    'pollution': 0.5, 'prevention': 0.3, 'radiation': 0.3,
    'rescue': 0.3, 'safety': 0.3, 'safety management': 0.3,
    'safety measures': 0.3, 'search and rescue operations': 0.3, 'seizure': 0.4,
    'sinking': 1.0, 'steering system damage': 0.5, 'stranded': 0.5,
    'violating crew standards': 0.5, 'war': 0.8,
    'injured': 0.7, 'deaths': 1.0, 'rescued': 0.3
}

# Convert weight data to DataFrame
weights_df = pd.DataFrame(list(severity_weights.items()), columns=['Incident Type', 'Severity Weight'])

print(weights_df)

