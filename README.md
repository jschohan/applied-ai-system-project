# Original Project
This project is an enhancement of Project 3: Music Recommender Simulation from module 3. The original goal of this project was to simulate a basic music recommending system with Python that can rank and list songs based on a user profile of preferences. The project was capable of matching user profile attributes to a small dataset of songs, also broken into attributes such as mood, energy, genre etc and generating a score based on alikeness then returning a list of a specified number of those songs ranked in decreasing order.

# Title and Summary
MusicMatcher 2.0 builds on top of the original project. It now features the ability to add a query in plain text that the system then turns into a user profile using Gemini and generates a ranked list of songs for that user. The project also provides feedback to a user if any passed attributes were not verifiable or matched to those in the dataset of songs and similar attributes, so a user will know if a preference was not accounted for. This produces more accurate and explainable results. It also allows users to generate a list without having to add a user profile as a dictionary manually.


# Architecture Overview
The system diagram can be rendered in mermaid.live to show an the project architecture. It shows the types of inputs that can be given to the system and the path they take into the agent loop. Text-queries are pipelined to the planner and validation from the Gemini API llm agent. If it is unavailable then the system falls back onto the rule-based keyword paradigm. Next, the generated results are verified against the input query, again using the Gemini API. The scoring algorithm is fixed and consistent for all pathways. The fixed user profiles are also validated and can be adjusted in the agentic loop. The output contains the top k rated songs, explanations, and warnings if applicable. There is an evaluater in place to act as a reliability harness.

