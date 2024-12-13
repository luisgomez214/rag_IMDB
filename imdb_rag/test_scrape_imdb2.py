import requests
from bs4 import BeautifulSoup

# List of URLs to scrape (provided by you)
url_list = [
    "https://www.rogerebert.com/reviews/wicked-film-review",
    "https://150film.blogspot.com/2024/11/wicked.html",
    "https://asliveroffilm.blogspot.com/2024/11/film-no-78-wicked-part-1-2024-18th-nov.html",
    "https://abcentertainment.co.in/wicked-2024-movie-review/",
    "https://www.accioncine.es/critica-wicked-parte-1",
    "https://ageofthegeek.org/2024/11/22/wicked-part-one-is-partially-wonderful-with-erivo-and-grande-well-worth-seeing-%e2%ad%90%ef%b8%8f%e2%ad%90%ef%b8%8f%e2%ad%90%ef%b8%8f/",
    "https://aisleseat.com/wicked.html",
    "https://www.youtube.com/watch?v=E-r1SkbW2Go",
    "https://allthingsfadra.com/wicked-movie-review/",
    "https://medium.com/amazing-cinema/wicked-part-i-881117d8ee9d",
    "https://anygoodfilms.com/wicked-part-one-review/",
    "https://www.withashleyandco.com/2024/11/wicked-review-ariana-grande-cynthia-erivo/",
    "https://awardswatch.com/wicked-review-cynthia-erivo-and-ariana-grande-will-sweep-you-off-your-feet-in-jon-m-chus-high-flying-musical-feast/",
    "https://www.backtothemovies.com/wicked-imax-review-believe-the-hype/",
    "https://www.bina007.com/2024/11/wicked-part-i.html",
    "https://spotifycreators-web.app.link/e/0yMyKMPvSOb",
    "https://www.blu-ray.com/Wicked/596245/#Review",
    "https://www.bollywoodhungama.com/movie/wicked-english/critic-review/wicked-english-movie-review/wicked-is-a-visually-stunning-musical-fantasy/",
    "https://boundingintocomics.com/movies/movie-reviews/wicked-review-a-bloated-screechy-symphony-straight-from-pink-and-green-hell/",
    "https://butwhytho.net/2024/11/wicked-movie-review/",
    "https://cailloupettismoviereviews.com/movies/wicked-film-review/",
    "https://caramiezone.blogspot.com/2024/11/critique-cinema-wicked.html",
    "https://www.caseymoviemania.com/wicked-2024-review/",
    "https://catwithmonocle.com/news/2024/11/19/wicked-review/",
    "https://www.cgmagonline.com/review/movie/wicked-2024-review/",
    "http://charitysplace.com/review/wicked1.htm",
    "https://www.cinefied.com/wickedmoviereview",
    "https://www.cinefilos.it/tutto-film/recensioni/wicked-cynthia-erivo-ariana-grande-656319",
    "https://cinemaaxis.com/2024/11/21/wicked/",
    "https://www.cinemabang.com/wicked.php",
    "https://cinemagavia.es/wicked-critica-pelicula-estreno-cine/",
    "https://cinemanerdz.com/movie-review-wicked-part-i/",
    "https://cineramafilm.com/2024/11/20/wicked-review/",
    "https://cinesthesiac.blogspot.com/2024/11/the-witches-wicked-part-1.html",
    "https://clutchpoints.com/wicked-ariana-grande-cynthia-erivo-2024-movie-review",
    "https://www.commonsensemedia.org/movie-reviews/wicked",
    "https://criticalia.com/pelicula/wicked",
    "https://culturemixonline.com/review-wicked-2024-starring-ariana-grande-cynthia-erivo-jonathan-bailey-bowen-yang-marissa-bode-the-voice-of-peter-dinklage-michelle-yeoh-and-jeff-goldblum/",
    "https://cuttothetake.com/review-wicked/",
    "https://darrens-world-of-entertainment.blogspot.com/2024/11/wicked-part-one-movie-review.html",
    "https://dcfilmdom.com/2024/11/wicked-part-i-movie-review/",
    "https://deadline.com/2024/11/wicked-review-cynthia-erivo-ariana-grande-movie-musical-adaptation-1236181476/",
    "https://dennisschwartzreviews.com/wicked-part-1-2024-b/",
    "https://www.detona.com/articulo/wicked-wicked-eua-2024",
    "https://www.digitaljournal.com/entertainment/review-wicked-part-i-is-fanciful-vibrant-and-incomplete/article",
    "https://www.disappointmentmedia.com/reviews/wicked-the-return-of-the-blockbuster-musical",
    "https://discussingfilm.net/2024/11/19/wicked-review-jon-m-chu-adaptation/",
    "https://www.doctorpopcorn.net/post/wicked-cynthia-erivo-and-ariana-grande-soar-in-entertaining-exciting-musical-adaptation",
    "https://dragonladyfiles.com/2024/11/22/wicked-not-all-wonderful/",
    "https://dvd-fever.co.uk/wicked-the-dvdfever-cinema-review-ariana-grande/",
    "https://dvdizzy.com/wicked/",
    "https://www.ecartelera.com/noticias/wicked-critica-jon-m-chu-musical-parte-1-79017/",
    "https://www.edb.co.il/blog/archives/34524",
    "https://film-authority.com/2024/11/19/wicked-part-1/",
    "https://film-book.com/film-review-wicked-part-1-2024-a-spectacular-musical-and-the-most-fun-youll-have-at-the-movies-this-year/",
    "https://filmfestivaltoday.com/#google_vignette",
    "https://filmfreakcentral.net/2024/11/wicked-2024/",
    "https://www.filmgeekguy.com/2024/11/wicked-movie-review-2024.html",
    "https://filmobsessive.com/film/new-releases/wicked-is-over-the-rainbow-excellence/",
    "https://www.filmreviewdaily.com/new-reviews/wicked",
    "https://filmreviewsbymark.com/2024/11/21/wicked-part-i/",
    "https://film-forward.com/musical/wicked",
    "https://www.filmstarts.de/kritiken/248289/kritik.html",
    "https://flickdirect.com/movie-review/3141/wicked/movie.ashx",
    "https://flixchatter.net/2024/11/21/flixchatter-review-wicked-part-i-2024-cynthia-erivo-ariana-grande-are-wicked-good-in-jon-m-chus-vivid-dazzling-and-surprisingly-heartfelt-movie-musical/",
    "https://freshfiction.tv/wicked-review-ariana-grande-and-cynthia-erivo-shine-bright-in-this-musical-masterpiece/",
    "https://galaxiadocinema.home.blog/2024/11/19/wicked-2024-e-um-espetaculo-de-imagem-e-som/",
    "https://gazettely.com/2024/11/entertainment/wicked-review/",
    "https://geekculture.co/wicked-review/",
    "https://gonewiththetwins.com/wicked-part-i-2024/",
    "https://good.film/guide/haters-will-tell-you-wicked-sucks-heres-why-theyre-wrong",
    "https://www.guyatthemovies.com/gatmhome/wicked-movie-review-cynthia-erivo-and-ariana-grande-bring-the-house-down-in-stunning-musical-adaptation",
    "https://www.heyuguys.com/wicked-part-i-review/",
    "https://hollywoodmoviesonafdah.blogspot.com/2024/11/wicked-review-with-romance-fantasy-and.html",
    "https://ifyouwantthegravy.wordpress.com/2024/11/29/the-weekly-gravy-218/",
    "https://influxmagazine.com/wicked-2024-review/",
    "https://www.irishfilmcritic.com/movie-review-theres-no-denying-that-wicked-will-be-extremely-popular-at-the-theaters/",
    "https://www.joblo.com/wicked-review-a-broadway-adaptation-thats-way-better-than-you-might-be-expecting/",
    "https://joshatthemovies.com/2024/11/19/film-review-wicked/",
    "https://keithlovesmovies.com/2024/11/19/wicked-early-review/",
    "https://www.kenkenreviews.com/wicked-part-1/",
    "https://kinoculturemontreal.com/wicked-part-one/",
    "https://kinotico.es/opinion/2024-11-22/critica-wicked-desafia-gravedad-colorido-y-esperanzador-homenaje-diversidad",
    "https://www.locchiodelcineasta.com/wicked-2024/",
    "https://laestatuilla.com/criticas/critica-de-wicked-ariana-grande-cynthia-erivo/",
    "https://lastonetoleavethetheatre.blogspot.com/2024/11/wicked.html",
    "https://thelatinoslant.com/movie-tv-reviews/wicked-is-a-triumphant-adaptation-movie-review/",
    "https://moviemovesme.com/2024/11/24/wicked-film-review-cynthia-erivo-and-ariana-grande-illuminate-the-untold-story-of-the-wicked-witch/",
    "https://letsgotothemovies.co.uk/2024/11/23/wicked-2024-review/",
    "https://www.lostincinema.it/recensioni/wicked-recensione/",
    "https://loudandclearreviews.com/wicked-2024-movie-review/",
    "https://alisechaffins.substack.com/p/wicked-review-part-1-movie-2024",
    "https://maddwolf.com/new-in-theaters/holiday-season-of-the-witch/",
    "http://www.markreviewsmovies.com/reviews/W/wicked-part1.htm",
    "https://www.youtube.com/watch?v=F6GHYQpT4gs",
    "http://metacultura.com.ar/la-maldad-naturalizada-y-justificada/",
    "https://montasefilm.com/wicked/2/",
    "https://www.moviearcher.com/2024-reviews/wicked",
    "https://www.nowplayingnetwork.net/moviemadness/episode520",
    "https://moviemeisterreviews.com/2024/11/25/wicked-part-one/",
    "http://moviefreak.com/wicked-part-one-2024-movie-review/",
    "https://www.moviementarios.com/critica-wicked/",
    "https://trustory.fm/movieswelike/re-recording-mixer-andy-nelson-on-butch-cassidy-and-the-sundance-kid-and-wicked/",
    "https://mundocine.es/critica-wicked",
    "https://www.serteli.com/2024/02/wicked.html",
    "https://www.new-video.de/film-wicked/",
    "https://outnow.ch/go/review/Wicked-PartOne/2024/",
    "https://www.papodecinema.com.br/filmes/wicked/",
    "https://parentpreviews.com/movie-reviews/wicked",
    "https://open.spotify.com/episode/6CVn64e2Yqrz3zuUCKeunU",
    "https://planetdave.com/2024/11/film-review-bewitchingly-entertaining-wicked/",
    "https://popculturemaniacs.com/wicked-review/",
    "https://popcornpodcast.com/episodes/wicked-review",
    "https://popcornreviewss.com/wicked-2024-movie-review/",
    "https://punchdrunkcritics.com/2024/11/wicked-57705/",
    "https://quinlan.it/2024/11/21/wicked/",
    "https://youtu.be/p5-1vNOCANs?si=ySK6w8DmXKs5eA7u",
    "https://www.razorfine.com/movie-reviews/wicked-part-i/",
    "https://www.youtube.com/watch?v=4QZVHS21x4Q",
    "https://www.reelingreviews.com/reviews/wicked/",
    "https://rendyreviews.com/movie-reviews/wicked-review",
    "https://open.spotify.com/episode/7Htx6OwG8HSSU7Cemmby3y",
    "https://www.ruthlessreviews.com/movies/wicked-part-one-2024/",
    "https://sarahgvincentviews.com/movies/wicked/",
    "https://skonmovies.com/review/wicked-part-one/",
    "https://www.youtube.com/watch?v=GeG_tpXgBTs",
    "https://www.youtube.com/watch?v=vAAtzxwP-KQ",
    "https://www.sknr.net/2024/11/19/wicked-is-a-modern-masterpiece-for-the-entire-family/",
    "https://www.slantmagazine.com/film/wicked-review-cynthia-erivo-ariana-grande-jonathan-bailey/",
    "https://www.slashfilm.com/1713820/wicked-movie-review/",
    "https://solzyatthemovies.com/2024/11/20/wicked-part-one-defies-gravity/",
    "https://sonic-cinema.com/wordpress/movie/wicked/",
    "https://spoilerfreereviews.com/post/wicked/?utm_source=IMDb&utm_medium=IMDb/",
    "https://spoilerfreereviews.com/post/wicked-2/?utm_source=IMDb&utm_medium=IMDb/",
    "https://youtube.com/shorts/7-sF1TuZZgY",
    "https://www.stevepulaski.com/2024/11/27/wicked-part-i-2024-review/",
    "https://www.maketheswitch.com.au/article/review-wicked-a-movie-musical-that-defies-gravity",
    "https://thatshelf.com/the-wicked-cast-and-crew-on-defying-gravity-in-their-movie-musical/",
    "https://thatdarngirlmovie.reviews/2024/11/19/wickedmovie-movie-review/",
    "https://kristenlopez.substack.com/p/wicked-review-cynthia-erivo",
    "https://thefilmverdict.com/wicked-film-review-2024-part-one/",
    "https://www.thefriendlyfilmfan.com/news--reviews/review-wicked-jon-m-chu-adapts-act-one-of-beloved-stage-musical-to-astoundifying-effect",
    "https://www.theguardian.com/film/2024/nov/19/wicked-review-cynthia-erivo-ariana-grande-wizard-of-oz-stephen-schwartz",
    "https://www.theguardian.com/film/2024/nov/24/wicked-the-film-review-cynthia-erivo-and-ariana-grande-jon-m-chu-part-one-1",
    "https://www.thehollywoodoutsider.com/wicked-2024-film-review/",
    "https://www.hollywoodreporter.com/movies/movie-reviews/wicked-review-cynthia-erivo-ariana-grande-1236062372/",
    "https://theindependentcritic.com/wicked_part_one",
    "https://joethemnmovieman.com/2024/11/19/wicked2024/",
    "https://www.themoviebuff.net/2024/11/wicked-review-an-epic-deeply-moving-flawless-translation-of-the-stage-musical-to-screen/",
    "https://www.theonlycritic.com/post/wicked-review-erivo-and-grande-bring-the-magic-in-exhilarating-musical-adaptation",
    "https://tldrmoviereviews.com/2024/11/20/wicked-wicked-part-1-movie-review/",
    "https://www.universalmovies.it/wicked-recensione-film-musical/",
    "https://variety.com/2024/film/reviews/wicked-review-cynthia-erivo-ariana-grande-1236214272/",
    "https://thecraggus.com/2024/11/24/wicked-2024-review/",
    "https://medium.com/@afdahfreemovies/wicked-2024-review-96d13915d055",
    "https://writerofpop.com/2024/11/20/although-long-wicked-is-a-near-perfect-musical/",
    "https://www.youtube.com/watch?v=IYtRO5S9g1k",
    "https://www.zekefilm.org/2024/11/22/wicked-part-one-film-review/",
]


