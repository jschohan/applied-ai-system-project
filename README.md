# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommendations work by using data from users and metrics such as 
skips, saves, repeats etc to determine if a song is liked by a user. They also 
use audio signals or contextual signals such as titles or details within videos to detemine if they match with other videos/songs to group them into a category and decide if something should be recommended to a user that consumed something simliar. My version will prioritize the features of a song, such as valence, genre, energy, mood, and acousticness to determine if a user would like a song. This will be done by using an algorithm to calculate a score for a song given its features and weighing them depending on their importance, then comparing that score to see how close it is to the user's preference which will be stored in the UserProfile with the same attributes. The genre will be a string, mood will be a string, valence will be a float, energy will be a float, and acousticness for a user will be stored as a bool. Given a list of songs, it will sort them based on their scores and given to a user in the order from the most recommended to least recommended.

My plan is to score each song from 0 to 100, the score will be calculated by a sum of six components: Mood, Energy, Genre, Acousticness, Valence, and Danceability. They will be weighted in terms of importance of what would match a song to a user's taste profile more accurately. The weights will be 30, 25, 20, 10, 10, and 5 respectively. Each component will be calculated as the weight times similarity. A similarity will be from 0 to 1 and calculated such that if a mood or genre is an exact match (1), belonging to the same group(0.5), or other(0). This will be calculated as the similarity coefficient times the difference between the user preference and song feature value. A biased that I excpect from this recipe is that songs will be scored highered based on mood than genre. I think in reality, a user will often listen to songs from a similar genre with varying moods as opposed to varying moods from various genres. 

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



