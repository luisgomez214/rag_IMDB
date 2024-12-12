import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from test3 import rag  # Import the RAG function
from test3 import MovieDB
import time
import random
import re
from nltk.stem import WordNetLemmatizer

# Initialize lemmatizer for word normalization
lemmatizer = WordNetLemmatizer()

class MovieRAGEvaluator:
    def __init__(self, db_path='reviews.db', model_name='all-MiniLM-L6-v2'):
        """
        Initialize the evaluator with a database connection and a sentence transformer model.
        """
        self.db = MovieDB(db_path)
        self.model = SentenceTransformer(model_name)

    def predict(self, question):
        """
        Predict the answer to a question using the RAG-based system.
        """
        output = rag(question, self.db)

        # Retry if the prediction is empty
        if not output.strip():
            print(f"Empty prediction for: {question}. Retrying...")
            time.sleep(random.uniform(0.5, 1.5))
            output = rag(question, self.db)
            if not output.strip():
                return "Sorry, I couldn't generate an answer. Please try again later."

        return output.strip()

    def normalize_answer(self, answer):
        """
        Normalize the answer for consistent comparison:
        - Lowercase
        - Remove punctuation
        - Lemmatize words
        """
        # Lowercase, remove extra spaces, remove punctuation
        answer = answer.lower().strip()
        answer = re.sub(r'[^\w\s]', '', answer)
        # Lemmatize words for better comparison
        answer = ' '.join([lemmatizer.lemmatize(word) for word in answer.split()])
        return answer

    def calculate_semantic_similarity(self, predicted_answer, expected_answer):
        """
        Compute semantic similarity between predicted and expected answers using sentence embeddings.
        """
        embeddings = self.model.encode([predicted_answer, expected_answer])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return similarity

    def calculate_partial_similarity(self, predicted_answer, expected_answer):
        """
        A simple method for partial matching by comparing important concepts (keywords).
        """
        # Split answers into words and normalize
        pred_tokens = set(self.normalize_answer(predicted_answer).split())
        exp_tokens = set(self.normalize_answer(expected_answer).split())

        # Find the intersection of tokens (core concepts)
        common_tokens = pred_tokens.intersection(exp_tokens)
        
        # Return the ratio of common tokens to total tokens in the expected answer
        partial_similarity = len(common_tokens) / len(exp_tokens) if len(exp_tokens) > 0 else 0
        return partial_similarity

    def evaluate_answer(self, predicted_answer, expected_answer, threshold=0.6, partial_threshold=0.8):
        """
        Evaluate the correctness of a prediction based on semantic similarity and partial keyword matching.
        """
        # Normalize both answers
        normalized_pred = self.normalize_answer(predicted_answer)
        normalized_exp = self.normalize_answer(expected_answer)

        # Calculate semantic similarity
        semantic_similarity = self.calculate_semantic_similarity(normalized_pred, normalized_exp)

        # Calculate partial keyword-based similarity
        partial_similarity = self.calculate_partial_similarity(predicted_answer, expected_answer)

        # Check if either similarity exceeds the thresholds
        if semantic_similarity >= threshold or partial_similarity >= partial_threshold:
            return "Overall correct", semantic_similarity, partial_similarity
        else:
            return "Incorrect", semantic_similarity, partial_similarity


def load_test_data(filepath):
    """
    Load test data from a JSON file.
    """
    with open(filepath, 'r') as file:
        return json.load(file)


def evaluate_predictions(data, db_path='reviews.db', threshold=0.6, partial_threshold=0.8):
    """
    Evaluate predictions for all questions in the test dataset.
    """
    evaluator = MovieRAGEvaluator(db_path)
    total = len(data)
    correct = 0
    total_similarity = 0
    total_partial_similarity = 0

    for entry in data:
        question = entry['question']
        expected_answer = entry['expected_answer']

        # Get the predicted answer from the system
        prediction = evaluator.predict(question)

        # Evaluate similarity between predicted and expected answer
        result, semantic_similarity, partial_similarity = evaluator.evaluate_answer(prediction, expected_answer)

        # Track correct answers and total similarity
        if result == "Overall correct":
            correct += 1
        total_similarity += semantic_similarity
        total_partial_similarity += partial_similarity

        # Output evaluation results
        print(f"Question: {question}")
        print(f"Expected: {expected_answer}")
        print(f"Predicted: {prediction}")
        print(f"Result: {result}")
        print(f"Semantic Similarity: {semantic_similarity:.4f}")
        print(f"Partial Similarity: {partial_similarity:.4f}")
        print()

    # Print overall accuracy and average similarity
    avg_similarity = total_similarity / total if total > 0 else 0
    avg_partial_similarity = total_partial_similarity / total if total > 0 else 0
    accuracy = correct / total if total > 0 else 0

    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Average Semantic Similarity: {avg_similarity:.4f}")
    print(f"Average Partial Similarity: {avg_partial_similarity:.4f}")


if __name__ == "__main__":
    filepath = 'wickedEasy.json'  # Path to your test data file
    data = load_test_data(filepath)
    evaluate_predictions(data, db_path='reviews.db')

