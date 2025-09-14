import json
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.classifier import classify_ticket
from backend.app.core.rag import answer_with_rag

router = APIRouter(prefix="/api")

DATA_PATH = Path(__file__).parent.parent / "data" / "sample_tickets.json"

if DATA_PATH.exists():
    RAW_TICKETS = json.loads(DATA_PATH.read_text())
else:
    RAW_TICKETS = []

classified_cache = [
    {**t, **classify_ticket(f"{t['subject']} {t['body']}")}
    for t in RAW_TICKETS
]


class Query(BaseModel):
    text: str


@router.get("/tickets")
def get_tickets():
    return classified_cache


@router.post("/classify_answer")
def classify_and_answer(payload: Query):
    txt = payload.text
    analysis = classify_ticket(txt)
    topic = analysis["topic"]
    if topic in {"How-to", "Product", "Best practices", "API/SDK", "SSO"}:
        answer, sources = answer_with_rag(txt, topic)
    else:
        answer = (
            f"This ticket has been classified as a '{topic}' issue and routed to the appropriate team."
        )
        sources = []
    return {"analysis": analysis, "response": answer, "sources": sources}
