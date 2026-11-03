"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Usage (from the project root):
    python src/main.py                  # standard profiles
    python src/main.py --adversarial    # edge-case / adversarial profiles
    python src/main.py --all            # both sets
"""

import sys

from recommender import load_songs, recommend_songs

STANDARD_PROFILES = {
    "pop / happy": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "lofi / chill": {"genre": "lofi", "mood": "chill", "energy": 0.3},
    "metal / energetic": {"genre": "metal", "mood": "energetic", "energy": 1},
    "country / depressing": {"genre": "country", "mood": "depressing", "energy": 0},
}

ADVERSARIAL_PROFILES = {
    "1 conflict: sad + high energy": {"mood": "sad", "energy": 0.9},
    "2 conflict: metal + peaceful + acoustic": {
        "genre": "metal", "mood": "peaceful", "energy": 0.95, "acousticness": 0.95,
    },
    "3 unknown labels (angry / k-pop)": {"mood": "angry", "genre": "k-pop", "energy": 0.8},
    "4 empty prefs": {},
    "5 wrong case (Pop / Happy)": {"genre": "Pop", "mood": "Happy", "energy": 0.8},
    "6 typo key (favorite_genre)": {"favorite_genre": "pop", "energy": 0.8},
    "7 out-of-range energy (1.5)": {"energy": 1.5},
    "8 single feature (mood=chill)": {"mood": "chill"},
    "9 ungrouped mood (romantic)": {"mood": "romantic", "genre": "r&b", "energy": 0.48},
    "10 energy 0 + valence 0": {"energy": 0.0, "valence": 0.0},
    "11 everything at 0.5": {
        "energy": 0.5, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 56
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items()) or "(empty)"
    print()
    print(f"[{name}]")
    print(f"Top {len(recommendations)} recommendations for: {profile}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        label = f"{rank}. {song['title']}"
        print(f"{label:<{width - 12}}{score:>6.1f} / 100")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
        print("-" * width)


def main() -> None:
    args = set(sys.argv[1:])
    songs = load_songs("data/songs.csv")

    profiles = {}
    if "--adversarial" not in args or "--all" in args:
        profiles.update(STANDARD_PROFILES)
    if "--adversarial" in args or "--all" in args:
        profiles.update(ADVERSARIAL_PROFILES)

    for name, user_prefs in profiles.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
