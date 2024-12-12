import os
import re
import logging
import sqlite3
import datetime
import argparse
from urllib.parse import urlparse
from langdetect import detect
from groq import Groq

################################################################################
# LLM functions
################################################################################

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def run_llm(system, user, model='llama3-8b-8192', seed=None):    #('llama3-8b-8192', seed=None):  
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': system,
            },
            {
                "role": "user",
                "content": user,
            }
        ],
        model=model,
        seed=seed,
    )
    return chat_completion.choices[0].message.content

def summarize_text(text, seed=None):
    """
    Summarize the movie review text in one concise paragraph, ensuring the summary reflects the core plot,
    major themes (love, sacrifice, power, friendship), and the emotional arc (e.g., tragic, uplifting) of 'Wicked'.
    The summary should include character relationships, key moments, and any notable performances.
    """
    system = '''Summarize the following movie review for the 2024 film "Wicked". Provide a concise and informative summary, including:
    - The central plot and key events.
    - Key themes.
    - Significant character relationships and emotional arcs.
    - The tone of the movie, whether tragic, uplifting, intense, or otherwise.
    - Important people in the development of the movie such as directors, actors, composers, writers, staff.
    - Remember the original language each review is in.
    Focus on providing a factual, accurate summary that highlights important moments, themes, and performances.'''
    
    return run_llm(system, text, seed=seed)


def translate_text(text, target_language="en"):
    """
    Translate the given movie review text into the target language, while also preserving the context of the original language.
    The translation should be professional and suitable for formal contexts.
    """
    system = f'''You are a professional translator working for the United Nations. The following text is an important movie 
    review that needs to be translated into {target_language}. Provide a professional, accurate, and contextually appropriate translation, 
    preserving the original meaning, tone, and style. Remember the original language each review is in.'''
    
    return run_llm(system, text)


def extract_keywords(text, seed=None):
    """
    Extract a comprehensive list of keywords from the movie review, focusing on specific elements of 'Wicked' (2024).
    This includes character names, themes, emotional tones, key plot events, and other significant references.
    """
    system_prompt = '''Extract relevant keywords and phrases from the following movie review of 'Wicked' (2024). Focus on:
    - Character names.
    - Themes.
    - Emotional tones.
    - Key plot events.
    - Specific references to locations and time (e.g., key moments in the story).
    Only provide a space-separated list of relevant keywords. Avoid adding explanations, comments, punctuation, or any additional text.
    Exclude filler words and focus on significant nouns, verbs, adjectives, and key emotional descriptions.'''
    
    user_prompt = f"Extract keywords from the following text: {text}"

    # Use the run_llm function to get the extracted keywords
    keywords = run_llm(system_prompt, user_prompt, seed=seed)

    # Return the keywords as a space-separated string
    return keywords

import re

def extract_from_review_llm(review_text, seed=None):
    """
    Extract key details from the review content using an LLM.
    """
    system_prompt = '''
    Extract key movie details from the following review. Include:
    - Director(s)
    - Cast
    - Release date (year or full date)
    - Runtime (in minutes)
    - Themes (brief description)
    - Awards (if mentioned)
    - Genre
    - Production company
    - Country
    - Language(s)
    - Box office or gross revenue (if mentioned).
    - Animators    

    Output each detail in this format (leave blank if not found):
    - Director: 
    - Cast: 
    - Release Date: 
    - Runtime: 
    - Themes: 
    - Awards: 
    - Genre: 
    - Production Company: 
    - Country: 
    - Language: 
    - Box Office:
    - Animators: 
    '''
    user_prompt = f"Review Text: {review_text}"

    extracted_details = run_llm(system_prompt, user_prompt, seed=seed)

    details = {key.lower(): "Not Found" for key in [
        "Director", "Cast", "Release Date", "Runtime", "Themes", "Awards", 
        "Genre", "Production Company", "Country", "Language", "Box Office"
    ]}

    for line in extracted_details.splitlines():
        key, _, value = line.partition(": ")
        if key.lower() in details:
            details[key.lower()] = value.strip() if value.strip() else "Not Found"

    return details

#def extract_from_review(review_text):
    """
    Extract key details from the review content using regex.
    This is generalized to accommodate a wide range of potential movie-related questions.
    """
    # Refined regex patterns for different possible movie-related questions
    director_pattern = r"(?i)\b(directed|director[:\s]+)([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)"
    cast_pattern = r"(?i)\b(starring|stars|cast|played|plays|as[:\s]+)([A-Za-z, ]+)"
    release_date_pattern = r"(?i)\b(release|date|year|month[:\s]*|released)\s*(\d{4}|[A-Za-z]+\s+\d{4})"
    runtime_pattern = r"(?i)\b(runtime|length|long[:\s]*)(\d{1,3})\s*(minutes|mins)"
    theme_pattern = r"(?i)\b(themes?|explores|focuses|plot|message)[:\s]*([\w\s,]+)"
    award_pattern = r"(?i)\b(awards?|accolades?)[:\s]*([\w\s,]+)"
    genre_pattern = r"(?i)\b(genre|type[:\s]*)([\w\s,]+)"
    production_company_pattern = r"(?i)\b(produced|production[:\s]+)([A-Za-z\s]+)"
    country_pattern = r"(?i)\b(country|filmed in[:\s]*)([A-Za-z\s]+)"
    language_pattern = r"(?i)\b(language|languages|spoken[:\s]*)([A-Za-z\s]+)"
    box_office_pattern = r"(?i)\b(box|gross|revenue|made[:\s]*)([0-9\.,]+)"

    # Extract metadata using regex search
    director = re.search(director_pattern, review_text)
    cast = re.search(cast_pattern, review_text)
    release_date = re.search(release_date_pattern, review_text)
    runtime = re.search(runtime_pattern, review_text)
    themes = re.search(theme_pattern, review_text)
    awards = re.search(award_pattern, review_text)
    genre = re.search(genre_pattern, review_text)
    production_company = re.search(production_company_pattern, review_text)
    country = re.search(country_pattern, review_text)
    language = re.search(language_pattern, review_text)
    box_office = re.search(box_office_pattern, review_text)

    # Return metadata in a dictionary
    return {
        "director": director.group(2) if director else "Not Found",
        "cast": cast.group(2) if cast else "Not Found",
        "release_date": release_date.group(2) if release_date else "Not Found",
        "runtime": runtime.group(2) + " minutes" if runtime else "Not Found",
        "themes": themes.group(2) if themes else "Not Found",
        "awards": awards.group(2) if awards else "Not Found",
        "genre": genre.group(2) if genre else "Not Found",
        "production_company": production_company.group(2) if production_company else "Not Found",
        "country": country.group(2) if country else "Not Found",
        "language": language.group(2) if language else "Not Found",
        "box_office": box_office.group(2) if box_office else "Not Found"
    }




