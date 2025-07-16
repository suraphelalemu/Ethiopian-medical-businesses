from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from .dependencies import get_db
# from .endpoints import analytics, channels, search

app = FastAPI(title="Ethiopian Medical Data API",
              description="API for analyzing medical Telegram data",
              version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(channels.router, prefix="/api/channels", tags=["Channels"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])

@app.get("/")
async def root():
    return {"message": "Ethiopian Medical Data API"}