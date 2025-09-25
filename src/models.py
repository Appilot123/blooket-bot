from pydantic import BaseModel, Field
from typing import List, Optional

class QA(BaseModel):
    q: str
    a: str
    distractors: List[str] = Field(default_factory=list)
    topic: Optional[str] = None
    hint: Optional[str] = None

class QASet(BaseModel):
    title: str
    questions: List[QA]
