from fastapi import FastAPI, Request
import brain
import logging

app = FastAPI()
brain = brain.Brain()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/conversation")
async def root(request: Request):
    req = await request.json()
    question = req['message']
    answer = brain.languageProcessor.answer(question)
    logger.log(level=logging.DEBUG, msg=brain.languageProcessor.prompt)
    return {
        "message": answer,
    }
