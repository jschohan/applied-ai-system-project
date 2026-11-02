"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 56
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print()
    print(f"Top {len(recommendations)} recommendations for: {profile}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        label = f"{rank}. {song['title']}"
        print(f"{label:<{width - 12}}{score:>6.1f} / 100")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
        print("-" * width)


if __name__ == "__main__":
    main()
