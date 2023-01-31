from fastapi import FastAPI, Request
import brain

app = FastAPI()
brain = brain.Brain()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/conversation")
async def root():
    return {"message": "Hello World"}


@app.post("/conversation")
async def root(request: Request):
    res = await request.json()
    question = res['message']
    answer = brain.language.conversation(question)
    return {
        "message": answer,
    }
