"""GAIA-style answer scoring helpers.

This mirrors the normalization behavior used by the GAIA reference scorer:
- numeric answers are compared after removing $, %, and commas
- comma/semicolon lists are split and compared element by element
- plain strings are lowercased and compared after removing whitespace/punctuation
"""

from __future__ import annotations

import re
import string
from logging import getLogger
from typing import Any


logger = getLogger(__name__)


def normalize_number_str(number_str: str) -> float:
    for char in ["$", "%", ","]:
        number_str = number_str.replace(char, "")
    try:
        return float(number_str)
    except ValueError:
        logger.warning("String %s cannot be normalized to number str.", number_str)
        return float("inf")


def split_string(s: str, char_list: list[str] | None = None) -> list[str]:
    char_list = char_list or [",", ";"]
    pattern = f"[{''.join(char_list)}]"
    return re.split(pattern, s)


def question_scorer(model_answer: str, ground_truth: str) -> tuple[bool, str]:
    model_answer = "" if model_answer is None else str(model_answer)
    ground_truth = "" if ground_truth is None else str(ground_truth)

    def is_float(element: Any) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    if is_float(ground_truth):
        normalized_answer = normalize_number_str(model_answer)
        return (
            normalized_answer == float(ground_truth),
            f"Evaluated {model_answer} as a number.",
        )

    if any(char in ground_truth for char in [",", ";"]):
        gt_elems = split_string(ground_truth)
        ma_elems = split_string(model_answer)

        if len(gt_elems) != len(ma_elems):
            return (
                False,
                "Evaluated answer as a comma separated list, returned False "
                "because lists have different lengths.",
            )

        comparisons = []
        for ma_elem, gt_elem in zip(ma_elems, gt_elems):
            if is_float(gt_elem):
                normalized_ma_elem = normalize_number_str(ma_elem)
                comparisons.append(normalized_ma_elem == float(gt_elem))
            else:
                comparisons.append(
                    normalize_str(ma_elem, remove_punct=False)
                    == normalize_str(gt_elem, remove_punct=False)
                )
        return all(comparisons), f"Evaluated {model_answer} as a comma separated list."

    return (
        normalize_str(model_answer) == normalize_str(ground_truth),
        f"Evaluated {model_answer} as a string.",
    )


def normalize_str(input_str: str, remove_punct: bool = True) -> str:
    no_spaces = re.sub(r"\s", "", input_str)
    if remove_punct:
        translator = str.maketrans("", "", string.punctuation)
        return no_spaces.lower().translate(translator)
    return no_spaces.lower()
