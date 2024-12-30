from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # allow Cross-Origin Resource Sharing 
from .routers import post, user, auth, vote
from . import models
from .database import engine
from .config import settings

# since using alembic we don't need this 
# models.Base.metadata.create_all(bind=engine) # commands to tell sqlachemy to generate all statement in db
#--------------------------------------------
# CRUD = CREATE, READ, UPDATE, DELETE
#--------------------------------------------
app = FastAPI()

origins = ["*"] # domains that can talk to our API -> '*' means allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# import all specific routs
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world"}