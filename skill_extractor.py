import re
from collections import Counter

STOP_WORDS = {
    "the","and","for","with","from","that","this","your","their",
    "have","will","into","using","used","are","our","you","they",
    "must","should","ability","knowledge","required","experience",
    "candidate","company","role","work","years","skills","job",
    "responsibilities","including","understanding","basic","good",
    "strong","ability","support","analysis","business"
}


def extract_keywords(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9+# ]", " ", text)

    words = text.split()

    words = [
        w for w in words
        if len(w) > 2 and w not in STOP_WORDS
    ]

    counter = Counter(words)

    keywords = []

    for word, count in counter.items():

        if count >= 2:
            keywords.append(word)

    return sorted(keywords)