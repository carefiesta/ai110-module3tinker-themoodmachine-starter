"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # Added posts: slang, emoji, sarcasm, and mixed or subtle tone.
    "lowkey this movie was fire no cap 😂",
    "I absolutely love getting stuck in traffic",
    "kinda stressed about the exam but also proud I studied",
    "just got home",
    "not bad, the food was actually good",
    "im soooo tired rn :(",
    "ugh I hate how good this song is",
    "this party is sick 💀",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "lowkey this movie was fire no cap 😂" (slang praise)
    "negative",  # "I absolutely love getting stuck in traffic" (sarcasm)
    "mixed",     # "kinda stressed about the exam but also proud I studied"
    "neutral",   # "just got home"
    "positive",  # "not bad, the food was actually good"
    "negative",  # "im soooo tired rn :("
    "mixed",     # "ugh I hate how good this song is"
    "positive",  # "this party is sick 💀" (sick = great here; easy to read the other way)
]

# SAMPLE_POSTS and TRUE_LABELS stay the same length.
# A few of the new posts are easy to argue about:
#   - The traffic line looks positive if you only read "love".
#   - "this party is sick" can mean the party is great or that it is awful.
#   - "hate how good this song is" is annoyed and impressed at the same time.
#   - "not bad... actually good" is mild praise, not a strong happy post.
