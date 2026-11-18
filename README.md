# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does


1. **The text arrives.** The writer sends JSON to `POST /submit` with their
   `text` and a `creator_id`. Nothing has been judged yet, so at this point
   they look exactly like everyone else.

2. **Check the input.** If `text` is missing, empty or not a string, the
   service should send back a 400 error and stop, not crash. My student's
   paragraph is normal, so it passes. (I still need to decide what "too long"
   means. gpt2 only reads the first 400 tokens anyway.)

3. **Signal 1, the model score.** `detector.py` runs gpt2 on the text and
   asks how predictable it is. Low perplexity means a higher score, meaning
   more likely AI. **This is where my student first gets hurt.** Common words
   in short, plain sentences are exactly what gpt2 finds easy to guess, so
   their honest writing can score as high as real AI text.

4. **Signal 2, the style score.** `stylometry.py` looks only at the shape of
   the text: how much sentence lengths vary, how much the vocabulary repeats,
   and punctuation. It can't read, so it doesn't care who wrote it. This could
   go either way for my student. Short sentences of similar length and a small
   vocabulary look "AI-like" here too. But if their sentences are uneven, this
   is the first place they could be saved.

5. **Combine the two.** `scoring.py` turns the two scores into one number
   from 0 to 1. Right now it's a 50/50 average. If both signals are fooled,
   my student ends up with a high combined score. If they disagree, the
   average lands in the middle.

6. **Turn it into a label, log it, and answer.** The thresholds in `config.py`
   are 0.35 and 0.65: at 0.65 or above it says AI, at 0.35 or below it says
   human, and anything in between is unsure. `audit.py` writes the decision to
   the log with a `content_id` and both signal scores, and the writer gets
   JSON back with the label, the confidence and both scores. **This is the
   label my student actually reads.** If they land in "unsure" instead of
   "AI", that middle band has saved them from a false accusation, so the
   wording of the unsure label matters a lot.

7. **Appeal.** If my student is labelled AI, they can send their
   `content_id` and their reasoning to `POST /appeal`. That logs the appeal
   next to the original decision (the log is append-only, so nothing is
   erased) and moves it to `under_review`, where a person looks at it. **This
   is the last place they can be saved**, and the only step where a human
   is involved. It only helps if they know they can appeal and feel
   confident enough to argue. A second-language writer may not.

**What this trace tells me:** the harm starts at step 3 and nothing
automatic undoes it. Steps 4 to 6 can only soften it (signal 2 disagreeing,
or landing in the unsure band), and step 7 depends on the person who was
wronged speaking up. The plain writer this signal is most likely to accuse is
also the one with the least room to argue back.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->


### Signal one — the model signal

**What it measures:** how predictable the text is to gpt2 (perplexity),
squashed onto 0–1 so that low perplexity gives a high score. Perplexity 45
scores 0.5 (`detector.py::model_signal`, which I left at the default
midpoint).

**Why that might differ between human and AI writing:** a language model
writes by picking likely next words, so its text is easy for another model to
predict. Human writing has more odd word choices and sudden turns.

**What it can't see:** who actually wrote it. It rewards common words in
short, ordinary sentences, and plenty of real people write like that. In my
calibration run the plain human paragraph (written like my second-language
student) scored **0.852**, *higher* than the clearly AI sample (0.754). It
also gets fooled the other way: the formal, ornate human paragraph scored
0.248, which reads as very human, just because the rare words surprise gpt2.

### Signal two — the style signal

**What it measures:** the shape of the text, without reading it
(`stylometry.py`). Three measures:
- **Sentence-length spread:** stdev of words per sentence divided by the
  mean. Higher means lumpier, which is more human.
- **Type-token ratio:** moving average over 50-word windows, so length
  doesn't decide it. Higher means more varied vocabulary.
- **Expressive punctuation per word:** ; : — – ( ) ! ? quotes, not full stops
  or commas. Higher is more human.

Only spread (weight 0.6) and punctuation (weight 0.4) count toward the
score. Punctuation can only move the score between 0.25 and 0.75, because
having no dashes or semicolons is weak evidence: lots of people never use
them. **Type-token ratio gets weight 0** because it ran *backwards* on my
calibration texts. The AI samples had the most varied vocabulary (0.91,
0.94) and the plain human writer the least (0.77), so counting it would have
accused plain writers even more. It's still computed so I can watch it.

