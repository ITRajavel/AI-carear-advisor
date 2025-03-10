import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load the dataset
career_data = pd.read_csv("career_data.csv")

# Combine skills and education level for training
career_data["combined_features"] = career_data["Required Skills"] + " " + career_data["Education Level"]

# Convert text data into numerical vectors
vectorizer = TfidfVectorizer()
career_vectors = vectorizer.fit_transform(career_data["combined_features"])

# Save the trained model and vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(career_vectors, "career_vectors.pkl")
joblib.dump(career_data, "career_data.pkl")

print("Model training complete. Vectorizer and career vectors saved.")