################################################################################
# MovieDB class for SQLite-based Database
################################################################################

class MovieDB:
    def __init__(self, db_name='reviews.db'):
        self.db_name = db_name
        self.logger = logging
        self._initialize_db()

    def _initialize_db(self):
        """
        Initialize the SQLite database.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                title TEXT,
                date TEXT,
                original_language TEXT,
                review TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def find_movies(self, query, limit=10):
        """
        Find movies in the SQLite database that match the query.
        This function uses a simple keyword match on the title and review fields.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, review FROM reviews
            WHERE title LIKE ? OR review LIKE ?
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        movies = cursor.fetchall()
        conn.close()
        return movies

    def add_movie(self, title, description, date, language):
        """
        Add a new movie to the SQLite database.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (title, date, original_language, review)
            VALUES (?, ?, ?, ?)
        ''', (title, date, language, description))
        conn.commit()
        conn.close()

    def __len__(self):
        """ Return the number of movies in the database """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM reviews')
        count = cursor.fetchone()[0]
        conn.close()
        return count

################################################################################
# RAG function
################################################################################

def rag(question, db):
    """
    Improved RAG function for answering movie-related questions and providing feedback.
    """
    # Extract reviews for the query
    reviews = db.find_movies("Wicked", limit=5)
    combined_text = " ".join([review[1] for review in reviews])

    # Translate the text to English
    translated_text = translate_text(combined_text, target_language="en")

    # Extract metadata using the translated text
    llm_metadata = extract_from_review_llm(translated_text)

    # Summarize the translated reviews for detailed context
    review_summary = summarize_text(translated_text)

    # Generate feedback on the reviews
    feedback_prompt = (
        f"You are a movie critic and feedback expert. Based on the provided review summaries and metadata, "
        f"analyze the movie's reception and provide constructive feedback for its creators. Focus on:\n"
        f"- Whether the movie meets expectations for its genre.\n"
        f"- Strengths in storytelling, visuals, and performances.\n"
        f"- Areas for improvement in pacing, tone, or character development.\n\n"
        f"Metadata:\n{llm_metadata}\n\n"
        f"Review Summaries:\n{review_summary}\n\n"
        f"Provide your feedback in a professional and insightful tone."
    )
    feedback = run_llm(system=feedback_prompt, user="Generate feedback")

    # Construct dynamic prompt for answering the question
    prompt = (
        f"You are a movie expert specializing in the movie 'Wicked' released in 2024. "
        f"Answer the following question based on the provided metadata, summaries, and feedback:\n\n"
        f"LLM Metadata:\n{llm_metadata}\n\n"
        f"Review Summaries:\n{review_summary}\n\n"
        f"Feedback:\n{feedback}\n\n"
        f"Question: {question}\n\n"
        f"Provide a concise, accurate response based on the provided data."
    )

    # Use LLM to generate the answer
    response = run_llm(system=prompt, user=question)
    return response


#def rag(question, db):
    """
    Improved RAG function for answering movie-related questions.
    """
    # Extract metadata from reviews
    reviews = db.find_movies("Wicked")
    combined_text = " ".join([review[1] for review in reviews])
    metadata = extract_from_review(combined_text)

    # Summarize reviews for detailed context
    review_summary = summarize_text(combined_text)

    # Construct dynamic prompt
    prompt = (
        f"You are a movie expert specializing in 'Wicked' (2024). "
        f"Answer the following question based on the provided metadata and review summaries:\n\n"
        f"Metadata:\n{metadata}\n\n"
        f"Review Summaries:\n{review_summary}\n\n"
        f"Question: {question}\n\n"
        f"Provide a concise, accurate response based on the provided data."
    )

    # Use LLM to generate the answer
    response = run_llm(system=prompt, user=question)
    #return response


################################################################################
# CLI Interface
################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interactive QA with movie database (SQLite).')
    parser.add_argument('--loglevel', default='warning')
    parser.add_argument('--db', default='reviews.db')  # Use the SQLite DB file here
    parser.add_argument('--add_movie', nargs=4, metavar=('TITLE', 'DESCRIPTION', 'DATE', 'LANGUAGE'))
    parser.add_argument('--query', help='Query for interactive QA')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=args.loglevel.upper(),
    )

    db = MovieDB(args.db)

    if args.add_movie:
        title, description, date, language = args.add_movie
        db.add_movie(title, description, date, language)
        print(f"Movie '{title}' added to database.")
    elif args.query:
        output = rag(args.query, db)
        print(output)
    else:
        import readline
        while True:
            text = input('movie_rag> ')
            if len(text.strip()) > 0:
                output = rag(text, db)
                print(output)