**Why that might differ between human and AI writing:** "most likely next
word" produces even, mid-length sentences. People mix a three-word sentence
with a forty-word one and use dashes, brackets and exclamation marks.

**What it can't see:** what the text says. Anything that changes the shape
without changing the content moves it. Chopping an AI paragraph into short
sentences and adding a dash and an exclamation mark took the AI style score
from 0.75 down to **0.20**. And it accuses plain writers too: my plain human
paragraph has even, short sentences and no expressive punctuation, so it
scored **0.864**, the most AI-like of all seven texts.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** average the two scores equally. But if the two signals
disagree by more than 0.30, the combined score is capped at 0.60, just under
the AI threshold (0.65). In words: when my two methods disagree, that is
uncertainty, and an uncertain case can be "unsure" but never "AI". The cap
only works in one direction. A split can still come out as "human", because
the costly mistake is accusing a real writer, not missing some AI text.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`,
`DISAGREEMENT_GAP = 0.30`, `DISAGREEMENT_CAP = 0.60` (all in `config.py`).

**Where it lives:** `scoring.py::combine_signals`


**A case where my two signals split, and what my rule does with it:**
A formal, ornate test paragraph about the marathon ("Whosoever undertakes
the labour of a marathon discovers…"). gpt2 scored it **0.248** (human)
because the rare words surprised it. The style signal scored it **0.831**
(AI) because its three long sentences are similar in length and it has no
expressive punctuation. They're **0.58 apart**, so my disagreement cap
applies. The equal average is already 0.539, below the 0.60 cap, so it lands
in **unsure**, not AI. Without the cap, a split where gpt2 says 0.9 and style
says 0.4 would average 0.65 and be labelled AI. With my rule it's held at
0.60, which is unsure.

**Calibration run** (one trial each, run from the terminal):

| Input | model | style | gap | combined | where it would land |
|---|---|---|---|---|---|
| clearly AI (`samples/clearly_ai.json`) | 0.754 | 0.752 | 0.00 | 0.753 | AI |
| lightly-edited AI (`samples/edited_ai.json`) | 0.691 | 0.687 | 0.00 | 0.689 | AI |
| borderline (`samples/borderline.json`) | 0.349 | 0.571 | 0.22 | 0.460 | unsure |
| **plain human** (`samples/plain_human.json`) | **0.852** | **0.864** | 0.01 | **0.858** | **AI (wrong)** |
| clearly human (`samples/clearly_human.json`) | 0.445 | 0.215 | 0.23 | 0.330 | human |
| formal human (split case) | 0.248 | 0.831 | 0.58 | 0.539 | unsure |
| choppy AI (short sentences, a dash, a "!") | 0.527 | 0.196 | 0.33 | 0.362 | unsure (just) |

⚠️ *The plain human, lightly-edited AI, formal and choppy texts are
stand-ins Claude wrote to imitate those styles, not real human writing.
TODO: replace `samples/plain_human.json` with a plain paragraph a real person
wrote (ideally mine) and re-run before trusting these numbers.*

**What this shows:** the system separates clearly AI from clearly human
text (0.753 vs 0.330, a gap of 0.42). But the plain human writer from my
Milestone 1 trace gets the *highest* score of all, because **both signals
accuse them at once**, and my disagreement rule only helps when the signals
split. On this run my criterion 2 (no plain human writing labelled AI) would
fail. I'm not tuning the numbers to make it pass now: that's what the Unit 8
test and fix are for.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.65 | We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done. |
| high-confidence AI | 0.65 – 1.00 | This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it. |

All three are reachable. From the sample run below: `samples/clearly_human.json`
scored 0.330 → human, `samples/borderline.json` 0.460 → unsure, and
`samples/clearly_ai.json` 0.753 → AI.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->


The person who reads "unsure" may well have written every word, and my
calibration run showed plain writers land high on both signals. So the label
says three things in plain words: we don't know, this is common (especially
for plain writing, so they don't feel singled out), and it isn't an
accusation and needs no action. It never mentions a score or a threshold. I
also put "our check can be wrong" and the review option into the AI label
itself, because my own data says the AI label will sometimes hit a real
person, and the appeal (step 7 of my trace) only helps if they know it
exists.

*Confidence* in the response is how far the combined score leans to whichever
side it's on: `max(score, 1 − score)`, so 0.5 is a coin flip and 1.0 is
completely sure.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

(Port 5050 because macOS AirPlay Receiver holds 5000 on my Mac:
`PORT=5050 python app.py`.)

```bash
$ curl -X POST http://127.0.0.1:5050/submit \
  -H "Content-Type: application/json" \
  -d @samples/clearly_ai.json
