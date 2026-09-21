# ITM SLS Baroda University — Synthetic Resume Analyzer Dataset

IMPORTANT:
This is a fully synthetic/demo dataset. The candidate identities, contact details, scores,
employers, salaries, resumes and hiring outcomes are fictional and must not be treated as
real student, employee, placement, or university records.

## Contents
- `candidates.csv` — structured candidate dataset for filtering, analytics and model evaluation.
- `candidates.json` — same records in JSON format.
- `resumes/` — 45 synthetic text resumes suitable for NLP/resume matching experiments.

## Suggested ML/NLP use
You can use the dataset to demonstrate:
- Resume-to-job similarity
- Skill extraction
- Keyword matching
- Resume scoring
- Candidate ranking
- Classification of hired/non-hired candidates
- TF-IDF / cosine similarity
- Sentence embeddings
- Skill-gap analysis

All 45 records have `hiring_status = Hired` because the requested dataset represents
people who completed the test and got jobs. For a real supervised classifier, add a
synthetic/non-hired control group separately rather than treating this dataset alone
as a balanced classification dataset.
