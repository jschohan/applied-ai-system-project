"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Usage (from the project root):
    python src/main.py                  # standard profiles
    python src/main.py --adversarial    # edge-case / adversarial profiles
    python src/main.py --all            # both sets
    python src/main.py --query "mellow for studying" [--verbose]   # agentic (Gemini)
    python src/main.py --eval           # reliability harness for the agent
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.agent import run_agent
from src.evaluate import print_eval, run_eval
from src.llm_client import GeminiClient
from src.recommender import load_songs, recommend_songs, validate_profile

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


def print_agent_result(res, width: int = 56) -> None:
    print()
    print(f'[agent] "{res.query}"')
    print(f"Profile used: {res.prefs or '(empty)'}")
    for w in res.warnings:
        print(f"  WARNING: {w}")
    print("=" * width)
    for rank, (song, score, why) in enumerate(res.results, start=1):
        print(f"{f'{rank}. {song['title']}':<{width - 12}}{score:>6.1f} / 100")
        print(f"     - {why}")
    print("-" * width)
    print(f"Why: {res.explanation}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Music recommender simulation")
    ap.add_argument("--adversarial", action="store_true", help="edge-case profiles")
    ap.add_argument("--all", action="store_true", help="standard + adversarial profiles")
    ap.add_argument("--query", help="free-text request handled by the Gemini agent")
    ap.add_argument("--eval", action="store_true", help="run the agent reliability harness")
    ap.add_argument("--verbose", action="store_true", help="print the agent trace")
    args = ap.parse_args()

    songs = load_songs(str(ROOT / "data" / "songs.csv"), quiet=args.query is not None or args.eval)

    if args.eval:
        print_eval(run_eval(songs, GeminiClient()))
        return
    if args.query is not None:
        res = run_agent(args.query, songs, GeminiClient(), verbose=args.verbose)
        print_agent_result(res)
        return

    profiles = {}
    if not args.adversarial or args.all:
        profiles.update(STANDARD_PROFILES)
    if args.adversarial or args.all:
        profiles.update(ADVERSARIAL_PROFILES)

    for name, user_prefs in profiles.items():
        clean, warnings = validate_profile(user_prefs, songs)
        for w in warnings:
            print(f"  (validation) [{name}] {w}")
        print_recommendations(name, clean, songs)


if __name__ == "__main__":
    main()