```

```json
{
  "combined_score": 0.7533,
  "confidence": 0.7533,
  "content_id": "c_04296a2fd24f",
  "creator_id": "demo_instructor",
  "guess": "ai",
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "model_score": 0.7544,
  "style_score": 0.7523
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5050/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_04296a2fd24f", "reasoning": "I wrote this myself for a work newsletter. It is formal because it was for my manager."}'
```

```json
{
  "content_id": "c_04296a2fd24f",
  "message": "Thanks. A person will review this. Your original result is kept, and your reasons are saved next to it.",
  "original_label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "status": "under_review"
}
```

An appeal against a made-up id (`c_doesnotexist`) gets a **404** with "No
submission with content_id 'c_doesnotexist'. Check it was copied exactly."
and writes nothing to the log. Appealing the same id twice returns "This is
already waiting for a person to review it." without adding a second entry.

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5050/log?limit=4"
```

```json
[
  {"timestamp": "2026-11-18T05:36:37+00:00", "content_id": "c_04296a2fd24f", "creator_id": "demo_instructor",
   "guess": "ai", "model_score": 0.7544, "style_score": 0.7523, "combined_score": 0.7533,
   "label": "This reads a lot like AI-generated text. …", "status": "decided"},
  {"timestamp": "2026-11-18T05:36:37+00:00", "content_id": "c_74dc024381e1", "creator_id": "demo_instructor",
   "guess": "unsure", "model_score": 0.3489, "style_score": 0.5714, "combined_score": 0.4602,
   "label": "We can't tell whether a person or an AI wrote this. …", "status": "decided"},
  {"timestamp": "2026-11-18T05:36:37+00:00", "content_id": "c_3309d9b702c8", "creator_id": "demo_instructor",
   "guess": "human", "model_score": 0.4445, "style_score": 0.2147, "combined_score": 0.3296,
   "label": "We think this was probably written by a person.", "status": "decided"},
  {"timestamp": "2026-11-18T05:36:37+00:00", "content_id": "c_04296a2fd24f", "creator_id": "demo_instructor",
   "event": "appeal", "status": "under_review",
   "reasoning": "I wrote this myself for a work newsletter. It is formal because it was for my manager."}
]
```

The original decision for `c_04296a2fd24f` is still there unchanged, and the
appeal sits after it with status `under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (on `POST /submit`, set in
`config.py`; rate limiting is on by default now, `AI201_RATE_LIMITS=0` turns
it off)

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer submits their own work a few times an hour. Even someone fixing
a typo and resubmitting rarely sends more than 5 in a minute, and 50 in a day
is far more than a person posting their own writing needs. A script trying
to map my thresholds (sending small variations of a text to find exactly
where "unsure" turns into "AI") needs hundreds or thousands of tries. At 50 a
day per creator, that takes weeks instead of minutes. I went lower than the
default 10/200 because every submission runs gpt2 on my laptop, which takes
real time, so a flood also slows the service for everyone else.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->
Per `creator_id`, falling back to the caller's address if there isn't one.
The weakness: `creator_id` is whatever the caller sends, so a script can
invent a new one on every request and never hit the limit. One script can
look like a thousand callers. I didn't add a per-address limit as well,
because on my laptop every test (including the whole attack set) comes from
the same address, `127.0.0.1`, and an address limit would block my own test
run. For a real deployment I'd add a looser per-address limit on top, for
example 30 a minute. The flip side of per-address is that one household or
classroom sharing an address would look like one caller.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15 --url http://127.0.0.1:5050
15 submissions as 'flood_tester' against http://127.0.0.1:5050

200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

10 of 15 were rate limited.
```

Every rejection leaves a trace in the log, so a flood doesn't show up only as
an absence:

```json
{"timestamp": "2026-11-18T05:44:00+00:00", "creator_id": "flood_tester", "event": "rejected",
 "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

Inputs `/submit` refuses are logged the same way, with their own reason
(`empty_or_missing_text`, `too_short`, `too_long`, `detector_unavailable`):

```json
{"timestamp": "2026-11-18T05:44:16+00:00", "creator_id": "m1_badinput", "event": "rejected",
 "status": "rejected", "reason": "empty_or_missing_text"}
{"timestamp": "2026-11-18T05:44:16+00:00", "creator_id": "m1_short", "event": "rejected",
 "status": "rejected", "reason": "too_short", "text_length": 2}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



`python run_attacks.py --set attack_set --url http://127.0.0.1:5050 --label before`,
56 attacks, 2026-11-17. Full output: `results/attack_run_2026-11-17_2158_before.md`.
Score is the response's `confidence` (`max(score, 1 − score)`), so a "human"
row at 0.672 means a combined score of 0.328.

**How I judged held vs broke** (thresholds: AI ≥ 0.65, human ≤ 0.35):
- *Evasion* (AI text dressed up): **broke** if it escaped the AI label.
- *False positive* (real human text): **broke** if it got the AI label.
- *Prompt injection*: **broke** if the AI text came out human, or the label
  or log was changed.
- *Malformed*: **broke** on a crash, or if junk got a confident label.

| ID | Family | Targeting | Status | Guess | Score | Verdict | Why |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety | 200 | unsure | 0.526 | BROKE | AI text escaped the AI label. The typos hit signal **one** (model 0.16), not signal two |
| EV02 | evasion | broken-up sentences raise spread | 200 | unsure | 0.548 | BROKE | AI text escaped to unsure |
| EV03 | evasion | pasted quotation changes the shape | 200 | unsure | 0.619 | BROKE | AI text escaped to unsure |
| EV04 | evasion | unusual words raise perplexity | 200 | ai | 0.749 | HELD | still AI |
| EV05 | evasion | heavy human editing pass | 200 | unsure | 0.593 | BROKE | escaped to unsure |
| EV06 | evasion | one very long + one very short sentence | 200 | unsure | 0.529 | BROKE | escaped to unsure |
| EV07 | evasion | padding with punctuation | 200 | unsure | 0.500 | BROKE | punctuation pulled style to 0.41 |
| EV08 | evasion | text below the token window | 200 | unsure | 0.544 | BROKE | escaped to unsure |
| EV09 | evasion | human opening bolted onto AI text | 200 | ai | 0.706 | HELD | still AI |
| EV10 | evasion | repeated stanza structure | 200 | ai | 0.874 | HELD | still AI |
| FP01 | false_positive | plain, clear human writing | 200 | **ai** | 0.667 | **BROKE** | a real person labelled AI |
| FP02 | false_positive | human, formal register | 200 | **ai** | 0.801 | **BROKE** | labelled AI |
| FP03 | false_positive | non-native speaker writing carefully | 200 | **ai** | 0.810 | **BROKE** | labelled AI: my Milestone 1 trace person |
| FP04 | false_positive | student essay written to a rubric | 200 | **ai** | 0.811 | **BROKE** | labelled AI |
| FP05 | false_positive | technical documentation by a person | 200 | **ai** | 0.823 | **BROKE** | labelled AI |
| FP06 | false_positive | person imitating a formal template | 200 | **ai** | 0.773 | **BROKE** | labelled AI |
| FP07 | false_positive | human repeating a phrase on purpose | 200 | unsure | 0.600 | HELD | the disagreement cap held it at 0.60 |
| FP08 | false_positive | very short genuine human text | 200 | unsure | 0.529 | HELD | not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.509 | HELD | no instruction followed, not labelled human |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | **human** | 0.672 | **BROKE** | AI text labelled human (combined 0.328). The odd header raised perplexity |
| PI03 | prompt_injection | instruction in the writer's voice | 200 | unsure | 0.612 | HELD | not labelled human |
| PI04 | prompt_injection | make the label text hostile | 200 | unsure | 0.553 | HELD | labels are fixed strings, can't be changed |
| PI05 | prompt_injection | inject into the audit log | 200 | unsure | 0.572 | HELD | the fake JSON stayed inside the text; log entry is clean |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.642 | HELD | not labelled human |
| MF01 | malformed | only whitespace | 400 | — | — | HELD | refused, logged |
| MF02 | malformed | a single character | 400 | — | — | HELD | refused (too_short) |
| MF03 | malformed | control characters | 200 | **human** | 0.700 | **BROKE** | junk got "probably written by a person" |
| MF04 | malformed | only punctuation | 200 | unsure | 0.544 | HELD | no crash, no accusation |
| MF05 | malformed | a very long single word | 200 | unsure | 0.600 | HELD | no crash, no accusation |
| MF06 | malformed | emoji only | 200 | unsure | 0.600 | HELD | no crash; model 0.997 but capped |
| MF07 | malformed | right-to-left script | 200 | unsure | 0.600 | HELD | no crash, no accusation |
| MF08 | malformed | 60,000 characters | 400 | — | — | HELD | refused (too_long) |
| RQ01 | malformed | no text field | 400 | — | — | HELD | refused |
| RQ02 | malformed | no creator_id | 200 | unsure | 0.580 | HELD | logged as `unknown` |
| RQ03 | malformed | text is a number | 400 | — | — | HELD | refused |
| RQ04 | malformed | text is a list | 400 | — | — | HELD | refused |
| RQ05 | malformed | text is null | 400 | — | — | HELD | refused |
| RQ06 | malformed | creator_id is an object | 200 | human | 0.675 | HELD | creator logged as `unknown`, no crash |
| RQ07 | malformed | body is a JSON array | 400 | — | — | HELD | refused (fixed in Unit 8 M1) |
| RQ08 | malformed | unparseable JSON | 400 | — | — | HELD | refused |
| RQ09 | malformed | empty body | 400 | — | — | HELD | refused |
| RQ10 | malformed | form-encoded body | 429 | — | — | HELD | rate-limited before validation (shared `127.0.0.1` bucket) |
| RQ11 | malformed | JSON sent as text/plain | 429 | — | — | HELD | same shared bucket |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD | refused |
| FL01_01–05 | flood_same_creator | 20 rapid submissions, one creator | 200 | human | 0.686 | HELD | first 5 allowed |
| FL01_06–12 | flood_same_creator | 20 rapid submissions, one creator | 429 | — | — | HELD | rate-limited and logged |

**Totals:** 0 crashes (no 5xx anywhere). 15 of 56 broke: 7 of 10 evasions,
**6 of 8 false positives**, 1 of 6 prompt injections, 1 malformed. Every
malformed request and the flood held.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_caa4605539f1", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.8156, "combined_score": 0.8104, "label": "This reads a lot like AI-generated text. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_f8b1f38c3cda", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.8638, "combined_score": 0.8013, "label": "This reads a lot like AI-generated text. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_83d649526ffa", "creator_id": "attacker_FP01", "guess": "ai", "model_score": 0.6175, "style_score": 0.7157, "combined_score": 0.6666, "label": "This reads a lot like AI-generated text. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_8befadfcb805", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.4524, "combined_score": 0.3284, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-18T05:58:36+00:00", "content_id": "c_240522d99eb4", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.8887, "combined_score": 0.5261, "label": "We can't tell whether a person or an AI wrote this. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_55ce1eb773c5", "creator_id": "attacker_EV07", "guess": "unsure", "model_score": 0.5862, "style_score": 0.4143, "combined_score": 0.5003, "label": "We can't tell whether a person or an AI wrote this. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_f2c8ca2679c6", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.6, "combined_score": 0.3, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-18T05:58:37+00:00", "content_id": "c_3d9d8a7743cd", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.5045, "combined_score": 0.5723, "label": "We can't tell whether a person or an AI wrote this. …", "status": "decided"}
{"timestamp": "2026-11-18T05:58:38+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-18T05:58:38+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "too_long", "text_length": 57640}
```

(Labels shortened with … here. The log has the full text.) What they show:
- **FP03, FP02, FP01:** real people labelled AI, with *both* signals high, so
  my disagreement cap never triggered.
- **PI02:** AI text labelled human.
- **EV01, EV07:** the signals split hard (0.16 vs 0.89, 0.59 vs 0.41) and
  the average lands in unsure.
- **MF03:** junk labelled human.
- **PI05:** the log injection stayed inside the text field.
- **The `unknown` 429:** RQ10 rejected only because every request without a
  `creator_id` shares one address bucket.
- **MF08:** a 57,640-character paste refused before gpt2 ran.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03, a non-native English speaker writing carefully, labelled AI at 0.810**
("I want to describe my experience of the first month in this country. The
weather was very different from my home…"). This is exactly the person I
followed through my Milestone 1 trace, and the trace predicted where they'd
get hurt. Both signals accused them: gpt2 found their careful, common words
predictable (0.805), and stylometry read their even, short sentences as
machine-like (0.816). My combining rule only protects people when the two
signals *disagree*, so it did nothing. The writer most likely to be accused
is the one with the least room to argue back, and the only thing left for
them is the appeal.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