import sqlite3
import requests
from bs4 import BeautifulSoup
from langdetect import detect
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # INFO for general progress, DEBUG for detailed output

def create_db(db_name="reviews.db"):
    """Create a new SQLite database and the reviews table."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Drop the table if it already exists (to avoid conflicts)
    cursor.execute('DROP TABLE IF EXISTS reviews')

    # Create the reviews table with the 'date' column
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

def add_date_column(db_name="reviews.db"):
    """Add the 'date' column to the reviews table if it's missing."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute('ALTER TABLE reviews ADD COLUMN date TEXT')
        conn.commit()
        print("Column 'date' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error adding column: {e}")
    finally:
        conn.close()

def insert_review(db_name, title, date, language, review_text):
    """Insert a review into the SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert the review into the table
    cursor.execute('''
        INSERT INTO reviews (title, date, original_language, review)
        VALUES (?, ?, ?, ?)
    ''', (title, date, language, review_text))
    
    conn.commit()
    conn.close()

def extract_review_text(soup):
    """Extract review text from different HTML elements."""
    review_text = ''
    
    # First attempt: <p> tags (common for plain text reviews)
    paragraphs = soup.find_all('p')
    review_text += '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
    
    # Additional common places for reviews
    review_containers = [
        {'tag': 'div', 'class': 'review-text'},
        {'tag': 'div', 'class': 'review-body'},
        {'tag': 'span', 'class': 'review-content'},
        {'tag': 'section', 'class': 'review-section'},
        {'tag': 'div', 'itemprop': 'reviewBody'}
    ]
    
    # Iterate through all containers and extract text
    for container in review_containers:
        elements = soup.find_all(container['tag'], class_=container.get('class'), itemprop=container.get('itemprop'))
        for element in elements:
            review_text += '\n' + element.get_text(strip=True)
    
    return review_text.strip()

def scrape_and_save_reviews(url_list, db_name="reviews.db"):
    """Scrape reviews and save them to an SQL database."""
    
    # Uncomment the solution you want to use:
    
    # Solution 1: Drop and recreate the table with the correct schema
    create_db(db_name)
    
    # Solution 2: Add the missing 'date' column (uncomment if you don't want to drop the table)
    # add_date_column(db_name)
    
    error_count = 0  # To keep track of total errors
    for idx, url in enumerate(url_list, 1):  # Adding index for ID
        try:
            # Request the page content
            response = requests.get(url)
            response.raise_for_status()  # Will raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title - assuming the title is in the <title> tag
            title_tag = soup.find('title')
            title = title_tag.text.strip() if title_tag else 'No title found'

            # Extract the date of the review (looking for <time> or meta tags)
            date_tag = soup.find('time')
            date = date_tag.text.strip() if date_tag else 'Date not found'

            # Extract review text from various locations
            review_text = extract_review_text(soup)

            # Skip empty reviews
            if not review_text.strip():  # If review text is empty or contains only whitespace
                logging.warning(f"Review ID {idx} has no text, skipping.")
                continue

            # Detect language of the review text
            try:
                language = detect(review_text)
            except Exception as e:
                language = 'Unknown'
                logging.error(f"Error detecting language for Review ID {idx}: {e}")

            # Print the ID, title, date, language, and review text (if needed)
            print(f"\n--- Review ID: {idx} ---")
            print(f"Title: {title}")
            print(f"Date: {date}")
            print(f"Detected Language: {language}")
            print("Full review text:\n")
            print(review_text)

            # Insert the review into the database
            insert_review(db_name, title, date, language, review_text)

        except requests.exceptions.RequestException as e:
            error_count += 1
            # Print the error message to the console
            print(f"\nError retrieving {url}: {e}")

    print(f"\nTotal Errors Encountered: {error_count}")

scrape_and_save_reviews(url_list, db_name="reviews.db")
