from fastapi import FastAPI
from app.api import recommend

app = FastAPI()
app.include_router(recommend.router)

@app.get("/")
async def root():
	return { "message" : "Hello World" }
