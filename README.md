# Original Project
This project is an enhancement of Project 3: Music Recommender Simulation from module 3. The original goal of this project was to simulate a basic music recommending system with Python that can rank and list songs based on a user profile of preferences. The project was capable of matching user profile attributes to a small dataset of songs, also broken into attributes such as mood, energy, genre etc and generating a score based on alikeness then returning a list of a specified number of those songs ranked in decreasing order.

# Title and Summary
MusicMatcher 2.0 builds on top of the original project. It now features the ability to add a query in plain text that the system then turns into a user profile using Gemini and generates a ranked list of songs for that user. The project also provides feedback to a user if any passed attributes were not verifiable or matched to those in the dataset of songs and similar attributes, so a user will know if a preference was not accounted for. This produces more accurate and explainable results. It also allows users to generate a list without having to add a user profile as a dictionary manually.


