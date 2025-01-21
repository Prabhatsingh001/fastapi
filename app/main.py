from database import engine
from fastapi import FastAPI
import models
from routers import users,posts,auth,vote
from config import Settings
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()


# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
