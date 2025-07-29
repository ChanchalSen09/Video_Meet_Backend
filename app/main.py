from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, meeting, websocket


app = FastAPI(title="Video Meet Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(meeting.router, prefix="/meeting", tags=["Meeting"])
app.include_router(websocket.router, tags=["WebSocket"])
