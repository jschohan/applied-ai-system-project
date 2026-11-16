import math
from pathlib import Path

import pytest

from src.recommender import (WEIGHTS, category_sim, check_invariants, load_songs,
                             MOOD_GROUPS, GENRE_GROUPS, recommend_songs,
                             score_song, validate_profile, vocabulary)

CSV = str(Path(__file__).resolve().parent.parent / "data" / "songs.csv")


@pytest.fixture(scope="module")
def songs():
    return load_songs(CSV, quiet=True)


def song(**kw):
    base = dict(id=1, title="T", artist="A", genre="pop", mood="happy", energy=0.8,
                tempo_bpm=120.0, valence=0.9, danceability=0.8, acousticness=0.2)
    base.update(kw)
    return base


# ---- category_sim ---------------------------------------------------------
def test_category_sim_exact_group_none():
    assert category_sim("chill", "chill", MOOD_GROUPS) == 1.0
    assert category_sim("chill", "focused", MOOD_GROUPS) == 0.5
    assert category_sim("chill", "aggressive", MOOD_GROUPS) == 0.0
    assert category_sim("romantic", "chill", MOOD_GROUPS) == 0.0
    assert category_sim("pop", "indie pop", GENRE_GROUPS) == 0.5


# ---- score_song -----------------------------------------------------------
def test_perfect_match_scores_100():
    s = song()
    score, reasons = score_song({"genre": "pop", "mood": "happy", "energy": 0.8}, s)
    assert score == pytest.approx(100.0)
    assert reasons


def test_empty_prefs_scores_zero():
    score, reasons = score_song({}, song())
    assert score == 0.0 and reasons == ["no matching preferences provided"]


def test_score_normalized_by_present_features_only():
    # mood exact (30) + genre none (0) => 30/50 = 60
    score, _ = score_song({"mood": "happy", "genre": "metal"}, song())
    assert score == pytest.approx(100 * WEIGHTS["mood"] / (WEIGHTS["mood"] + WEIGHTS["genre"]))


def test_energy_is_gaussian():
    score, _ = score_song({"energy": 0.55}, song(energy=0.8))
    assert score == pytest.approx(100 * math.exp(-(0.25 ** 2) / (2 * 0.25 ** 2)))


def test_recommend_songs_sorted_and_k(songs):
    out = recommend_songs({"genre": "lofi", "mood": "chill", "energy": 0.3}, songs, k=5)
    assert len(out) == 5
    assert out[0][0]["genre"] == "lofi"
    assert check_invariants(out, 5) == []


# ---- load_songs -----------------------------------------------------------
def test_load_songs_types(songs):
    assert len(songs) == 20
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert vocabulary(songs)["genre"] and "romantic" in vocabulary(songs)["mood"]


# ---- validate_profile -----------------------------------------------------
def test_validate_lowercase_alias_clamp_drop(songs):
    clean, warns = validate_profile(
        {"favorite_genre": "Pop", "mood": "depressing", "energy": 1.5,
         "valence": "high", "bogus": 1}, songs)
    assert clean == {"genre": "pop", "energy": 1.0}
    assert len(warns) >= 4


def test_validate_handles_garbage(songs):
    assert validate_profile("nope", songs)[0] == {}
    clean, _ = validate_profile({"energy": float("nan"), "mood": None, "genre": 5}, songs)
    assert clean == {}
    # cleaned prefs must always be scoreable
    recommend_songs(clean, songs)


def test_validate_does_not_mutate_input(songs):
    prefs = {"Genre": "POP"}
    validate_profile(prefs, songs)
    assert prefs == {"Genre": "POP"}


# ---- check_invariants -----------------------------------------------------
def test_check_invariants_detects_problems():
    a, b = song(id=1), song(id=1)
    assert check_invariants([(a, 50.0, ""), (b, 60.0, "")], 2)  # unsorted + dup
    assert check_invariants([(a, 150.0, "")], 1)  # out of range
    assert check_invariants([(a, 10.0, "")], 3)  # wrong count
