"""Characterisation tests for the 2019 Jaccard matcher."""

import random

from retroville.matching.domain import Candidate, liked_story_ids, select_match


def test_liked_story_ids_preserve_order_and_skip_uninterested():
    stories = [
        {"id": 2, "interested": True},
        {"id": 3, "interested": False},
        {"id": 4, "interested": True},
    ]
    assert liked_story_ids(stories) == [2, 4]


def test_first_strictly_greater_coefficient_wins():
    user_likes = [1, 2, 3]
    candidates = [
        Candidate("alice", frozenset({1})),  # 1/3
        Candidate("bob", frozenset({1, 2})),  # 2/3
        Candidate("cara", frozenset({1, 2, 3, 4})),  # 3/4
    ]
    story_id, user_id = select_match(user_likes, candidates, rng=random.Random(0))
    assert user_id == "cara"
    assert story_id in {1, 2, 3}


def test_ties_keep_the_earlier_candidate():
    user_likes = [1, 2]
    candidates = [
        Candidate("alice", frozenset({1, 2})),
        Candidate("bob", frozenset({1, 2})),
    ]
    _, user_id = select_match(user_likes, candidates, rng=random.Random(0))
    assert user_id == "alice"


def test_zero_overlap_does_not_match():
    story_id, user_id = select_match(
        [1, 2],
        [Candidate("alice", frozenset({3, 4}))],
        rng=random.Random(0),
    )
    assert story_id is None
    assert user_id is None


def test_empty_candidates_returns_none():
    assert select_match([1], [], rng=random.Random(0)) == (None, None)


def test_story_sample_is_drawn_from_intersection():
    rng = random.Random(1)
    story_id, user_id = select_match(
        [10, 20, 30],
        [Candidate("alice", frozenset({20, 30, 40}))],
        rng=rng,
    )
    assert user_id == "alice"
    assert story_id in {20, 30}


def test_empty_likes_on_both_sides_do_not_crash():
    story_id, user_id = select_match([], [Candidate("alice", frozenset())], rng=random.Random(0))
    assert story_id is None
    assert user_id is None