# Setup Instructions
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and paste your Gemini free-tier key
   (https://aistudio.google.com/apikey). Without a key the app still runs,
   using the rule-based fallback.

# Usage
python src/main.py                       # 4 standard profiles
python src/main.py --adversarial         # 11 edge-case profiles
python src/main.py --all                 # both
python src/main.py --query "chill lofi for studying" --verbose   # Gemini agent + trace
python src/main.py --eval                # reliability harness (9 queries)
pytest                                   # 25 tests, offline

# Sample Interactions
## Input: 
python src/main.py --query "chill lofi for studying" --verbose

## Output: 
[plan] query='chill lofi for studying'
  raw={'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'acousticness': 0.6, 'valence': 0.5, 'danceability': 0.4}
  validated={'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'acousticness': 0.6, 'valence': 0.5, 'danceability': 0.4}
[recommend #1] prefs={'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'acousticness': 0.6, 'valence': 0.5, 'danceability': 0.4}
1. Library Rain (lofi, chill, energy 0.35, acoustic 0.86, valence 0.60) score 95.0: mood matches (chill), genre matches (lofi), energy is close (0.35 vs 0.30), valence isclose (0.60 vs 0.50)
2. Midnight Coding (lofi, chill, energy 0.42, acoustic 0.71, valence 0.56) score 94.5: mood matches (chill), genre matches (lofi), valence is close (0.56 vs 0.50)
3. Spacewalk Thoughts (ambient, chill, energy 0.28, acoustic 0.92, valence 0.65) score 85.2: mood matches (chill), genre is similar (ambient ~ lofi), energy is close (0.28 vs 0.30), danceability is close (0.41 vs 0.40)
4. Focus Flow (lofi, focused, energy 0.40, acoustic 0.78, valence 0.59) score 79.4: mood is similar (focused ~ chill), genre matches (lofi), energy is close (0.40 vs 0.30), valence is close (0.59 vs 0.50)
5. Coffee Shop Stories (jazz, relaxed, energy 0.37, acoustic 0.89, valence 0.71) score 68.3: mood is similar (relaxed ~ chill), genre is similar (jazz ~ lofi), energy is close (0.37 vs 0.30)
[critique #1] {'verdict': 'ok', 'rating': 5, 'reason': "The top results closely match the user's request for chill lofi music suitable for studying, with strong genre andmood alignment."}
[select] kept iteration 1 of 1
[explain] These songs fit your request because they match your desired chill mood and lofi genre, or feature very similar moods like relaxed and focused alongside similargenres like ambient and jazz. Additionally, their energy and valence levels are closely aligned with what you are looking for.

[agent] "chill lofi for studying"
Profile used: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'acousticness': 0.6, 'valence': 0.5, 'danceability': 0.4}
========================================================
1. Library Rain                               95.0 / 100
     - mood matches (chill), genre matches (lofi), energy is close (0.35 vs 0.30), valence is close (0.60 vs 0.50)
2. Midnight Coding                            94.5 / 100
     - mood matches (chill), genre matches (lofi), valence is close (0.56 vs 0.50)
3. Spacewalk Thoughts                         85.2 / 100
     - mood matches (chill), genre is similar (ambient ~ lofi), energy is close (0.28 vs 0.30), danceability is close (0.41 vs 0.40)
4. Focus Flow                                 79.4 / 100
     - mood is similar (focused ~ chill), genre matches (lofi), energy is close (0.40 vs 0.30), valence is close (0.59 vs 0.50)
5. Coffee Shop Stories                        68.3 / 100
     - mood is similar (relaxed ~ chill), genre is similar (jazz ~ lofi), energy is close (0.37 vs 0.30)
--------------------------------------------------------
Why: These songs fit your request because they match your desired chill mood and lofi genre, or feature very similar moods like relaxed and focused alongside similar genres like ambient and jazz. Additionally, their energy and valence levels are closely aligned with what you are looking for.

## Input: 
python src/main.py --query "Funky music that I can jam out to" --verbose

## Output: 
1. Calle Sol (latin, energetic, energy 0.84, acoustic 0.20, valence 0.88) score 74.5: mood matches (energetic), energy is close (0.84 vs 0.80), danceability is close (0.92 vs 0.90)
2. Sunrise City (pop, happy, energy 0.82, acoustic 0.18, valence 0.84) score 55.5: mood is similar (happy ~ energetic), energy is close (0.82 vs 0.80)
3. Rooftop Lights (indie pop, happy, energy 0.76, acoustic 0.35, valence 0.81) score 55.4: mood is similar (happy ~ energetic), energy is close (0.76 vs 0.80), danceability is close (0.82 vs 0.90)
4. Neon Pulse Festival (edm, euphoric, energy 0.95, acoustic 0.03, valence 0.82) score 51.1: mood is similar (euphoric ~ energetic), danceability is close (0.90 vs 0.90)
5. Concrete Poetry (hip hop, confident, energy 0.72, acoustic 0.12, valence 0.58) score 48.1: genre is similar (hip hop ~ r&b), energy is close (0.72 vs 0.80), danceability is close (0.85 vs 0.90)
[critique #1] {'verdict': 'adjust', 'rating': 2, 'reason': 'The results provided latin, pop, indie pop, edm, and hip hop, but the user specifically asked for funky music to jam out to. While the energy and danceability are high, the genre needs to reflect a funkier or soul-infused style.', 'adjustments': {'genre': 'pop', 'mood': 'energetic', 'energy': 0.85, 'danceability': 0.95}}
[recommend #2] prefs={'genre': 'pop', 'mood': 'energetic', 'energy': 0.85, 'danceability': 0.95}
1. Sunrise City (pop, happy, energy 0.82, acoustic 0.18, valence 0.84) score 80.0: mood is similar (happy ~ energetic), genre matches (pop), energy is close (0.82 vs 0.85)
2. Calle Sol (latin, energetic, energy 0.84, acoustic 0.20, valence 0.88) score 74.8: mood matches (energetic), energy is close (0.84 vs 0.85), danceability is close (0.92 vs 0.95)
3. Rooftop Lights (indie pop, happy, energy 0.76, acoustic 0.35, valence 0.81) score 66.0: mood is similar (happy ~ energetic), genre is similar (indie pop ~ pop), energyis close (0.76 vs 0.85)
4. Gym Hero (pop, intense, energy 0.93, acoustic 0.05, valence 0.77) score 60.5: genre matches (pop), energy is close (0.93 vs 0.85), danceability is close (0.88 vs 0.95)
5. Neon Pulse Festival (edm, euphoric, energy 0.95, acoustic 0.03, valence 0.82) score 53.5: mood is similar (euphoric ~ energetic), energy is close (0.95 vs 0.85), danceability is close (0.90 vs 0.95)
[critique #2] {'verdict': 'adjust', 'rating': 2, 'reason': 'The user requested funky music to jam out to, but the current results focus heavily on standard pop, latin, and edm rather than funk or r&b with high danceability and groove.', 'adjustments': {'genre': 'r&b', 'mood': 'energetic', 'danceability': 0.98}}
[recommend #3] prefs={'genre': 'r&b', 'mood': 'energetic', 'energy': 0.85, 'danceability': 0.98}
1. Calle Sol (latin, energetic, energy 0.84, acoustic 0.20, valence 0.88) score 74.6: mood matches (energetic), energy is close (0.84 vs 0.85), danceability is close (0.92 vs 0.98)
2. Sunrise City (pop, happy, energy 0.82, acoustic 0.18, valence 0.84) score 54.8: mood is similar (happy ~ energetic), energy is close (0.82 vs 0.85)
3. Neon Pulse Festival (edm, euphoric, energy 0.95, acoustic 0.03, valence 0.82) score 53.3: mood is similar (euphoric ~ energetic), energy is close (0.95 vs 0.85), danceability is close (0.90 vs 0.98)
4. Rooftop Lights (indie pop, happy, energy 0.76, acoustic 0.35, valence 0.81) score 53.3: mood is similar (happy ~ energetic), energy is close (0.76 vs 0.85)
5. Concrete Poetry (hip hop, confident, energy 0.72, acoustic 0.12, valence 0.58) score 45.2: genre is similar (hip hop ~ r&b)
[critique #3] {'verdict': 'adjust', 'rating': 2, 'reason': 'The request is for funky music to jam out to, but the current results are heavy on latin, pop, edm, and indie pop without any explicit funk genre focus.', 'adjustments': {'genre': 'pop', 'mood': 'energetic', 'energy': 0.9, 'danceability': 0.95}}
[select] kept iteration 1 of 3
[explain] These songs fit your request because they match your desired energetic mood and feature close energy levels for you to jam out to. Additionally, they have high danceability and valence scores that align with your musical preferences.

[agent] "Funky music that I can jam out to"
Profile used: {'genre': 'r&b', 'mood': 'energetic', 'energy': 0.8, 'danceability': 0.9}
========================================================
1. Calle Sol                                  74.5 / 100
     - mood matches (energetic), energy is close (0.84 vs 0.80), danceability is close (0.92 vs 0.90)
2. Sunrise City                               55.5 / 100
     - mood is similar (happy ~ energetic), energy is close (0.82 vs 0.80)
3. Rooftop Lights                             55.4 / 100
     - mood is similar (happy ~ energetic), energy is close (0.76 vs 0.80), danceability is close (0.82 vs 0.90)
4. Neon Pulse Festival                        51.1 / 100
     - mood is similar (euphoric ~ energetic), danceability is close (0.90 vs 0.90)
5. Concrete Poetry                            48.1 / 100
     - genre is similar (hip hop ~ r&b), energy is close (0.72 vs 0.80), danceability is close (0.85 vs 0.90)
--------------------------------------------------------
Why: These songs fit your request because they match your desired energetic mood and feature close energy levels for you to jam out to. Additionally, they have high danceability and valence scores that align with your musical preferences.

# Design Decisions
One design decision I made was to exclude RAG since that would increase response time generation significantly. I also chose to keep the data set fixed and small for the songs to allow the AI to verify results faster. This means that there can still be responses or inputs that can fail to give a user desired results.

# Testing Summary
Based on the tests it seems like the Agent Loop is working well and system will iterate to see if a higher result score can be generated.

# Reflection 
I learned that using a general AI model to solve a problem could come at a cost of time. A trained model to perform a specific task would be much more desirable. Also, when building the system there needs to be fixed guardrails for when the agent fails, which could be for a multitude of reasons.