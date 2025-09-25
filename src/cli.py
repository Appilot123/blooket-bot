import argparse, json, pandas as pd, pathlib
from slugify import slugify
from models import QA, QASet

p = argparse.ArgumentParser(description="CSV → Blooket-style JSON (ethical, no automation)")
p.add_argument("--csv", required=True, help="Input CSV with columns: question, answer, distractor1..3, topic?, hint?")
p.add_argument("--out", required=True, help="Output JSON file")
p.add_argument("--title", default=None)
args = p.parse_args()

df = pd.read_csv(args.csv)
questions = []
for _, r in df.iterrows():
    distractors = []
    for c in df.columns:
        if str(c).lower().startswith("distractor") and pd.notna(r.get(c)):
            distractors.append(str(r.get(c)))
    questions.append(QA(
        q=str(r["question"]),
        a=str(r["answer"]),
        distractors=distractors,
        topic=(str(r["topic"]) if "topic" in df.columns and pd.notna(r.get("topic")) else None),
        hint=(str(r["hint"]) if "hint" in df.columns and pd.notna(r.get("hint")) else None),
    ))
title = args.title or slugify(pathlib.Path(args.csv).stem).replace("-", " ").title()
payload = QASet(title=title, questions=questions)
pathlib.Path(args.out).write_text(payload.model_dump_json(indent=2), encoding="utf-8")
print(f"Wrote {args.out} ({len(questions)} questions)")
