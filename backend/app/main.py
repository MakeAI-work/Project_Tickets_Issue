from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.tickets import router as tickets_router

app = FastAPI(title="Atlan Helpdesk AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets_router)


@app.get("/")
async def root():
    return {"status": "ok"}
