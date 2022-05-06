from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) # we dont need this anymore because autogenerating from alembic 

app = FastAPI()

#origins = ["https://www.google.com", "https://www.youtube.com"] # for particual site to allow for our api
origins = ["*"] # allow all public site/domain

app.add_middleware(
    CORSMiddleware, #function run for every requests, before going to the our below routers first goto the CORSMiddleware and perform some sort of operation
    allow_origins=origins, #what domain should be able to talk to our api
    allow_credentials=True,
    allow_methods=["*"], #what domain http method should be able to talk to our api, ex: public api where people can retrieve data we may not want them allow, and sent post request/ delete request
    allow_headers=["*"], #same as above but for headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my api!!!!!!"}

# in production env variable setted on machine, for dev we are using .env