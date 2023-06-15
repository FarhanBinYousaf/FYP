import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

jobs = pd.read_csv("careerjobs.csv")



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Clean Description
import ast
import re

def convert(text):
    original_description = ast.literal_eval(text)
    cleaned_text = [re.sub(r'[•\t\r\xa0>]', '', sentence) for sentence in original_description]
    cleaned_text = ' '.join(cleaned_text)
    return cleaned_text

try:
    jobs['Description'] = jobs['Description'].apply(convert)
except Exception as e:
    print("An error occurred: ", e)
    

# Drop Duplicate
jobs = jobs.drop_duplicates().reset_index(drop=True)


# clean text
def clean_text(text):
    cleaned_text = ''.join(char for char in text if char.isalnum() or char.isspace())
    return cleaned_text



jobs['Skills'] = jobs['Skills'].apply(clean_text)
jobs['Qualification'] = jobs['Qualification'].apply(clean_text)
jobs['Category'] = jobs['Category'].apply(clean_text)
jobs['Experience'] = jobs['Experience'].apply(clean_text)

# Lowercase
jobs['Skills'] = jobs['Skills'].apply(lambda x : x.lower())
jobs['Qualification'] = jobs['Qualification'].apply(lambda x : x.lower())
jobs['Category'] = jobs['Category'].apply(lambda x : x.lower())
jobs['Experience'] = jobs['Experience'].apply(lambda x : x.lower())


# Experience
jobs['Experience'] = jobs['Experience'].apply(lambda x: x.replace(" ", ""))




# Lemmitization

lemmatizer = WordNetLemmatizer()



def convert(text):
    # Tokenize the input text
    tokens = nltk.word_tokenize(text)
    
    # Lemmatize each token
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Join the lemmatized tokens back into a string
    lemmatized_text = " ".join(lemmatized_tokens)
    
    return lemmatized_text

jobs['Skills'] = jobs['Skills'].apply(convert)
jobs['Qualification'] = jobs['Qualification'].apply(convert)
jobs['Category'] = jobs['Category'].apply(convert)
jobs['Experience'] = jobs['Experience'].apply(convert)


#  job seeker data
user_qualification = input("Enter Qualification: ")
user_experience = input("Enter Experience: ")
user_skills = input("Enter Skills: ")

user_experience.replace(" ", "")
user_data = f"{user_qualification} {user_skills} {user_experience}"
user_data =   clean_text(user_data)
user_data = user_data.lower()
user_data = convert(user_data)


# Text Vectorization using TF-IDF

vectorizer = TfidfVectorizer(stop_words = 'english')
corpus = [user_data] + list(jobs['Qualification'] + ' '  + jobs['Skills'] + ' ' + jobs['Category'] +  ' ' + jobs['Experience'])
tfidf_matrix = vectorizer.fit_transform(corpus)

user_vector = tfidf_matrix[0]
job_vectors = tfidf_matrix[1:]


# cosine similarity

similarities = cosine_similarity(user_vector, job_vectors)
sorted_indices = similarities.argsort()[0][::-1]
num_recommendations = 20
recommended_jobs = jobs.iloc[sorted_indices[:num_recommendations]]
print(recommended_jobs['Description'])