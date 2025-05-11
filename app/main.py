from fastapi import FastAPI
from app.api import recommend
from app.api import admin_ingest

app = FastAPI()
app.include_router(recommend.router)
app.include_router(admin_ingest.router)

@app.get("/")
async def root():
	return { "message" : "Hello World" }
