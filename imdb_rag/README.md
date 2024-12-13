# Overview
On IMDb, there is a section called "Reviews" where members share their ratings and written reviews of movies and shows. Another section, titled "External Reviews," provides links to other sites with additional reviews, but only as links, without offering users any immediate insights. My goal is to enhance this experience by creating a chatbot that users can interact with based on the content of these reviews.

The LLM used for this system is Groq llama, the language model is not up to date with information from recently released movies. The reason why this model was used is because the goal is to provde users with information that are strictly based on the reviews from the links. Up to date models will already have review and critic information in its training set, making the goal difficult to achieve. 

This system focuses on the 2024 movie 'Wicked' but can easily be used for other movies. Simply switch the links on 'test_scrape_imdb.py'.


# Setup

First scrape all the links found in the 'External Reviews' (the ones I used are 'https://www.imdb.com/title/tt1262426/externalreviews/?ref_=tt_ov_crv'). I used a software called ParseHub. 
Once all new links have been retrieved, replace the current links in 'test_scrape_imdb.py' with the new ones. 

Then run: 
```
python3 test_scrape_imdb.py 
```

# Database

Once 'test_scrape_imdb.py' has been ran, a SQL database is made. The contents of the database are
```
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            title TEXT,
            date TEXT,
            original_language TEXT,
            review TEXT
        )
    ''')
```
id, title, date, the original language of the text, and the review itself

Over 70% of the links were abled to be added to the database. Some are excluded due to the websites privacy restrictions or because of formatting issues.

Now, setup your GROQ API KEY:
```
export GROQ_API_KEY=
```


# Examples
**Example 1: Answer Questions Based on Summary**

The system can answer simple summazation question based on the external reviews.  

Example 1: 
```
luis@Luiss-MacBook-Pro-40 finalproj % python3 -i test3.py                                                         
movie_rag> Who are the stars of the 2024 movie Wicked?
The stars of the 2024 movie Wicked are:

1. Cynthia Erivo (Elphaba)
2. Ariana Grande (Galinda)
3. Michelle Yeoh (Madam Morrible)
4. Jeff Goldblum (Wizard)
5. Jonathan Bailey (Fiyero)
```

**Example 2: Answer Questions Based on Critics Opnions**

Beyond text summazation, the system can answer questions based on opinions. 

Example 2:
```
movie_rag> Did critics have a good or bad review of the 2024 movie Wicked?
Critics had a generally positive review of the 2024 movie Wicked. The feedback described it as visually stunning, musically captivating, and emotionally resonant. They praised the strong performances of the cast, particularly Cynthia Erivo and Ariana Grande, as well as the production design, costume design, and music.
```

```
movie_rag> What did critics think were some of the issues with the 2024 movie Wicked?
According to the review summaries and feedback, critics noted the following issues with the 2024 movie Wicked:

1. Pacing: The film felt slightly slow or plodding at times, with some scenes that could be trimmed or edited to maintain a consistent tempo.
2. Tone: The tone was occasionally inconsistent or uneven, with moments that didn't quite match the overall light and playful tone of the film.
3. Character Relationships: Some supporting characters in the movie felt underdeveloped, and critics recommended adding more depth or nuance to these characters to enrich the story and create a more complex narrative.
```

# Evaluate: 
To evaluate the system, both partial and semantic similarities were used. The threshold for semantic was at least .6 and for partial at least .8. If the predicted matched by either of those thresholds, then it is counted as correct. At times, "vague" or "broad" questions will give different answers than what was expected. For example "What did crtics think of Ariana Grande's performance in the 2024 movie Wicked." Will result in a different answer every time because there are many things critics could talk about regarding her performance.  

