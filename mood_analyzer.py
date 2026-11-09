# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Words that flip the next mood word. "not happy" should count as negative,
# and "not bad" should count as positive.
NEGATION_WORDS = {
    "not",
    "no",
    "never",
    "dont",
    "don't",
    "isnt",
    "isn't",
    "wasnt",
    "wasn't",
    "cant",
    "can't",
    "wont",
    "won't",
}

# Emoji signals added after breaker tests. Posts whose only cue was an emoji
# scored 0 and came back neutral. Skull and other ambiguous marks are left out.
POSITIVE_EMOJI = {":)", ":-)", ":d", ";)", "😂"}
NEGATIVE_EMOJI = {":(", ":-(", "😭"}

# Simple tokens: emoticons, words (keep apostrophes), then one leftover symbol
# such as an emoji. Punctuation below is dropped so "tired," still matches.
_TOKEN_RE = re.compile(r":-?\)|:-?\(|:d|;\)|[a-z0-9]+(?:'[a-z]+)?|[^\s\w]", re.IGNORECASE)
_SKIP_TOKENS = set(".,!?;:\"'()[]{}…-_/\\*#@")


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)
        self._positive_hits: List[str] = []
        self._negative_hits: List[str] = []

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Steps:
          - Strip leading and trailing whitespace
          - Lowercase the whole string
          - Split into words, simple emoticons, and single emoji characters
          - Drop commas and other punctuation stuck to a word
        """
        cleaned = text.strip().lower()
        tokens: List[str] = []
        for match in _TOKEN_RE.finditer(cleaned):
            token = match.group(0)
            if token in _SKIP_TOKENS:
                continue
            tokens.append(token)
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        Enhancement: a negation word flips the next mood word.
        "not happy" subtracts a point. "not bad" adds a point.
        A short list of emojis also adds or subtracts one point.
        Each match is counted every time it appears.
        """
        tokens = self.preprocess(text)
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            negated = token in NEGATION_WORDS or token.endswith("n't")
            if negated and i + 1 < len(tokens):
                nxt = tokens[i + 1]
                if nxt in self.positive_words:
                    score -= 1
                    negative_hits.append(f"not {nxt}")
                    i += 2
                    continue
                if nxt in self.negative_words:
                    score += 1
                    positive_hits.append(f"not {nxt}")
                    i += 2
                    continue

            if token in self.positive_words or token in POSITIVE_EMOJI:
                score += 1
                positive_hits.append(token)
            elif token in self.negative_words or token in NEGATIVE_EMOJI:
                score -= 1
                negative_hits.append(token)
            i += 1

        self._positive_hits = positive_hits
        self._negative_hits = negative_hits
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Mapping:
          - positive hits and negative hits together, and score between -1 and 1 -> "mixed"
          - score > 0 -> "positive"
          - score < 0 -> "negative"
          - score == 0 -> "neutral"

        A score of 2 or more stays positive even if one negative word showed up,
        and a score of -2 or less stays negative. The two sides have to nearly
        cancel before the label is mixed.
        """
        score = self.score_text(text)
        if self._positive_hits and self._negative_hits and abs(score) <= 1:
            return "mixed"
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        Uses the same hits as score_text, including negation flips.
        """
        score = self.score_text(text)
        return (
            f"Score = {score} "
            f"(positive: {self._positive_hits or '[]'}, "
            f"negative: {self._negative_hits or '[]'})"
        )
