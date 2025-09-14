from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.tickets import router as tickets_router

app = FastAPI(title="Atlan Helpdesk AI")
# Configure CORS for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://atlan-helpdesk-frontend.onrender.com",  # Your frontend URL
        "https://*.onrender.com",  # Other Render deployments
        "https://*.netlify.app",   # Netlify deployments
        "https://*.vercel.app",    # Vercel deployments
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(tickets_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Atlan Helpdesk AI API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "atlan-helpdesk-api",
        "version": "1.0.0"
    }
