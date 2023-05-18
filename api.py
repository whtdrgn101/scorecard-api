from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_router, bow_router, round_router, end_router, auth_router

# Cores allowable origins:
origins = [ "http://localhost", "http://localhost:3000","http://localhost:5173", "https://www.myshootinglog.com", "https://myshootinglog.com"]

# Initializes the FastAPI app
app = FastAPI(title="Scorecard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(bow_router.router)
app.include_router(round_router.router)
app.include_router(end_router.router)
