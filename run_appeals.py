#!/usr/bin/env python3
"""
Criterion 5, tested three times: every appeal is recorded and changes status.

    PORT=5050 python app.py                                   # one terminal
    python run_appeals.py --url http://127.0.0.1:5050 --label before

Per trial:
  1. Submit 5 texts (the samples), each as its own creator_id so the rate
     limit doesn't interfere.
  2. Appeal each content_id that came back.
  3. Check: the appeal answered 200 with status `under_review`; GET /log shows
     the original decision (unchanged) followed by the appeal.
  4. Appeal a made-up content_id. Check: refused (404) and the log grew by
     nothing.

Criterion 5 passes a trial only if all 5 appeals pass AND the fake one is
refused without a log entry. Writes results/appeals_<date>_<label>.md.
"""
import argparse
import datetime as dt
import json
from pathlib import Path

import requests

import config

ROOT = Path(__file__).parent
TEXTS = [json.loads((ROOT / "samples" / f"{n}.json").read_text())["text"]
         for n in ("clearly_ai", "clearly_human", "borderline", "edited_ai", "plain_human")]


def log_entries(url):
    return requests.get(f"{url}/log", params={"limit": 100000}, timeout=30).json()["entries"]


def run_trial(url, trial, stamp):
    checks = []
    for i, text in enumerate(TEXTS, 1):
        creator = f"appeal_{stamp}_t{trial}_{i}"
        sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator}, timeout=120)
        sub_body = sub.json()
        cid = sub_body.get("content_id")
        app = requests.post(f"{url}/appeal", json={
            "content_id": cid,
            "reasoning": f"Criterion 5 test, trial {trial}, appeal {i}."}, timeout=30)
        app_body = app.json()
        entries = [e for e in log_entries(url) if e.get("content_id") == cid]
        decided = [e for e in entries if e.get("status") == "decided"]
        appeals = [e for e in entries if e.get("event") == "appeal"]
        ok = (sub.status_code == 200 and app.status_code == 200
              and app_body.get("status") == "under_review"
              and len(decided) == 1 and len(appeals) == 1
              and decided[0].get("label") == sub_body.get("label")
              and entries.index(decided[0]) < entries.index(appeals[0]))
        checks.append({"appeal": i, "content_id": cid, "submit_status": sub.status_code,
                       "appeal_status": app.status_code, "status": app_body.get("status"),
                       "log": [e.get("event") or e.get("status") for e in entries], "pass": ok})

    before = len(log_entries(url))
    fake = requests.post(f"{url}/appeal", json={"content_id": f"c_fake_{stamp}_{trial}",
                                                "reasoning": "made-up id"}, timeout=30)
    after = len(log_entries(url))
    fake_ok = fake.status_code == 404 and after == before
    return checks, {"status": fake.status_code, "log_grew_by": after - before, "pass": fake_ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    ap.add_argument("--label", default="")
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()

    stamp = dt.datetime.now().strftime("%H%M%S")
    lines = [f"# Appeal check (criterion 5){' — ' + args.label if args.label else ''}", "",
             "- Produced by: `run_appeals.py::main`",
             "- Service: `app.py::appeal` · log: `audit.py::log_appeal`",
             f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
             "| Trial | Real appeals passed | Fake id refused, nothing logged | Trial passes |",
             "|---|---|---|---|"]
    details = []
    for t in range(1, args.trials + 1):
        checks, fake = run_trial(args.url, t, stamp)
        passed = sum(c["pass"] for c in checks)
        trial_ok = passed == len(checks) and fake["pass"]
        print(f"trial {t}: {passed}/{len(checks)} appeals ok · fake id {fake['status']}, "
              f"log grew by {fake['log_grew_by']} · {'PASS' if trial_ok else 'FAIL'}")
        lines.append(f"| {t} | {passed}/{len(checks)} | "
                     f"{'yes' if fake['pass'] else 'NO'} ({fake['status']}, log +{fake['log_grew_by']}) | "
                     f"{'PASS' if trial_ok else 'FAIL'} |")
        details.append({"trial": t, "appeals": checks, "fake_id": fake})

    lines += ["", "## What actually came back", "", "```json", json.dumps(details, indent=2), "```"]
    config.RESULTS_DIR.mkdir(exist_ok=True)
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{dt.datetime.now().strftime('%Y-%m-%d_%H%M')}{label}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
