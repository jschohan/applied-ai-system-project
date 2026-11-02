import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

WEIGHTS = {
    "mood": 30,
    "energy": 25,
    "genre": 20,
    "acousticness": 10,
    "valence": 10,
    "danceability": 5,
}

ENERGY_SIGMA = 0.25

MOOD_GROUPS = [
    {"chill", "relaxed", "peaceful", "focused"},
    {"happy", "uplifting", "euphoric", "energetic"},
    {"intense", "aggressive", "confident"},
    {"moody", "melancholic", "sad", "nostalgic"},
]

GENRE_GROUPS = [
    {"pop", "indie pop"},
    {"rock", "metal"},
    {"lofi", "jazz", "ambient", "classical"},
    {"edm", "synthwave"},
    {"folk", "country", "blues"},
    {"hip hop", "r&b"},
    {"latin", "reggae"},
]


def category_sim(a: str, b: str, groups: List[set]) -> float:
    """1.0 for an exact match, 0.5 if both labels share a group, else 0.0."""
    if a == b:
        return 1.0
    if any(a in group and b in group for group in groups):
        return 0.5
    return 0.0


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns (score out of 100, reasons). Features missing from user_prefs are
    skipped and the remaining weights are rescaled to sum to 100.
    """
    points: Dict[str, float] = {}
    reasons: List[str] = []

    for feature, groups in (("mood", MOOD_GROUPS), ("genre", GENRE_GROUPS)):
        if feature not in user_prefs:
            continue
        sim = category_sim(user_prefs[feature], song[feature], groups)
        points[feature] = WEIGHTS[feature] * sim
        if sim == 1.0:
            reasons.append(f"{feature} matches ({song[feature]})")
        elif sim > 0:
            reasons.append(
                f"{feature} is similar ({song[feature]} ~ {user_prefs[feature]})"
            )

    for feature in ("energy", "acousticness", "valence", "danceability"):
        if feature not in user_prefs:
            continue
        diff = abs(user_prefs[feature] - song[feature])
        if feature == "energy":
            sim = math.exp(-(diff ** 2) / (2 * ENERGY_SIGMA ** 2))
        else:
            sim = max(0.0, 1.0 - diff)
        points[feature] = WEIGHTS[feature] * sim
        if sim >= 0.9:
            reasons.append(
                f"{feature} is close ({song[feature]:.2f} vs {user_prefs[feature]:.2f})"
            )

    total_weight = sum(WEIGHTS[f] for f in points)
    if total_weight == 0:
        return 0.0, ["no matching preferences provided"]

    score = sum(points.values()) * 100 / total_weight
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, ", ".join(reasons) or "weak match on all features")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
