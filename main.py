from fastapi import FastAPI
from os import path, mkdir
from fastapi.middleware.cors import CORSMiddleware
from src.utils import filesPath, imagesPath
from src.routes import routesRouter

app = FastAPI()

if not path.exists(filesPath):
    mkdir(filesPath)

if not path.exists(imagesPath):
    mkdir(imagesPath)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(routesRouter)