Below is the results: 
```
luis@Luiss-MacBook-Pro-40 finalproj % python3 evaluate_easy.py
Question: How does the 2024 movie Wicked differ from the Broadway musical?
Expected: While the movie remains largely faithful to the musical, it expands on the visual storytelling with more elaborate settings and cinematography. Some scenes are adjusted for the screen format, and a few new dialogues were added to enhance character depth.
Predicted: Although not explicitly stated in the provided review summaries and metadata, based on generic knowledge about the production, it can be inferred that the 2024 movie "Wicked" is a film adaptation of the iconic Broadway musical of the same name. 

Some differences between the movie and the Broadway musical "Wicked" include:

1. **Transition from Stage to Screen:** The movie "Wicked" is a filming adaptation of the stage production, meaning the format of the storytelling has changed from live performances to a cinematic experience. This shift could result in visual and narrative changes.

2. **Enhanced Visuals:** With a movie adaptation, the creative team likely had more resources at their disposal for elaborate sets, visual effects, and cinematography, which could enhance the overall visual experience.

3. **Interpretation of Musical Numbers:** The stage production has impressive musical numbers performed live by the cast and orchestra. The movie version might have made some adjustments to the song arrangements, choreography, or even potentially using post-production elements to emphasize certain aspects.

4. **Screenplay and Narrative Adjustments:** In the movie adaptation, there might be minor adjustments in the storytelling to better accommodate a two-hour cinematic format, including scenes that wouldn't have been feasible in a stage production due to time and space constraints.

5. **Extension of Emotional Resonance:** The film adaptation could delve deeper into the emotions and character development of certain characters due to a more dynamic audio-visual storytelling approach.

Please note that the differences mentioned are speculative, and since specific information about the stage production of "Wicked" isn't available in the provided data, this answer is based on commonly anticipated changes in moving a stage production to the big screen.
Result: Overall correct
Semantic Similarity: 0.6259
Partial Similarity: 0.6286

Question: What are critics saying about the performances in the 2024 movie Wicked?
Expected: Critics praise Cynthia Erivo and Ariana Grande for their emotionally charged and vocally impressive performances, highlighting their chemistry and individual depth.
Predicted: Critic's consensus suggests that Cynthia Erivo shines as Elphaba, bringing a compelling sense of vulnerability and ferocity to the role, while Ariana Grande impresses as Glinda, capturing the complexities of her character with ease.
Result: Overall correct
Semantic Similarity: 0.6916
Partial Similarity: 0.3333

Question: How do critics describe the direction of Jon M. Chu in the 2024 movie Wicked?
Expected: Critics commend Jon M. Chu for his visionary direction, blending vibrant visuals with heartfelt storytelling to bring Oz to life in a compelling way.
Predicted: Critics describe the direction of Jon M. Chu in the 2024 movie Wicked as "well-crafted" and skillful in translating the stage musical to the big screen. He effectively captures the essence of the genre, blending elements of fantasy, adventure, and drama to create an engaging story. However, some viewers might find the pacing slightly uneven, particularly during the first act.
Result: Overall correct
Semantic Similarity: 0.6025
Partial Similarity: 0.3913

Question: What are the critical opinions on the visual effects of the 2024 movie Wicked?
Expected: Critics have lauded the stunning visual effects, particularly the depiction of the Emerald City and the seamless integration of practical sets and CGI.
Predicted: Unfortunately, I was not provided with a direct mention on the movie Wicked's visual effects in the feedback summary provided.
Result: Incorrect
Semantic Similarity: 0.4579
Partial Similarity: 0.1667

Question: What aspects of the 2024 movie Wicked have received mixed reviews from critics?
Expected: Some critics have expressed mixed feelings about the pacing of the movie and the inclusion of new scenes that diverge slightly from the Broadway musical.
Predicted: Several aspects of the 2024 movie Wicked have received mixed reviews from critics, including:

1. **Pacing**: Some critics have mentioned that the film's 2.5-hour runtime can feel slow-paced at times.
2. **Tone**: Critics have noted that the film sometimes veers into overly sentimental or melodramatic territory, which may be off-putting for some viewers.
3. **Development of supporting characters**: While the focus on Elphaba and Glinda is well-executed, some critics have suggested that the supporting characters, such as the Wizard and the university's director, could be fleshed out more to add depth to the narrative.
4. **Thematic balance**: Critics have cautioned against overemphasizing any one theme, which could overshadow the main ideas explored in the film.

These criticisms suggest that while Wicked has many strengths, there is room for improvement in certain areas.
Result: Incorrect
Semantic Similarity: 0.4841
Partial Similarity: 0.5238

Question: How do critics view the music in the 2024 movie Wicked?
Expected: Critics unanimously praise the music, particularly iconic songs like 'Defying Gravity,' for their emotional resonance and ability to drive the narrative.
Predicted: The music in the 2024 movie "Wicked" is seen as a major strength by the critics.  They describe John Powell and Stephen Schwartz's (who composed the songs from the musical) work as memorable, charming, and well-integrated into the film. There are no negative comments found stating the music had to be improved or rewritten.
Result: Incorrect
Semantic Similarity: 0.4942
Partial Similarity: 0.3000

Question: What is the overall critical reception of the 2024 movie Wicked?
Expected: The movie has received largely positive reviews, with critics celebrating its faithful adaptation, strong performances, and visual splendor, though some note its slight departure in tone from the Broadway original.
Predicted: The overall critical reception of the 2024 movie Wicked is generally positive, with praise for its visually stunning production, impressive performances, and memorable musical numbers. However, some critics have noted that it sometimes struggles to balance tone, character development, and thematic consistency, which prevents it from reaching its full potential. Overall, the movie has received a rating of 4 out of 5 stars, indicating that it is well-received by critics but has room for improvement.
Result: Overall correct
Semantic Similarity: 0.6751
Partial Similarity: 0.4643

Question: What do critics think about the movie's exploration of moral ambiguity in Wicked?
Expected: Critics appreciate the nuanced portrayal of moral ambiguity, applauding the movie's ability to challenge traditional notions of good and evil.
Predicted: According to the feedback provided for "Wicked", critics think that the movie skillfully explores the themes of "the nature of good and evil". However, there is no specific critique on how well or poorly it handles moral ambiguity. Nevertheless, it is mentioned that the movie captures 'the complexities' of the characters very effectively, which suggests that critics appreciate the nuance it brings to the storytelling.
Result: Overall correct
Semantic Similarity: 0.7977
Partial Similarity: 0.6111

Question: How do critics compare the movie Wicked to other recent musical adaptations?
Expected: Critics place Wicked among the top musical adaptations, citing its ambitious production values and emotional depth as standout features compared to other recent releases.
Predicted: According to the feedback provided, critics do not explicitly compare Wicked to other recent musical adaptations. However, based on similar genre reviews from critics, recent musical adaptations with high musical or fantasy elements often have the following trends: 

1. Critiques of pacing, tone, or characterization can sometimes be too similar in musical adaptations.
2. New musical adaptations offer improved visuals and have the potential to add new ideas into a story.
3. The original concept or content can make or break an otherwise great adaptation.

With these trends in mind, assuming some musical adaptations might indeed have varying quality or common pitfalls, I will posit a guess for potential criticism of Wicked, using critical context found in reviews of similar movies: 

In comparison to other recent musical adaptations, critics might find Wicked's greatest strength to be its strong character development and world-building, similar to films such as Chicago (2002), Les Misérables (2012), or Hamilton (2020). The movie's emotional resonance and engaging storyline could make it stand out among musical adaptations, similar to projects like Mamma Mia! (2008) or The Greatest Showman (2017). However, the pacing and tone might be criticized for being inconsistent, much like in some other big-budget musical adaptations, such as Phantom of the Paradise (2023), American Buffalo (in development) etc. 

Please note that I've drawn parallels based on genre trends and the absence of direct comparisons in the feedback. Actual reviews of Wicked would provide a more accurate answer to this question.
Result: Overall correct
Semantic Similarity: 0.8062
Partial Similarity: 0.5417

Question: What elements of the 2024 movie Wicked have been described as innovative by critics?
Expected: Critics highlight the innovative camera work, dynamic choreography, and the seamless blending of live-action and animation as groundbreaking elements.
Predicted: Critics have not explicitly described specific elements of the movie "Wicked" (2024) as "innovative." However, they have praised the film's production design, led by Nathan Crowley, for transporting viewers to the Land of Oz with vibrant colors, intricate sets, and clever use of special effects.
Result: Incorrect
Semantic Similarity: 0.3404
Partial Similarity: 0.4118

Question: What do critics say about the balance of humor and drama in the 2024 movie Wicked?
Expected: Critics appreciate the balance of humor and drama, noting how the lighter moments enhance the emotional impact of the movie's dramatic scenes.
Predicted: The provided data does not explicitly mention the critics' opinions on the balance of humor and drama in the 2024 movie Wicked.
Result: Overall correct
Semantic Similarity: 0.6250
Partial Similarity: 0.4444

Question: Who directed the 2024 movie Wicked?
Expected: Jon M. Chu
Predicted: According to the Review Summaries: The director of the 2024 movie "Wicked" is Jon M. Chu.
Result: Overall correct
Semantic Similarity: 0.5650
Partial Similarity: 1.0000

Question: Who plays Glinda in the 2024 movie Wicked?
Expected: Ariana Grande
Predicted: Ariana Grande plays Glinda in the 2024 movie "Wicked".
Result: Overall correct
Semantic Similarity: 0.5121
Partial Similarity: 1.0000

Question: Who plays Elphaba in the 2024 movie Wicked?
Expected: Cynthia Erivo
Predicted: Cynthia Erivo plays Elphaba Thropp in the 2024 movie Wicked.
Result: Overall correct
Semantic Similarity: 0.5269
Partial Similarity: 1.0000
```

Finally, I repeated the process for a different movie, 'Moana 2,' and I was successfully able to seamlessly replicate my results for a different movie. 
