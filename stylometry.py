"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import math
import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.

    MY CHOICE: coefficient of variation of words-per-sentence (stdev / mean).
    0.0 = every sentence the same length. Higher = lumpier = MORE HUMAN.
    Fewer than 2 sentences returns 0.0, and style_signal treats that case
    as "no evidence" (neutral) rather than as AI.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.

    MY CHOICE: moving-average TTR (MATTR). Take the TTR of every 50-word
    window and average them, so a long text isn't punished just for being
    long. Texts shorter than 50 words fall back to plain TTR.
    Higher = more varied vocabulary = MORE HUMAN.
    """
    w = words(text)
    if not w:
        return 0.0
    window = 50
    if len(w) <= window:
        return len(set(w)) / len(w)
    ratios = [len(set(w[i:i + window])) / window for i in range(len(w) - window + 1)]
    return sum(ratios) / len(ratios)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.

    MY CHOICE: "expressive" punctuation per word. Count everything EXCEPT
    full stops and commas, which every writer uses: ; : — – ( ) ! ? " … and
    a hyphen with spaces round it used as a dash.
    Higher = MORE HUMAN.
    """
    w = words(text)
    if not w:
        return 0.0
    marks = len(re.findall(r"[;:!?\"“”()…—–]", text))
    marks += len(re.findall(r"\s-\s", text))   # " - " typed as a dash
    return marks / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    MY RULE (numbers from the calibration run in the README):
      - spread -> AI score with a logistic: spread 0.6 scores 0.5, lower
        spread (sentences marching in step) scores higher. Weight 0.6.
      - punctuation -> AI score between 0.25 and 0.75 only: having no dashes
        or semicolons is weak evidence (lots of people never use them), so it
        can't push the score to the extremes on its own. Weight 0.4.
      - type-token ratio gets weight 0. On my calibration texts it pointed
        the WRONG way (AI text had the most varied vocabulary, the plain
        human writer the least), so counting it would accuse plain writers.
        It's still computed and printed so I can watch it.
      - one sentence: no spread evidence -> the spread part counts as 0.5.

    UNIT 8 MILESTONE 5 CHANGE (the one fix — see README "The Improvement"):
      - type-token ratio now COUNTS, pointing the way my data shows: HIGH
        vocabulary variety = more AI. Logistic, midpoint 0.86 (halfway between
        the AI calibration samples, 0.915/0.935, and the human ones,
        0.773/0.808), steepness 20. Under 50 words it's neutral (0.5), because
        TTR on a short text is near 1.0 for everyone. Weight 0.4.
      - punctuation weight 0.4 -> 0.2 (diagnosis 1: "no dashes or semicolons"
        is weak evidence; all six false positives had none).
      - spread weight 0.6 -> 0.4.
    """
    n_sentences = len(sentences(text))
    if n_sentences < 2:
        spread_ai = 0.5
    else:
        spread = sentence_length_spread(text)
        spread_ai = 1.0 / (1.0 + (spread / SPREAD_MIDPOINT) ** 3)

    punct = punctuation_density(text)
    punct_ai = 0.25 + 0.5 / (1.0 + (punct / PUNCT_MIDPOINT) ** 2)

    if len(words(text)) < TTR_MIN_WORDS:
        ttr_ai = 0.5
    else:
        ttr_ai = 1.0 / (1.0 + math.exp(-TTR_STEEPNESS * (type_token_ratio(text) - TTR_MIDPOINT)))

    score = WEIGHT_SPREAD * spread_ai + WEIGHT_PUNCT * punct_ai + WEIGHT_TTR * ttr_ai
    return round(min(max(score, 0.0), 1.0), 4)


# Tuned on the calibration inputs — see README "Signals and Scoring".
SPREAD_MIDPOINT = 0.6    # sentence-length CV that scores 0.5
PUNCT_MIDPOINT = 0.02    # expressive marks per word that scores 0.5
TTR_MIDPOINT = 0.86      # vocabulary variety that scores 0.5 (Unit 8 M5)
TTR_STEEPNESS = 20.0
TTR_MIN_WORDS = 50       # below this, TTR says nothing -> neutral
# Before Unit 8 M5: spread 0.6, punct 0.4, ttr 0.0
WEIGHT_SPREAD = 0.4
WEIGHT_PUNCT = 0.2
WEIGHT_TTR = 0.4         # high variety = AI, the way my calibration data ran


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
