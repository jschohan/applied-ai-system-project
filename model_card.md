# 🎧 Model Card: Music Recommender Simulation

The Musice Recommender uses an algorithm to parse a csv file containing songs and features of the songs such as title, artist, genre, moode, energy, tempo_bpm, valence, danceability, and acousticness. This is parsed into a list of dictionaries and the algorithm processes each song to generate a score for it, comparing it to a given user's profile and preferences contained in the profile. Each song is given a score out of 100, weighing matches for genre and mood as heaviest. The recommender then can generate a list of songs based on the scores, a user can enter how many songs they would like recommended.

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MusicMatcher

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender calculates a score for songs based on a user's preferences on a set of values to 'describe' the song. It assumes that a user knows what they like to hear. This was built for classroom exploration.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

A song is described using features: artist, genre, mood, energy, acousticness, valence, and danceability. The recommender assigns weights to each feature then calculates a score but summing the match of each feature with a user's preferences of those features. A user can omit a feature and the recommender will adjust according to the features provided to create a score. The model then returns top number of songs requested by the user that scored the highest.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The model uses a dataset of 20 songs. It contains genres pop, hip-hop, lofi, rock, metal, indie, classical, country and more. I added data to include different combinations of featuers. There are some parts such as genres and combinations of moods/energy or moods/genres missing from the dataset.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system seems to work well when matching a user's mood or genre to exact matches in the dataset. It also does well if the features are included in the related group to ensure the songs get a partial score boost for being similar to the feature the user is looking for. 

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

I tested user profiles with genre/mood pairs: pop/happy, lofi/chill, metal/energetic, country/depressing. I expected the recommendations to first cover the mood matches since they were weighted the highest followed by genre matches. The pop/happy profile prefers happy songs from the pop genre and high energy. Lofi/chill profile prefers chill or similar (relaxed or ambient) matches for genre. Metal/energetic prefers high energy songs with mood match prioritizing genre + energy match. Country/depressing prioritized genre match and similar genres since the 'depressing' mood did not match those in the groups or data set.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would improve the next model by expanding the related group and allowing users to detemine their own priority of featues. So that a user can get results better refined for what they truly want. For example, if a user wants a country song with a happy mood but low energy. 

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned what types of values recommender systems look and a way to potentially score items to find the best match to a user's preferences. Something interesting I discovered is that it could be difficult to completely eliminate bias toward features. Having an unbiased recommender would mean inaccurate recommendations while a biased gives priority to some aspect of the data, making it more likely to appear or score higher. AI tools helped me create the algorithm and write a recipe for scoring and weighting. My biggest learning moment was seeing how to cover the related but not exact word matches for features, by creating a mapping and groups of synonomous terms. I needed to double-check the complicated arthimetic by running the data manually to see if the results would be as expected. What surprised me about a simple algorithm feeling like recommendations is that it doesn't require as much backend or complex code to figure out if a song fits a user's preferences. For example, a simple points assigning system (+-) for feature matches would give a fairly accurate score. If I were to extend this project I would try to parse a larger dataset to see how the recommender handles it.

---

## 10. AI Feature: Agentic Gemini Workflow

**What it does.** `python src/main.py --query "..."` runs plan -> act -> check -> explain. Gemini (default `gemini-3.5-flash-lite`, free tier, override with `GEMINI_MODEL`) turns free text into a preference profile with genre/mood restricted to the catalog vocabulary. The deterministic scorer (`recommend_songs`) produces the ranking. A Gemini critic reviews the top 5 against the request and may adjust the profile (max 3 iterations, best-rated iteration kept). Gemini then writes a short rationale. The LLM never ranks songs itself.

**Guardrails.** Every profile (LLM-made or hand-written) goes through `validate_profile` (lowercase, alias keys, clamp to [0,1], drop unknown labels and non-numeric values). Final results pass invariant checks (scores 0-100, descending, k items, no duplicates). Any API error, rate limit, timeout or bad JSON falls back to a keyword-based profile and the same scorer, with a visible warning. User text is passed inside `<request>` delimiters as data, and the output is schema-constrained.

**Privacy.** Only the free-text music request and song metadata (title, genre, mood, audio features) are sent. Free-tier prompts may be used by Google, so nothing personal should be typed. The key comes from `GEMINI_API_KEY` or a git-ignored `.env`.

**Measured reliability** (`python src/main.py --eval`, 9 queries, one run, so noisy): JSON parse success 89%, valid profile after validation 78%, critic changed the result 11%, top-1 matched expected genre/mood 4 of 4 (100%) on queries with expectations, fallback 11%, invariants 100%. The two non-valid runs were the empty query (no preferences, which is correct) and the prompt-injection query, where the model returned no usable JSON and the app fell back.

**Limitations / biases.**
- The critic can only re-weight the profile, not change the catalog. For "chill lofi, not too acoustic" every lofi/chill song in the 20-song catalog has acousticness 0.71-0.92, so the critic rated 2/5 three times and the loop kept iteration 1. The explanation did not warn the user about the mismatch.
- LLM output varies run to run; the eval is a small sample, and expected-genre matching uses hand-picked acceptable sets.
- Query text is truncated to 500 characters. The planner can only express the six scored features.
- Free-tier quotas are low; the eval pauses between queries.

