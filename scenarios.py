"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

import json as _json
from pathlib import Path as _Path


def _sample(name):
    """The text of one file in samples/, so criterion 3 tests exactly those."""
    return _json.loads((_Path(__file__).parent / "samples" / f"{name}.json").read_text())["text"]


SCENARIOS = [
    {
        # Criterion 1: of 10 pieces I wrote myself, at most 1 labelled AI,
        # in every trial.
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        # Each piece needs a few sentences at least (gpt2 refuses under 3
        # tokens) and under 20,000 characters.
        "texts": [
            # Paragraphs from my own earlier CodePath READMEs (markdown stripped).
            # TakeMeter README, 'What I predicted before I looked'
            "I expect the baseline to score about 0.50 accuracy and 0.40 macro F1, well below my trained model (0.70 / 0.656). It has never seen LetsRun posts and only gets one sentence per label. I expect it to do best on reaction, because first-person feelings and race reports are easy to spot, and maybe beat my model’s 0.43 recall there. I expect it to struggle most on analysis vs hot_take, because the difference is whether a fact actually carries the argument, and a definition alone can’t teach that. If the gap turns out smaller than 0.05 accuracy (under 2 posts out of 30), I’ll treat the two models as tied.",
            # TakeMeter README, 'What the gap actually means'
            "I expected 'hot_take' to be its best label but it showed 0. The trained model beat the baseline by 0.545 macro F1 (21 vs 6 correct out of 30), far more than the 1–2 posts chance could explain, so fine-tuning on my 140 labelled posts clearly taught the model something my definitions alone could not. But the baseline labelled every single post analysis, likely because my analysis definition (“makes an argument…”) fits almost any opinion post, so this gap partly reflects a weak opponent rather than a strong model. The fairer comparison is the “always guess hot_take” strategy (0.57 accuracy), which my model beats by only about 4 posts: useful, but still modest.",
            # Unofficial Guide README, CHUNK_SIZE diagnosis
            "CHUNK_SIZE is 800 characters but my criterion is in tokens. Every advice_threads file is under 800 characters (shortest 320, longest 796), so fallback_split never cuts anything: each thread becomes exactly one chunk of roughly 90–225 tokens. The five threads my questions hit are all under 200. The size half of the criterion can't be met by tuning CHUNK_SIZE, because a bigger window has nothing more to take from the same file. The only way to get over 200 tokens would be to merge different threads into one chunk, which breaks the other half of the same criterion (\"without excessive unrelated information\").",
            # Unofficial Guide README, unrelated-text diagnosis
            "The unrelated-text half is also a chunking problem. One thread is several replies, and each of my questions is answered by one reply (pass/fail → reply 2, internship → reply 1, meal plan → reply 1, laundry → reply 1). Whole-thread chunks always carry the other replies along. That shows up in retrieval too: the pass/fail question's best distance is 0.474, the weakest of the five, because the \"week eight\" sentence is diluted by three replies about other things.",
            # Unofficial Guide README, what improved
            "What did improve is retrieval. The best distance dropped for all five questions, and the biggest gain was the one my diagnosis pointed at: pass/fail went from 0.474 to 0.217 once the \"week eight\" reply stopped sharing a chunk with three unrelated replies. The gate got safer too. Before, the gap between my worst in-scope question (0.474) and my closest out-of-scope question (0.787) was 0.31. Now it is 0.29 to 0.81, a gap of 0.51, so 0.6 sits much more comfortably in the middle. Fewer unrelated threads come back as well (2–3 source files per question instead of 4–5).",
            # Unofficial Guide README, laundry answer change
            "One answer-quality change I didn't expect: before, the laundry answer said laundry is \"free\", which could be read as no cost. After, all three runs say \"least busy\" or \"free (least busy)\". With only the one reply and the title in front of it, the model read \"free\" the way the thread meant it.",
            # Unofficial Guide README, rewriting criterion 4
            "I'd rewrite criterion 4. I wrote \"200–800 tokens\" before measuring my documents, and it mixed up units: the config counts characters and the criterion counts tokens. The longest thread in the corpus is about 225 tokens, so the floor was close to impossible from the start. A better version, based on what I actually saw: \"For at least 4 of 5 questions, the chunk containing the answer holds no more than one reply that is unrelated to the question, and no reply is cut mid-sentence.\" That is countable and fits a corpus of short threads.",
            # FitFindr README, what it does
            "FitFindr helps someone shop secondhand. You type what you're looking for in plain language — like 'vintage graphic tee under $30, size M' — and it searches 40 thrift listings from Depop, thredUp and Poshmark for the best match within your size and budget. It then suggests one or two outfits that pair the find with clothes you already own, and writes a short caption you could post about it. If nothing matches, it stops and tells you what to change (a higher price, a different size, other keywords) instead of inventing a result.",
            # FitFindr README, seller-voice mechanism
            "Mechanism: the prompt passes Platform: depop as a bare label and says \"thrift find\", but never says the user bought the item there. Depop is known as an app where individuals post their own clothes to sell, so the model often fills the gap with \"I'm selling this.\" Criterion 4 still passes because it only checks that the platform name appears, not what the sentence around it says. The tool works; the prompt leaves out who is buying.",
            # FitFindr README, worst scenario before/after
            "The worst scenario before was \"price ceiling $30\" (the band tee on Depop), with 5 of 5 cards in seller voice. After the change it had 0 of 5. Every card there now reads like \"Scored this faded grey vintage band tee on depop for only $19 and I am completely obsessed with it.\" I also read all 20 Depop cards by hand to catch seller phrasing the keyword list might miss. I didn't find any.",
        ],
    },
    {
        # Criterion 2: of 5 plainly-written human paragraphs, 0 labelled AI
        # in any trial ("unsure" is allowed).
        "name": "plain human writing",
        "criterion": 2,
        # Real people writing plainly: short sentences, common words. Not text
        # Claude wrote to imitate that — it has to be human.
        "texts": [
            # Plain human writing from the course's attack set (false_positive
            # family, written by course staff, not by me and not by AI). The same
            # texts appear in the attack run as FP01/FP03/FP04/FP07/FP08.
            # course attack set FP01 (human-written by course staff)
            "We got to the campsite about four. The pitch was fine, a bit sloped, but there was a tap nearby and the toilets were clean enough. Putting the tent up took longer than it should have because I had forgotten how the poles went. The weather held until Saturday night. Then it rained hard and kept raining. We stayed in the tent and played cards and ate most of the food we had brought for Sunday. On Sunday we packed up wet and drove home early. It was not the weekend we planned but the kids enjoyed it and we would go back.",
            # course attack set FP03 (human-written by course staff)
            "I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. I am still learning the words that people use in the office. Sometimes I do not understand the jokes. But I am happy that I came here and I think it was a good decision for my family.",
            # course attack set FP04 (human-written by course staff)
            "There are three main causes of the conflict. The first cause is economic. Trade between the two regions had declined significantly in the preceding decade. The second cause is political. Neither government was able to control its own border provinces effectively. The third cause is social. Population movements had created communities on both sides with divided loyalties. In conclusion, the conflict cannot be explained by any single factor.",
            # course attack set FP07 (human-written by course staff)
            "It rained on Monday. It rained on Tuesday. It rained on Wednesday and it rained on Thursday and by Friday I had stopped looking out of the window altogether. The forecast said it would clear. The forecast said that on Monday, and on Tuesday, and on Wednesday. I have stopped believing the forecast. I have started believing the window.",
            # course attack set FP08 (human-written by course staff)
            "Went for a run. Legs hurt. Worth it.",
        ],
    },
    {
        # Criterion 3: across the three samples, each label appears at least
        # once, and clearly-AI's combined score is >= 0.30 above clearly-human's.
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            _sample("clearly_ai"),
            _sample("clearly_human"),
            _sample("borderline"),
        ],
    },
    {
        # Criterion 4: 4 malformed requests -> 400 with a JSON error, 0 crashes.
        "name": "bad input",
        "criterion": 4,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
    # Criterion 5 (appeals) can't be tested by sending text alone: it needs a
    # submission first, then an appeal against the content_id that came back.
    # It's tested by run_appeals.py instead — see the README.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
