# 🎧 Model Card: Music Recommender Simulation

The Musice Recommender uses an algorithm to parse a csv file containing songs and features of the songs such as title, artist, genre, moode, energy, tempo_bpm, valence, danceability, and acousticness. This is parsed into a list of dictionaries and the algorithm processes each song to generate a score for it, comparing it to a given user's profile and preferences contained in the profile. Each song is given a score out of 100, weighing matches for genre and mood as heaviest. The recommender then can generate a list of songs based on the scores, a user can enter how many songs they would like recommended.

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness is that mood dominates the score for a song recommendation. So if a user wants to prioritize a genre or other feature but includes a mood in their profile, then they may not get the results expected or desired. The system also overfits to mood + high energy. Specifically with a positive mood and high energy. The data also does not have enough variety to cater to a combination of negative mood + high energy or positive mood + low energy. Another weakness of the system is that similarity groups are hard-coded so they may not always cover mood of the songs processed, even if a similar or related mood/genre should have been matched and given some sort of points.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.



---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
