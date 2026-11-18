# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely called AI

Of **10 pieces I wrote myself**, **at most 1** gets the high-confidence AI
label, in **every one of the three trials**.

**Why this target:** on a writing site a wrong accusation costs the writer a
lot, and a missed AI post costs the site a little. So the false-positive
number is the one I care about most. I allow 1 and not 0 because gpt2 scores
plain writing as predictable, and some of my own writing is plain. 2 or more
out of 10 would mean one in five honest writers gets accused, which I
wouldn't ship.

---

## 2. Plain human writing never gets the AI label

Of **5 plainly-written human paragraphs** (short sentences, common words, the
way my second-language student in the Milestone 1 trace writes), **0** get the
high-confidence AI label in any of the three trials. Landing in "unsure" is
allowed.

**Why this target:** my trace showed this writer gets hurt first, at signal 1,
and has the least room to argue back. The unsure band is the only automatic
thing that can save them, so I want the system to use it for them instead of
accusing them. I know gpt2's blind spot makes this hard, which is why it's a
real target and not an easy one.

---

## 3. All three labels are reachable

Across the three sample inputs in `samples/` (clearly AI, clearly human,
borderline), **each of the three labels (AI / unsure / human) appears at least
once**, in **every trial**. On top of that, the clearly AI sample's combined
score is **at least 0.30 higher** than the clearly human sample's.

**Why this target:** if one label can never be produced, my thresholds (0.35
and 0.65) have a gap and the label is just decoration. The 0.30 gap is about
the width of my unsure band (0.65 − 0.35). If clearly AI and clearly human
text aren't at least that far apart, the two signals can't separate them well
enough for the labels to mean anything.

---

## 4. Bad input gets a clear error, never a crash

For **4 malformed requests** (empty `text`, no `text` field, `text` set to
null, and about 50,000 words), the service returns a **400 with a JSON
error message** every time. That's **0 crashes (no 500s)** across all three
trials, and the server keeps running afterwards.

**Why this target:** step 2 of my trace says bad input should be stopped
before any signal runs. A crash on a malformed input is one of the most
common real failures. The 50,000-word case matters because gpt2 is slow and
an enormous paste shouldn't be able to stall or break the service for
everyone else.

---

## 5. Every appeal is recorded and changes the status

For **5 appeals** sent against real `content_id`s, **5 of 5** return a
confirmation, move the item's status to `under_review`, and appear in `/log`
next to the original decision, which is still there unchanged. An appeal
against a **made-up `content_id`** is refused with an error and **nothing**
is written to the log.

**Why this target:** in my trace, the appeal (step 7) is the last place a
wrongly accused writer can be saved and the only step with a human in it. If
even one appeal silently disappears, that writer has nothing. 5 of 5 because
there's no acceptable failure rate for losing someone's appeal. I'll test this
one by hand, since it needs a real submission first.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
