from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from models import QA, QASet
from srs import Card, review

app = FastAPI(title="Blooket Study Assistant")
STORE: Optional[QASet] = None
SRS: dict[int, Card] = {}

class LoadReq(BaseModel):
    title: str
    questions: List[QA]

@app.get("/health")
def health(): return {"ok": True}

@app.post("/load")
def load(req: LoadReq):
    global STORE, SRS
    STORE = QASet(title=req.title, questions=req.questions)
    SRS = {i: Card() for i in range(len(STORE.questions))}
    return {"loaded": len(STORE.questions)}

@app.get("/question")
def question(idx: int):
    if STORE is None or idx >= len(STORE.questions): return {"done": True}
    q = STORE.questions[idx]
    opts = [q.a] + q.distractors
    return {"idx": idx, "q": q.q, "options": opts, "hint": q.hint, "topic": q.topic}

@app.post("/answer")
def answer(idx: int, guess: str):
    if STORE is None or idx >= len(STORE.questions): return {"ok": False}
    q = STORE.questions[idx]
    correct = guess.strip().lower() == q.a.strip().lower()
    # Update SRS quickly: 5 if correct else 2
    SRS[idx] = review(SRS[idx], 5 if correct else 2)
    return {"ok": True, "correct": correct, "answer": q.a, "interval": SRS[idx].interval}
