# Appeal check (criterion 5) — before

- Produced by: `run_appeals.py::main`
- Service: `app.py::appeal` · log: `audit.py::log_appeal`
- 3 trials · 2026-11-17 22:12

| Trial | Real appeals passed | Fake id refused, nothing logged | Trial passes |
|---|---|---|---|
| 1 | 5/5 | yes (404, log +0) | PASS |
| 2 | 5/5 | yes (404, log +0) | PASS |
| 3 | 5/5 | yes (404, log +0) | PASS |

## What actually came back

```json
[
  {
    "trial": 1,
    "appeals": [
      {
        "appeal": 1,
        "content_id": "c_924e86c4ab11",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 2,
        "content_id": "c_be935efb9f67",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 3,
        "content_id": "c_de73a7453959",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 4,
        "content_id": "c_fea308d1ca67",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 5,
        "content_id": "c_812e0244d9ab",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      }
    ],
    "fake_id": {
      "status": 404,
      "log_grew_by": 0,
      "pass": true
    }
  },
  {
    "trial": 2,
    "appeals": [
      {
        "appeal": 1,
        "content_id": "c_412f2e25b9d3",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 2,
        "content_id": "c_1e0fd30fa332",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 3,
        "content_id": "c_93acd6104e09",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 4,
        "content_id": "c_e5769f69cacb",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 5,
        "content_id": "c_08916bc92c1e",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      }
    ],
    "fake_id": {
      "status": 404,
      "log_grew_by": 0,
      "pass": true
    }
  },
  {
    "trial": 3,
    "appeals": [
      {
        "appeal": 1,
        "content_id": "c_19662a50cd53",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 2,
        "content_id": "c_454c1d10d006",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 3,
        "content_id": "c_7691350458d1",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 4,
        "content_id": "c_80f4e6d1ce93",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      },
      {
        "appeal": 5,
        "content_id": "c_ab9da341e774",
        "submit_status": 200,
        "appeal_status": 200,
        "status": "under_review",
        "log": [
          "decided",
          "appeal"
        ],
        "pass": true
      }
    ],
    "fake_id": {
      "status": 404,
      "log_grew_by": 0,
      "pass": true
    }
  }
]
```