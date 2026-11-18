# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-17 22:35
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_4cb7dbb6214b` | unsure | 0.519 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_c8800f9b8f7b` | unsure | 0.521 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_23e5c6f5e909` | ai | 0.681 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_bce20a3b5610` | ai | 0.743 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_29fcc7f2bdac` | unsure | 0.596 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_ec93af5d113b` | unsure | 0.527 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_f4e4db5b1e83` | unsure | 0.507 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_e5673f979abc` | unsure | 0.521 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_9e4f5e578a88` | ai | 0.726 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_676c22de2a73` | unsure | 0.600 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_771ae6080481` | unsure | 0.573 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_e277bb4c3247` | ai | 0.660 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_6b7b6371f84d` | ai | 0.711 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_3d5c7816e380` | ai | 0.717 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_63ba8b8ac954` | ai | 0.659 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_86ba23c6ba14` | unsure | 0.600 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_508e22193214` | unsure | 0.587 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_2db5d8c80069` | unsure | 0.518 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_a5d3239005cd` | unsure | 0.509 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_e08a48c15067` | human | 0.663 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_f4a317e7e7c3` | ai | 0.653 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_a4ef1a4b3697` | unsure | 0.540 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_1ded1b4cc7f6` | unsure | 0.580 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_6dda75fc5775` | unsure | 0.552 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `c_05b2a6521b67` | human | 0.725 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_cb19e817cbbc` | unsure | 0.619 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_456240debf75` | unsure | 0.600 |  |
| MF06 | malformed | text is emoji only | 200 | `c_1bb8651e96ba` | unsure | 0.600 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_7cb31d517bd6` | unsure | 0.600 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_fc44b6ebcdd2` | unsure | 0.605 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_b13eb031cd18` | human | 0.700 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_a11988894555` | human | 0.711 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_e10ff15b476b` | human | 0.711 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_6167f8bcb4b6` | human | 0.711 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_d0df6a04166c` | human | 0.711 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_232ecdaafa2a` | human | 0.711 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_4cb7dbb6214b",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5191,
  "model_score": 0.1635,
  "style_score": 0.8746,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_c8800f9b8f7b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5208,
  "model_score": 0.5943,
  "style_score": 0.4472,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_23e5c6f5e909",
  "creator_id": "attacker_EV03",
  "guess": "ai",
  "confidence": 0.6806,
  "model_score": 0.6662,
  "style_score": 0.6951,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_bce20a3b5610",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7427,
  "model_score": 0.6114,
  "style_score": 0.8739,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_29fcc7f2bdac",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.5961,
  "model_score": 0.3212,
  "style_score": 0.4866,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_ec93af5d113b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5269,
  "model_score": 0.5727,
  "style_score": 0.3736,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_f4e4db5b1e83",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5072,
  "model_score": 0.5862,
  "style_score": 0.4282,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_e5673f979abc",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5214,
  "model_score": 0.2452,
  "style_score": 0.7121,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_9e4f5e578a88",
  "creator_id": "attacker_EV09",
  "guess": "ai",
  "confidence": 0.7257,
  "model_score": 0.7042,
  "style_score": 0.7472,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_676c22de2a73",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9792,
  "style_score": 0.4621,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_771ae6080481",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5733,
  "model_score": 0.6175,
  "style_score": 0.529,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_e277bb4c3247",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6604,
  "model_score": 0.7387,
  "style_score": 0.5822,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_6b7b6371f84d",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7109,
  "model_score": 0.8051,
  "style_score": 0.6168,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_3d5c7816e380",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7172,
  "model_score": 0.8329,
  "style_score": 0.6015,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_63ba8b8ac954",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6592,
  "model_score": 0.8005,
  "style_score": 0.5179,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_86ba23c6ba14",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.8814,
  "style_score": 0.4372,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_508e22193214",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5873,
  "model_score": 0.8816,
  "style_score": 0.293,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_2db5d8c80069",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5185,
  "model_score": 0.3223,
  "style_score": 0.6407,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_a5d3239005cd",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5086,
  "model_score": 0.4625,
  "style_score": 0.5204,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_e08a48c15067",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6628,
  "model_score": 0.2044,
  "style_score": 0.47,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_f4a317e7e7c3",
  "creator_id": "attacker_PI03",
  "guess": "ai",
  "confidence": 0.6526,
  "model_score": 0.5943,
  "style_score": 0.7109,
  "label": "This reads a lot like AI-generated text. Our check can be wrong, especially about simple or plain writing. If you wrote this yourself, you can ask for a person to review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_a4ef1a4b3697",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5404,
  "model_score": 0.4998,
  "style_score": 0.581,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_1ded1b4cc7f6",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5798,
  "model_score": 0.6401,
  "style_score": 0.5196,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_6dda75fc5775",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5518,
  "model_score": 0.5583,
  "style_score": 0.5454,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_05b2a6521b67",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.725,
  "model_score": 0.0,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_cb19e817cbbc",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.6194,
  "model_score": 0.0112,
  "style_score": 0.75,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_456240debf75",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9976,
  "style_score": 0.55,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_1bb8651e96ba",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9969,
  "style_score": 0.55,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_7cb31d517bd6",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.9064,
  "style_score": 0.55,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_fc44b6ebcdd2",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.6052,
  "model_score": 0.2395,
  "style_score": 0.55,
  "label": "We can't tell whether a person or an AI wrote this. That happens a lot, especially with short or plainly written text, and it is not an accusation. Nothing needs to be done.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_b13eb031cd18",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.7004,
  "model_score": 0.0492,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_a11988894555",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7107,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_e10ff15b476b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7107,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_6167f8bcb4b6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7107,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_d0df6a04166c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7107,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_232ecdaafa2a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7107,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
