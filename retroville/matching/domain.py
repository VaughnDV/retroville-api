"""Pure matching rules extracted from the 2019 `match_algorythim`.

Behaviour is characterised in tests/characterisation/test_matching_algorithm.py.
Random story selection is the original algorithm; pass `rng` to make it
deterministic in tests.
"""

from __future__ import annotations

import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    user_id: str
    liked_story_ids: frozenset[int]


def liked_story_ids(stories: Iterable[Mapping[str, object]]) -> list[int]:
    """Return story ids marked interested, preserving 2019 iteration order."""
    likes: list[int] = []
    for story in stories:
        story_id = story.get("id")
        if story.get("interested") and story_id is not None:
            likes.append(int(str(story_id)))
    return likes


def jaccard_coefficient(left: Iterable[int], right: Iterable[int]) -> float:
    left_set = set(left)
    right_set = set(right)
    union = left_set | right_set
    if not union:
        return 0.0
    return len(left_set & right_set) / len(union)


def select_match(
    user_likes: Sequence[int],
    candidates: Sequence[Candidate],
    rng: random.Random | None = None,
) -> tuple[int | None, str | None]:
    """Return `(matched_story_id, matched_user_id)`.

    2019 semantics:
    - first strictly greater Jaccard coefficient wins
    - coefficient 0 never matches
    - overlapping story is sampled uniformly from the intersection
    """
    sampler = rng.sample if rng is not None else random.sample
    coeff = 0.0
    matched_user: str | None = None
    matched_story: list[int] | None = None

    for candidate in candidates:
        intersection = list(set(candidate.liked_story_ids) & set(user_likes))
        coeff_new = jaccard_coefficient(candidate.liked_story_ids, user_likes)
        if coeff_new > coeff:
            matched_user = candidate.user_id
            matched_story = sampler(intersection, 1)
            coeff = coeff_new

    if not matched_story:
        return None, None
    return matched_story[0], matched_user
