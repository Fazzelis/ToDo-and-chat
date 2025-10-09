from fastapi import FastAPI
from controllers.routers import router
from database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
Base.metadata.create_all(bind=engine)
